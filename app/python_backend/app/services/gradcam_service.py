from __future__ import annotations

import base64
import io
from typing import Optional, Tuple

import cv2
import numpy as np
import tensorflow as tf
from PIL import Image


def _find_last_conv_layer(model: tf.keras.Model) -> tf.keras.layers.Layer | None:
    # Search nested EfficientNet first if present
    for layer in model.layers:
        if isinstance(layer, tf.keras.Model) and "efficientnet" in layer.name.lower():
            for l in reversed(layer.layers):
                if isinstance(l, tf.keras.layers.Conv2D):
                    return l
    # Fallback: last Conv2D in top-level
    for layer in reversed(model.layers):
        if isinstance(layer, tf.keras.layers.Conv2D):
            return layer
    return None


def _nested_backbone(model: tf.keras.Model) -> tf.keras.Model | None:
    for layer in model.layers:
        if isinstance(layer, tf.keras.Model) and "efficientnet" in layer.name.lower():
            return layer
    return None


def _gradcam_nested(model: tf.keras.Model, backbone: tf.keras.Model, img_tensor: tf.Tensor) -> np.ndarray:
    """Grad-CAM for models whose backbone is a nested sub-model (EfficientNet concern model).

    The layers after the backbone (pooling, batch norm, dense, softmax) are re-applied to the backbone's
    feature map so that gradients can flow from the class score to the last convolutional feature map.
    """
    head_in = tf.keras.Input(shape=backbone.output_shape[1:])
    x = head_in
    found = False
    for layer in model.layers:
        if found:
            x = layer(x)
        elif layer.name == backbone.name:
            found = True
    head = tf.keras.Model(head_in, x)

    feature_map = tf.convert_to_tensor(backbone(img_tensor, training=False))
    with tf.GradientTape() as tape:
        tape.watch(feature_map)
        preds = head(feature_map, training=False)
        class_channel = preds[:, tf.argmax(preds[0])]
    grads = tape.gradient(class_channel, feature_map)
    pooled = tf.reduce_mean(grads, axis=(0, 1, 2))
    heat = tf.squeeze(feature_map[0] @ pooled[..., tf.newaxis])
    heat = tf.maximum(heat, 0) / (tf.math.reduce_max(heat) + 1e-10)
    return heat.numpy()


def _gradcam_flat(model: tf.keras.Model, img_tensor: tf.Tensor) -> np.ndarray | None:
    last_conv = _find_last_conv_layer(model)
    if last_conv is None:
        return None
    grad_model = tf.keras.Model(inputs=model.inputs, outputs=[last_conv.output, model.output])
    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_tensor, training=False)
        class_channel = predictions[:, tf.argmax(predictions[0])]
    grads = tape.gradient(class_channel, conv_outputs)
    pooled = tf.reduce_mean(grads, axis=(0, 1, 2))
    heat = tf.squeeze(conv_outputs[0] @ pooled[..., tf.newaxis])
    heat = tf.maximum(heat, 0) / (tf.math.reduce_max(heat) + 1e-10)
    return heat.numpy()


def _decode_image(data: bytes, size: Tuple[int, int]) -> np.ndarray:
    img = Image.open(io.BytesIO(data)).convert("RGB")
    img = img.resize(size)
    return np.array(img)


def generate_gradcam_base64(
    model: tf.keras.Model,
    img_tensor: tf.Tensor,
    original_image_bytes: bytes,
    image_size: Tuple[int, int] = (224, 224),
) -> Optional[str]:
    """
    Generic Grad-CAM for classification models.

    Args:
        model: classification model
        img_tensor: (1, H, W, C) tensor used for prediction
        original_image_bytes: uploaded image bytes for overlay

    Returns:
        base64-encoded JPEG heatmap overlay, or None on failure
    """
    try:
        backbone = _nested_backbone(model)
        heatmap = (
            _gradcam_nested(model, backbone, img_tensor)
            if backbone is not None
            else _gradcam_flat(model, img_tensor)
        )
        if heatmap is None:
            return None

        # Resize heatmap
        heatmap = cv2.resize(heatmap, image_size)
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

        # Original image for overlay
        img = _decode_image(original_image_bytes, image_size)
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        overlay = cv2.addWeighted(img_bgr, 0.6, heatmap, 0.4, 0)

        # Encode as JPEG base64
        _, buffer = cv2.imencode(".jpg", overlay)
        b64 = base64.b64encode(buffer.tobytes()).decode("utf-8")
        return f"data:image/jpeg;base64,{b64}"
    except Exception as exc:  # Grad-CAM must never break the prediction
        import logging
        logging.getLogger(__name__).warning("Grad-CAM failed: %s", exc)
        return None

