# Models

Trained weights are **not committed to git** (size). Publish them as a **GitHub Release asset** or on **Hugging Face Hub**, then download into this folder.

| File | Model | Status |
|---|---|---|
| `best_skin_model.keras` | Disease – Stage 1 (class weights) | experiment |
| `finetuned_skin_model.keras` | Disease – Stage 2 (fine-tuning) | experiment |
| `focal_finetuned_skin_model.keras` | Disease – Stage 3 (focal loss) | **deployed** |
| `best_hybrid_model.h5` | Skin type – hybrid CNN + LBP | **deployed** |
| `skin_concern_final_model.keras` | Skin concern | **deployed** |

Download helper: `python scripts/download_models.py` (set the release URL inside the script).
