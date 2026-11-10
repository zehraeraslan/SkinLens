# Skin Type Model — Hybrid DenseNet121 + LBP

| File | Purpose |
|---|---|
| `lbp_pipeline.py` | `extract_lbp_features` (uniform LBP, **P=24, R=3 → 26 bins**) and `HybridSkinGenerator` (dual-input Keras `Sequence`) |
| `hybrid_model.py` | `build_hybrid_model(num_classes)` |

## Architecture (as implemented)
- **CNN branch:** DenseNet121 (ImageNet, frozen) → GAP → BatchNorm → Dense(256, ReLU) → Dropout(0.4)
- **LBP branch:** 26-d histogram → Dense(64) → BatchNorm → Dropout(0.3) → Dense(32)
- **Fusion:** Concatenate → Dense(128) → BatchNorm → Dropout(0.4) → Softmax(4)
- Adam (lr 1e-4), categorical cross-entropy, batch 8, 30 epochs, best-val checkpoint (`best_hybrid_model.h5`)
- Training augmentation: h-flip, rotation ±20°, zoom ±10 %, brightness 0.9–1.1

## Reproduce
```bash
python scripts/audit_split_leakage.py data/skin_type          # check for leakage
python scripts/make_clean_split.py data/skin_type data/skin_type_clean
```

## Still to add (from the original project)
`train_prof.py` (training loop), `analiz.py` (test report), prediction script, confidence-analysis script.
