from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Literal, Optional

import numpy as np
import tensorflow as tf

from app.config import get_settings
from app.core.model_loader import get_model_registry
from app.services.gradcam_service import generate_gradcam_base64
from app.services.image_processing import (
    preprocess_for_concern,
    preprocess_for_disease,
    preprocess_for_skin_type,
)
from app.services.recommendation_engine import Recommendation, generate_recommendation


settings = get_settings()
models = get_model_registry()

AnalysisMode = Literal[
    "full",
    "skin_type",
    "skin_disease",
    "skin_concern",
]


@dataclass
class PredictionResult:
    label: str
    confidence: float
    probabilities: Dict[str, float]
    status: str = "OK"


@dataclass
class FullAnalysisResult:
    mode: AnalysisMode
    skin_type: Optional[PredictionResult]
    skin_disease: Optional[PredictionResult]
    skin_concern: Optional[PredictionResult]
    disease_gradcam: Optional[str]
    concern_gradcam: Optional[str]
    recommendation: Optional[Recommendation]
    global_status: str
    message: Optional[str]


LOW_CONF_MESSAGE = (
    "The lighting or focus of the image is insufficient. "
    "Please upload a clearer photo for an accurate dermatological assessment."
)


def _softmax(x: np.ndarray) -> np.ndarray:
    e = np.exp(x - np.max(x))
    return e / e.sum(axis=-1, keepdims=True)


def _build_prediction(
    logits: np.ndarray,
    classes: list[str],
) -> PredictionResult:
    if logits.ndim == 2:
        logits = logits[0]
    # Many Keras classifiers already output probabilities (softmax). If it already
    # looks like a probability distribution, keep it; otherwise apply softmax.
    if (
        np.all(logits >= 0.0)
        and np.all(logits <= 1.0)
        and np.isfinite(logits).all()
        and abs(float(np.sum(logits)) - 1.0) < 1e-3
    ):
        probs = logits
    else:
        probs = _softmax(logits)
    idx = int(np.argmax(probs))
    label = classes[idx]
    confidence = float(probs[idx])
    return PredictionResult(
        label=label,
        confidence=confidence,
        probabilities={c: float(p) for c, p in zip(classes, probs)},
    )


async def run_skin_type_inference(image_bytes: bytes) -> PredictionResult:
    image_input, lbp_input = preprocess_for_skin_type(image_bytes)
    model = models.skin_type_model
    preds = model.predict({"image_input": image_input, "lbp_input": lbp_input}, verbose=0)
    return _build_prediction(preds, settings.skin_type_classes)


async def run_skin_disease_inference(
    image_bytes: bytes,
) -> tuple[PredictionResult, Optional[str]]:
    img_tensor = preprocess_for_disease(image_bytes)
    model = models.skin_disease_model
    preds = model.predict(img_tensor, verbose=0)
    pred = _build_prediction(preds, settings.skin_disease_classes)

    gradcam_b64 = generate_gradcam_base64(
        model=model,
        img_tensor=tf.convert_to_tensor(img_tensor),
        original_image_bytes=image_bytes,
    )

    if pred.confidence < settings.reliability_threshold:
        pred.status = "LOW_CONFIDENCE_RETRY"

    return pred, gradcam_b64


async def run_skin_concern_inference(
    image_bytes: bytes,
) -> tuple[PredictionResult, Optional[str]]:
    img_tensor = preprocess_for_concern(image_bytes)
    model = models.skin_concern_model
    preds = model.predict(img_tensor, verbose=0)
    pred = _build_prediction(preds, settings.skin_concern_classes)

    gradcam_b64 = generate_gradcam_base64(
        model=model,
        img_tensor=tf.convert_to_tensor(img_tensor),
        original_image_bytes=image_bytes,
    )

    if pred.confidence < settings.reliability_threshold:
        pred.status = "LOW_CONFIDENCE_RETRY"

    return pred, gradcam_b64


async def run_analysis(
    mode: AnalysisMode,
    image_bytes: bytes,
) -> FullAnalysisResult:
    """
    Orchestrates all analyses and applies global low-confidence logic.
    """
    skin_type_res: Optional[PredictionResult] = None
    disease_res: Optional[PredictionResult] = None
    concern_res: Optional[PredictionResult] = None
    disease_cam: Optional[str] = None
    concern_cam: Optional[str] = None
    recommendation: Optional[Recommendation] = None

    if mode == "skin_type":
        skin_type_res = await run_skin_type_inference(image_bytes)
    elif mode == "skin_disease":
        disease_res, disease_cam = await run_skin_disease_inference(image_bytes)
    elif mode == "skin_concern":
        concern_res, concern_cam = await run_skin_concern_inference(image_bytes)
    else:
        # full analysis – run concurrently where possible
        import asyncio

        skin_type_task = asyncio.create_task(run_skin_type_inference(image_bytes))
        disease_task = asyncio.create_task(run_skin_disease_inference(image_bytes))
        concern_task = asyncio.create_task(run_skin_concern_inference(image_bytes))

        skin_type_res, (disease_res, disease_cam), (concern_res, concern_cam) = await asyncio.gather(
            skin_type_task,
            disease_task,
            concern_task,
        )

    global_status = "OK"
    message: Optional[str] = None

    # Global low confidence logic for disease/concern
    low_conf = any(
        r is not None and r.status == "LOW_CONFIDENCE_RETRY"
        for r in (disease_res, concern_res)
    )
    if low_conf:
        global_status = "LOW_CONFIDENCE_RETRY"
        message = LOW_CONF_MESSAGE

    if global_status == "OK":
        recommendation = generate_recommendation(
            skin_type=skin_type_res.label if skin_type_res else None,
            disease=disease_res.label if disease_res else None,
            concern=concern_res.label if concern_res else None,
        )

    return FullAnalysisResult(
        mode=mode,
        skin_type=skin_type_res,
        skin_disease=disease_res,
        skin_concern=concern_res,
        disease_gradcam=disease_cam,
        concern_gradcam=concern_cam,
        recommendation=recommendation,
        global_status=global_status,
        message=message,
    )

