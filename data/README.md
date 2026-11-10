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
skin_disease/{train,val,test}/{Acne,Atopic_Dermatitis,Benign_Lesion,Melanoma,Tinea_Ringworm_Candidiasis}/
```
Split: train 12,771 · validation 1,429 · test 1,430. Sources: ISIC archive (augmented subsets) and public dermatology repositories.

Class counts (test measured; train derived from the balanced class weights in the thesis):

| Class | Train (≈) | Train % | Test | Test % |
|---|---|---|---|---|
| Acne | 2,367 | 18.5 | 296 | 20.7 |
| Atopic Dermatitis | 4,106 | 32.2 | 514 | 35.9 |
| Melanoma | 1,816 | **14.2** | 59 | **4.1** |
| Tinea/Ringworm/Candidiasis | 879 | 6.9 | 111 | 7.8 |
| Benign Lesion | 3,597 | 28.2 | 450 | 31.5 |

> ⚠️ Melanoma is 14 % of train but only 4 % of test, while all other classes keep similar shares. This suggests the training set contains augmented/oversampled Melanoma images and is not a pure stratified split. Run `scripts/audit_split_leakage.py` on this dataset before trusting the reported 87.97 %.

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
