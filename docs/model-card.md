# Model Card — SkinLens

## Intended use
Educational, preliminary screening from a single facial/skin photograph. **Not** for diagnosis or clinical decisions.

## Disease model (DenseNet121, focal-loss fine-tuned)
> ⚠️ **Evaluation caveat.** 547 of the 1,430 test images (38.3 %) are byte-identical to training or validation images (`scripts/evaluate_skin_disease.py`). The table below is the original, optimistic evaluation. On the 883 test images that do **not** occur in train/valid, accuracy is **85.96 %** (leaked images: 91.22 %). Near-duplicates are not detected, so this is still an upper bound.

| Class (clean subset, n = 883) | Precision | Recall | F1 | Support | Leaked (of 1,430-set) |
|---|---|---|---|---|---|
| Acne | 0.96 | 0.91 | 0.93 | 202 | 94 / 296 |
| Atopic Dermatitis | 0.65 | 0.94 | 0.77 | 97 | **417 / 514** |
| Melanoma | 0.62 | 0.52 | 0.56 | 56 | 3 / 59 |
| Tinea/Ringworm/Candidiasis | 0.88 | 0.61 | 0.72 | 106 | 5 / 111 |
| Benign Lesion | 0.91 | 0.92 | 0.92 | 422 | 28 / 450 |

Observations: 81 % of the Atopic Dermatitis test images are duplicates of training images, so the clean AD figures rest on only 97 images. Melanoma performance is unaffected by leakage (F1 0.56): 27 of 56 clean Melanoma images are classified as benign lesions and 18 benign lesions as Melanoma. 33 of 106 Tinea images are classified as Atopic Dermatitis.


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

> ⚠️ **Evaluation caveat (skin type).** The original split was made after offline augmentation: 65 of the 235 test images are byte-identical to training images (66 to training or validation) and 136 share a source file name with a training image. Measured with the training-time pipeline: accuracy 92.34 % on all 235 test images, **89.35 %** on the 169 images without an identical counterpart in train/valid, 84.2 % on the 95 images that also share no source name with train (no Sensitive images), 97.9 % on the remaining 140. A source-level re-split and retraining is recommended.

## Skin concern model (EfficientNetB0)
Test set n = 771 · Accuracy **93.77 %** · Macro F1 0.94 (measured on the supplied `skin_concern_final_model.keras` with `image_dataset_from_directory`, i.e. the training-time preprocessing).

| Class | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| Blackheads | 0.88 | 0.98 | 0.93 | 199 |
| acne | 0.99 | 0.92 | 0.95 | 217 |
| pores | 0.89 | 0.94 | 0.91 | 165 |
| wrinkles | 0.99 | 0.91 | 0.95 | 190 |

Main confusions: wrinkles → pores (15), acne → Blackheads (14), pores → Blackheads (10). Five test images are byte-identical to training images; on the 521 test images with no identical or same-source counterpart in train accuracy is 91.94 % (250 others: 97.6 %). Mean confidence 0.97; 27 of 771 predictions (3.5 %) fall below the 70 % threshold, accuracy of the rest 95.4 %.

## Limitations
- **Training images are not facial photographs.** The disease model was trained on ISIC dermoscopy images and clinical photographs of various body sites (see `docs/dataset_provenance.md`); behaviour on facial photos has not been evaluated.
- **Image source is confounded with diagnosis** (Melanoma ≈ ISIC dermoscopy, other classes ≈ clinical photos), so accuracy overstates disease-recognition ability.
- Melanoma F1 0.56 / recall 0.51 — below clinical screening standards; small test set (59).
- Datasets are small and may not represent all skin tones, ages or imaging conditions.
- Single standard photograph; no dermoscopy, patient history or multi-angle input.
- No prospective clinical validation.
- Normal vs. Oily skin types are visually similar (lower confidence ≈ 0.81 / 0.84).
