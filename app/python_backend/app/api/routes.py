from __future__ import annotations

import time
from typing import Dict

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

from app.config import Settings, get_settings
from app.core.model_loader import get_model_registry
from app.services.inference_service import AnalysisMode, run_analysis
from app.utils.validators import validate_upload_image


router = APIRouter()


def get_settings_dep() -> Settings:
    return get_settings()


_RATE_LIMIT_STATE: Dict[str, list[float]] = {}


def _check_rate_limit(client_id: str, settings: Settings) -> None:
    window = settings.rate_limit_window_seconds
    max_req = settings.rate_limit_requests
    now = time.time()
    timestamps = _RATE_LIMIT_STATE.get(client_id, [])
    timestamps = [t for t in timestamps if now - t <= window]
    if len(timestamps) >= max_req:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please wait a moment before trying again.",
        )
    timestamps.append(now)
    _RATE_LIMIT_STATE[client_id] = timestamps


@router.post("/analyze")
async def analyze_image(
    mode: AnalysisMode = "full",
    file: UploadFile = File(...),
    settings: Settings = Depends(get_settings_dep),
):
    # Simple client identifier (in production: IP or auth user id)
    client_id = "anonymous"
    _check_rate_limit(client_id, settings)

    raw_bytes = await validate_upload_image(file)

    # Ensure models are loaded (startup also loads, but this is safe)
    get_model_registry().load_models()

    result = await run_analysis(mode=mode, image_bytes=raw_bytes)
    return JSONResponse(
        {
            "mode": result.mode,
            "global_status": result.global_status,
            "message": result.message,
            "skin_type": None
            if result.skin_type is None
            else {
                "label": result.skin_type.label,
                "confidence": result.skin_type.confidence,
                "probabilities": result.skin_type.probabilities,
                "status": result.skin_type.status,
            },
            "skin_disease": None
            if result.skin_disease is None
            else {
                "label": result.skin_disease.label,
                "confidence": result.skin_disease.confidence,
                "probabilities": result.skin_disease.probabilities,
                "status": result.skin_disease.status,
            },
            "skin_concern": None
            if result.skin_concern is None
            else {
                "label": result.skin_concern.label,
                "confidence": result.skin_concern.confidence,
                "probabilities": result.skin_concern.probabilities,
                "status": result.skin_concern.status,
            },
            "gradcam": {
                "disease": result.disease_gradcam,
                "concern": result.concern_gradcam,
            },
            "recommendation": None
            if result.recommendation is None
            else {
                "skin_type": result.recommendation.skin_type,
                "disease": result.recommendation.disease,
                "concern": result.recommendation.concern,
                "active_ingredients": result.recommendation.active_ingredients,
                "morning_routine": result.recommendation.morning_routine,
                "night_routine": result.recommendation.night_routine,
                "product_suggestions": result.recommendation.product_suggestions,
                "tips": result.recommendation.tips,
            },
        }
    )

