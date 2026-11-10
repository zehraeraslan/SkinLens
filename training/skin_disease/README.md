# Skin Disease Model — DenseNet121, 3-stage training

Run in order (expects `final_dataset/{train,valid,test}/<class>/`):

| Step | Script | Input → Output | Key settings |
|---|---|---|---|
| 1 | `01_train_head.py` | ImageNet DenseNet121 → `best_skin_model.keras` | backbone frozen; GAP → BN → Dense(256, ReLU) → Dropout(0.5) → Softmax(5); Adam 1e-4; balanced class weights; ≤30 epochs; EarlyStopping (val_loss, patience 8); ReduceLROnPlateau (×0.2, patience 3); live augmentation (rot 20°, shifts 0.1, shear 0.1, zoom 0.1, h-flip) |
| 2 | `02_finetune.py` | → `finetuned_skin_model.keras` | last 60 layers trainable; Adam 1e-5; categorical CE; 15 epochs |
| 3 | `03_focal_loss.py` | → `focal_finetuned_skin_model.keras` (**deployed**) | **all 432 layers trainable**; focal loss (γ=2, α=0.25); Adam 1e-5; 10 epochs |

Notes
- `02_finetune.py` had a stray `X` after `train_gen,` (syntax error) — fixed.
- Class indices are alphabetical folder names; inference code must use the same order.
- Loading the final model for inference: `load_model(path, compile=False)`; for evaluation pass `custom_objects={'loss': focal_loss(2, 0.25)}`.
- In the focal loss α is a single scalar, so it rescales the loss but does **not** re-balance classes.
