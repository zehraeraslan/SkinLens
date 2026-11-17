from __future__ import annotations

from typing import Any, Dict

import tensorflow as tf

from app.config import get_settings


settings = get_settings()


class ModelRegistry:
    """
    Singleton-style registry that lazily loads and stores all models.
    """

    _instance: "ModelRegistry | None" = None

    def __new__(cls) -> "ModelRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return
        self._models: Dict[str, tf.keras.Model] = {}
        self._initialized = True

    def load_models(self) -> None:
        if self._models:
            return

        # Skin type hybrid model (image + LBP)
        self._models["skin_type"] = tf.keras.models.load_model(
            settings.skin_type_model_path
        )

        # Disease model with custom loss in training – load without compile
        self._models["skin_disease"] = tf.keras.models.load_model(
            settings.skin_disease_model_path, compile=False
        )

        # Concern model (EfficientNet-based classifier)
        self._models["skin_concern"] = tf.keras.models.load_model(
            settings.skin_concern_model_path, compile=False
        )

    def get(self, key: str) -> tf.keras.Model:
        if not self._models:
            self.load_models()
        return self._models[key]

    @property
    def skin_type_model(self) -> tf.keras.Model:
        return self.get("skin_type")

    @property
    def skin_disease_model(self) -> tf.keras.Model:
        return self.get("skin_disease")

    @property
    def skin_concern_model(self) -> tf.keras.Model:
        return self.get("skin_concern")


def get_model_registry() -> ModelRegistry:
    return ModelRegistry()

