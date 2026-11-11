# Model Card — SkinLens

## Intended use
Educational, preliminary screening from a single facial/skin photograph. **Not** for diagnosis or clinical decisions.

## Disease model (DenseNet121, focal-loss fine-tuned)
> ⚠️ **Evaluation caveat.** 483 of the 1,430 test images (33.8 %) are byte-identical to training images (see `data/README.md`). The figures below were measured on the original split and are optimistic; a leakage-free re-evaluation is pending.

Architecture (verified from the model file): DenseNet121 (432 layers, 7.3 M params) → GAP → BatchNorm → Dense(256, ReLU) → Dropout(0.5) → Dense(5, softmax). In Stage 3 all layers are trainable.

Test set n = 1,430 · Accuracy **87.97 %** · Macro F1 0.79 · Weighted F1 0.88

| Class | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| Acne | 0.95 | 0.90 | 0.93 | 296 |
| Atopic Dermatitis | 0.89 | 0.93 | 0.91 | 514 |
| Melanoma | 0.61 | 0.51 | 0.56 | 59 |
| Tinea/Ringworm/Candidiasis | 0.73 | 0.62 | 0.67 | 111 |
| Benign Lesion | 0.89 | 0.92 | 0.90 | 450 |

| Stage | Epochs | Best val acc | Test acc |
|---|---|---|---|
| 1 – class weights | 26 | 79.50 % | 81.26 % |
| 2 – fine-tuning (last 60 layers) | 15 | 85.02 % | – |
| 3 – focal loss | 10 | 86.84 % | **87.97 %** |

## Skin type model (hybrid CNN + LBP)
Test set n = 235 · Accuracy **92 %** · Macro F1 0.93

| Class | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| Dry | 0.96 | 0.88 | 0.92 | 80 |
| Normal | 0.98 | 0.93 | 0.95 | 45 |
| Oily | 0.87 | 0.92 | 0.90 | 65 |
| Sensitive | 0.90 | 1.00 | 0.95 | 45 |

> ⚠️ **Evaluation caveat (skin type).** The reported 92 % was measured on the original split, which contains duplicate / augmented copies of training images (see `data/README.md`). On the subset of test images whose source image does not occur in train (n = 95, no Sensitive samples), the same model scored ≈ 86 %. A leakage-free re-split and retraining is recommended before claiming final performance.

## Skin concern model (EfficientNetB0)
Test set n = 771 · Accuracy **92.7 %** · Macro F1 0.93 (re-measured on the supplied `skin_concern_final_model.keras`, TensorFlow 2.21; not copied from a training log).

| Class | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| Blackheads | 0.86 | 0.98 | 0.92 | 199 |
| acne | 0.99 | 0.89 | 0.94 | 217 |
| pores | 0.88 | 0.94 | 0.91 | 165 |
| wrinkles | 0.99 | 0.89 | 0.94 | 190 |

Main confusions: acne → Blackheads (20), wrinkles → pores (17), pores → Blackheads (10). On test images whose source image is absent from train (n = 521) accuracy is 91.0 %. Mean confidence 0.97; 37 of 771 predictions fall below the 70 % threshold.

## Limitations
- Melanoma F1 0.56 / recall 0.51 — below clinical screening standards; small test set (59).
- Datasets are small and may not represent all skin tones, ages or imaging conditions.
- Single standard photograph; no dermoscopy, patient history or multi-angle input.
- No prospective clinical validation.
- Normal vs. Oily skin types are visually similar (lower confidence ≈ 0.81 / 0.84).
