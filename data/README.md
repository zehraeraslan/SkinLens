# Datasets

Image data is **not stored in this repository** (size, licensing, and privacy of face photographs). Expected local layout:

## Skin Type (2,388 images)
```
skin_type/{train,validation,test}/{Dry,Normal,Oily,Sensitive}/
```
| Split | Dry | Normal | Oily | Sensitive | Total |
|---|---|---|---|---|---|
| train | 609 | 360 | 589 | 360 | 1,918 |
| validation | 80 | 45 | 65 | 45 | 235 |
| test | 80 | 45 | 65 | 45 | 235 |

Sources: Kaggle MSC-6 and other web/Roboflow images. About half of the files (1,200 / 2,388) are offline augmentations (flip / rotate).

> ⚠️ **Data-leakage warning.** The original split was made *after* offline augmentation. An audit (`scripts/audit_split_leakage.py`) found **63 byte-identical images shared by train and test**, and 80 of 156 test source images also appear (augmented) in train. Use `scripts/make_clean_split.py` to build a leakage-free split (group-wise by source image) and re-evaluate.

## Skin Disease (15,630 images)
```
final_dataset/{train,valid,test}/{Acne,Atopic Dermatitis,Melanoma,Tinea Ringworm Candidiasis,benign_lesion}/
```
Measured counts:

| Class | train | valid | test |
|---|---|---|---|
| Acne | 2,366 | 296 | 296 |
| Atopic Dermatitis | 4,108 | 514 | 514 |
| Melanoma | 1,817 | 59 | 59 |
| Tinea Ringworm Candidiasis | 880 | 110 | 111 |
| benign_lesion | 3,600 | 450 | 450 |
| **Total** | **12,771** | **1,429** | **1,430** |

Sources: ISIC archive (augmented subsets) and public dermatology repositories. Images are 224×224 RGB.

Provenance, duplicate statistics and source analysis: see [../docs/dataset_provenance.md](../docs/dataset_provenance.md).

How `final_dataset` was built (`training/skin_disease/data_preparation/final_dataset_builder.py`): source train/valid/test pooled → *Benign keratosis* + *Melanocytic nevus* merged into `benign_lesion` and undersampled to 4,500 → random 80/10/10 split per class (seed 42) → train-only augmentation (flip, rotate ±20°, brightness/contrast, affine, Gaussian noise). Class totals match this recipe exactly (e.g. Tinea 880/110/111 = 80/10/10 of 1,101, i.e. Tinea was **not** augmented in the final dataset, Melanoma was). No de-duplication was applied before the split.

> ⚠️ **Data-leakage warning.** `scripts/audit_split_leakage.py` found **483 of the 1,430 test images (33.8 %) byte-identical to training images**, 72 test images identical to validation images and 488 validation images identical to training images. Melanoma is also 14 % of train but only 4 % of valid/test, i.e. the training set contains duplicated/augmented Melanoma images. The reported 87.97 % test accuracy is therefore optimistic. Including validation, 547 test images (38.3 %) have an identical twin in train or valid; accuracy on the other 883 is 85.96 % (see `docs/model-card.md`). `scripts/evaluate_skin_disease.py` reproduces this, and rebuild the split with `scripts/make_clean_split.py` before retraining.

## Skin Concern (6,247 images)
```
skin_concern/{train,valid,test}/{acne,Blackheads,pores,wrinkles}/
```
| Split | acne | Blackheads | pores | wrinkles | Total |
|---|---|---|---|---|---|
| train | 1,116 | 791 | 1,304 | 1,586 | 4,797 |
| valid | 108 | 202 | 163 | 206 | 679 |
| test | 217 | 199 | 165 | 190 | 771 |

> Leakage audit: 5 test images are byte-identical to train images and 67 of 1,129 test source images also occur in train (Roboflow augmentations of one source). Validation overlaps train even more (67 of 208 sources). Test accuracy is therefore slightly optimistic (≈ 91 % on the leakage-free subset vs 92.7 %).

Several images carry Roboflow-style names (`*.rf.<hash>.jpg`); respect the original dataset licences when redistributing.
