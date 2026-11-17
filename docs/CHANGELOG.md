# Changelog

## Unreleased — import of the web application (Nov 2026)
The application was prototyped on Replit and imported into this repository. While preparing it for public deployment the following issues were found and fixed:

- **Disease class order (critical).** The inference service listed the disease classes as `Acne, Atopic Dermatitis, benign_lesion, Melanoma, Tinea…`, whereas the model outputs follow the alphabetical order of the training folders (`Acne, Atopic Dermatitis, Melanoma, Tinea Ringworm Candidiasis, benign_lesion`). Labels of the last three classes were therefore shifted. Fixed in `python_backend/app/config.py`.
- **Grad-CAM for the concern model** silently failed (nested EfficientNet backbone) and returned no heatmap; it now uses a dedicated nested-backbone implementation.
- **Preprocessing parity.** Image resizing now matches the training pipelines (nearest-neighbour for the skin type and disease models, bilinear for the concern model).
- **Privacy.** The Express server stored every analysis, including the uploaded photograph, in memory and exposed the 20 most recent ones through `GET /api/analyses`. Storage and these endpoints were removed.
- Removed an unused mock inference module that generated random predictions.
- UI/About text said the models were EfficientNetV2B0; corrected (DenseNet121 for skin type and disease, EfficientNetB0 for concerns) and the facial/non-facial training-data limitation was documented.
- Configurable model directory and CORS origins; `requirements.txt` replaces the Replit `pyproject.toml`; Replit-specific files and the hard-coded `/home/runner/...` path were removed.
