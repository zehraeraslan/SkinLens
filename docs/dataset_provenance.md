# Disease dataset — reconstructed provenance

No build log was kept. Everything below is **reconstructed** from (a) the data-preparation scripts, (b) a file inventory of `final_dataset` (file names, sizes, resolutions, MD5, timestamps; `scripts/dataset_inventory.py`) and (c) the evaluation in `scripts/evaluate_skin_disease.py`. Items marked *inferred* still need confirmation from the original download pages.

## Build facts (measured)
- `final_dataset` was generated in a single run on **2026‑02‑17, 14:19–14:23** (file timestamps); the deployed model file is dated 2026‑02‑19.
- Recipe (`final_dataset_builder.py`): pool source train/valid/test → merge *Benign keratosis* + *Melanocytic nevus* → `benign_lesion` (4,500) → random 80/10/10 split per class (seed 42) → train-only augmentation.
- **Melanoma:** 469 original training images, 1,348 augmented copies (`_aug0`–`_aug3`, ×4 per image, ≈337 per index). 338 of the 469 originals received copies; 131 did not (not explained by the scripts).
- **Tinea / other classes:** no augmentation (Tinea 880 = 80 % of 1,101).
- No de-duplication before the split.

## Duplicates (original images, byte-identical MD5)
| Class | Files | Unique | Duplicates |
|---|---|---|---|
| Acne | 2,958 | 2,446 | 17.3 % |
| Atopic Dermatitis | 5,136 | 2,764 | **46.2 %** |
| Melanoma | 587 | 561 | 4.4 % |
| Tinea Ringworm Candidiasis | 1,101 | 1,058 | 3.9 % |
| benign_lesion | 4,500 | 4,293 | 4.6 % |
| **Total** | **14,282** | **≈ 11,120** | |

## Sources (inferred from file names and image sizes)
| Class | Evidence | Likely source |
|---|---|---|
| Melanoma | 100 % `ISIC_<id>` names; median 3008×2000 px (up to 4288×2848) | ISIC archive (dermoscopy) |
| benign_lesion | ≈ 78 % `ISIC_<id>` (nevus / benign keratosis), ≈ 22 % clinical names such as `seborrheic-keratoses-*`, `skin-tags-polyps-*`, `keratoacanthoma-*` | ISIC + DermNet-style clinical photos |
| Acne | `acne-*`, `rosacea-*`, `perioral-dermatitis-*`, `hidradenitis-suppurativa-*`, and **998 files named `pigmentation_*`**; median ≈ 720×474 px | DermNet-style category "Acne and Rosacea" + other — *to be confirmed* |
| Atopic Dermatitis | `eczema-*`, `lichen-simplex-chronicus-*`, `stasis-dermatitis-*`, numeric / `IMG` names; median ≈ 720×477 px | DermNet-style category "Atopic Dermatitis / Eczema" |
| Tinea Ringworm Candidiasis | `tinea-versicolor/groin/body/foot-webs/hand-dorsum/face-*`; median ≈ 720×478 px | DermNet-style category "Tinea, Ringworm, Candidiasis and other fungal infections" |

## Consequences for the thesis
1. **The images are not facial photographs.** Melanoma/benign images are ISIC dermoscopy; the other classes are clinical photographs of many body sites (hand, foot, groin, …). The disease model therefore has **not been validated on facial photos**, which is the intended input of the app.
2. **Source and diagnosis are confounded.** Melanoma (and most benign images) come from ISIC dermoscopy, the other three classes from clinical photography. On the clean test subset 0 of 56 Melanoma images were confused with Acne / Atopic Dermatitis / Tinea; all Melanoma errors were with `benign_lesion`. Part of the 88 % accuracy is likely image-source recognition rather than disease recognition.
3. **Class labels are umbrella categories** (e.g. "Acne" includes rosacea and perioral dermatitis; "Atopic Dermatitis" includes stasis dermatitis and lichen simplex chronicus), not single diagnoses.

## To confirm
- Open `pigmentation_*` images in `train/Acne` and check whether they really show acne.
- Identify the original dataset pages (browser history, Kaggle) and record names, URLs and licences. DermNet-derived images carry their own licence terms; images are **not** redistributed in this repository.
