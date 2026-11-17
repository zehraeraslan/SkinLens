import os
from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = "SkinLens Platform"
    api_prefix: str = "/api"

    # Paths
    base_dir: Path = Path(__file__).resolve().parents[1]
    models_dir: Path = Path(os.getenv("MODEL_DIR", str(base_dir / "models")))

    # Model filenames
    skin_type_model_path: Path = models_dir / "best_hybrid_model.h5"
    skin_disease_model_path: Path = models_dir / "focal_finetuned_skin_model.keras"
    skin_concern_model_path: Path = models_dir / "skin_concern_final_model.keras"

    # Class definitions. They MUST match the output order of the trained models, which is the
    # alphabetical (ASCII) order of the training folder names used by Keras
    # (flow_from_directory / image_dataset_from_directory): upper-case names sort before lower-case.
    skin_type_classes: list[str] = ["Dry", "Normal", "Oily", "Sensitive"]
    skin_disease_classes: list[str] = [
        "Acne",
        "Atopic Dermatitis",
        "Melanoma",
        "Tinea Ringworm Candidiasis",
        "benign_lesion",
    ]
    skin_concern_classes: list[str] = ["Blackheads", "acne", "pores", "wrinkles"]

    # Reliability threshold
    reliability_threshold: float = 0.70

    # Upload & security
    max_upload_size_mb: int = 8
    allowed_content_types: tuple[str, ...] = (
        "image/jpeg",
        "image/png",
        "image/jpg",
    )

    # Comma-separated list of allowed CORS origins ("*" = any origin)
    cors_origins: str = os.getenv("CORS_ORIGINS", "*")

    # Simple in-memory rate limiting
    rate_limit_requests: int = 15
    rate_limit_window_seconds: int = 60


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

