from __future__ import annotations

import io
from typing import Tuple

import cv2
import numpy as np
from PIL import Image
from skimage.feature import local_binary_pattern
from tensorflow.keras.applications.efficientnet import preprocess_input


IMG_SIZE: Tuple[int, int] = (224, 224)


def _load_image_from_bytes(data: bytes, resample: int = Image.NEAREST) -> np.ndarray:
    """Decode and resize like the training pipelines.

    - skin type / disease models were trained with Keras ImageDataGenerator.flow_from_directory
      (nearest-neighbour resizing);
    - the concern model was trained with image_dataset_from_directory (bilinear resizing).
    """
    img = Image.open(io.BytesIO(data)).convert("RGB")
    img = img.resize(IMG_SIZE, resample)
    return np.array(img, dtype="float32")


def preprocess_for_skin_type(data: bytes) -> tuple[np.ndarray, np.ndarray]:
    """
    Returns:
        image_input: (1, 224, 224, 3) normalized 0-1 RGB
        lbp_input:   (1, 26) histogram
    """
    img = _load_image_from_bytes(data) / 255.0

    # LBP on grayscale, matching training code
    gray = cv2.cvtColor((img * 255).astype("uint8"), cv2.COLOR_RGB2GRAY)
    radius = 3
    n_points = 8 * radius
    n_bins = n_points + 2

    lbp = local_binary_pattern(gray, P=n_points, R=radius, method="uniform")
    hist, _ = np.histogram(
        lbp.ravel(),
        bins=np.arange(0, n_bins + 1),
        range=(0, n_bins),
    )
    hist = hist.astype("float32")
    hist /= (hist.sum() + 1e-8)

    image_input = np.expand_dims(img, axis=0)
    lbp_input = np.expand_dims(hist, axis=0)
    return image_input, lbp_input


def preprocess_for_disease(data: bytes) -> np.ndarray:
    """
    EfficientNet-like 224x224 RGB scaled to [0,1] as in training.
    """
    img = _load_image_from_bytes(data) / 255.0
    return np.expand_dims(img, axis=0)


def preprocess_for_concern(data: bytes) -> np.ndarray:
    """
    EfficientNet B0 preprocessing (same as training script).
    """
    img = _load_image_from_bytes(data, Image.BILINEAR)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img

