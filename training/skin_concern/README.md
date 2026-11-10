# Skin Concern Model — EfficientNetB0 (4-class)

Classes (Keras alphabetical order): `Blackheads, acne, pores, wrinkles` — **keep this order at inference**.

| File | Purpose |
|---|---|
| `train_efficientnetb0.py` | Stage 1: frozen EfficientNetB0 + GAP → BN → Dense(256, swish) → Dropout(0.4) → Softmax, Adam 1e-3, 15 epochs, balanced class weights. Stage 2: unfreeze last 30 backbone layers, Adam 1e-5, 10 epochs. Saves `skin_concern_final_model.keras` |
| `gradcam_concern.py` | Grad-CAM on the EfficientNet feature map: `python gradcam_concern.py image.jpg` |

Input: 224×224 RGB, `efficientnet.preprocess_input` is part of the model; augmentation (flip, rotation 0.1, zoom 0.1) is inside the model graph.

> The checkpoint file was renamed to `best_concern_checkpoint.keras` (the original `best_skin_model.keras` collided with the disease Stage-1 model).

## Other experiments supplied (not deployed)
| File | Architecture |
|---|---|
| `concern_baseline_final.keras` | EfficientNetB0 baseline |
| `best_final_model.keras` | EfficientNetV2-B0 |
| `best_hybrid_concern_model.keras` | DenseNet121 + LBP (two inputs) |

Evaluation: `python scripts/evaluate_skin_concern.py` (needs `data/skin_concern` and `models/`).
