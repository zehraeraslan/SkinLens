# SkinLens web application

Three-tier application: **React + TypeScript** UI → **Express.js** gateway (serves the UI, validates uploads, proxies `/api/analyze`) → **FastAPI + TensorFlow** inference server (three models, Grad-CAM, rule-based recommendations).

```
app/
├── client/            React 18 + Vite + Tailwind + shadcn/ui + Recharts + Framer Motion
├── server/            Express gateway (multer in-memory upload, label normalisation, static hosting)
├── shared/            Types / schemas shared by client and server
├── script/build.ts    Production build (Vite client + esbuild server bundle)
├── python_backend/    FastAPI inference service
│   └── app/{api,core,services,utils}
└── start.sh           Starts both servers (used by the Docker image)
```

## Run locally

1. Download the trained models from the repository's GitHub release into `python_backend/models/`:
   `python ../scripts/download_models.py` (files: `focal_finetuned_skin_model.keras`, `best_hybrid_model.h5`, `skin_concern_final_model.keras`).
2. Inference server (Python 3.11+):
   ```bash
   cd python_backend
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ./run.sh                     # http://localhost:8000  (GET /health)
   ```
3. Web server (Node 20+), in a second terminal:
   ```bash
   npm install
   npm run dev                  # http://localhost:5000
   ```
   Production build: `npm run build && npm start`.

## API

`POST /api/analyze` — `multipart/form-data`, field `image` (JPEG/PNG, ≤ 8 MB) and `mode` (`full`, `skin_type`, `disease`, `concern`).
Returns predictions with all class probabilities, a `SUCCESS` / `LOW_CONFIDENCE_RETRY` status (70 % threshold), Grad-CAM overlays (base64 JPEG) and skincare recommendations. `GET /api/health` reports the state of the inference server.

## Privacy by design
Uploaded photographs are handled in memory only: the Express server does not write them to disk or keep them after the response, and no analysis history is exposed.

## Environment variables
See [`../.env.example`](../.env.example). Model class order is defined in `python_backend/app/config.py` and **must** equal the alphabetical (ASCII) order of the training folders (see `../docs/CHANGELOG.md`).
