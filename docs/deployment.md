# Deployment

## 1. Static demo on GitHub Pages (free, always on) — recommended for the portfolio
`.github/workflows/pages.yml` builds the web UI in *demo mode* (`VITE_DEMO=true`) and publishes it. Demo mode replaces the API call with pre-computed model outputs for one sample image (`app/client/public/demo/*.json`), disables uploads and shows a banner.

Setup (once):
1. Repository → **Settings → Pages → Build and deployment → Source: GitHub Actions**.
2. Push to `main` (or run the workflow from the **Actions** tab). After about two minutes the site is live at `https://<user>.github.io/SkinLens/`.

Use your own sample photo: start the app locally and run `python scripts/make_demo_data.py my_photo.jpg`, then commit the changed files in `app/client/public/demo/`.

## 2. Live inference (real uploads) — options
The application needs about 2–4 GB of RAM (TensorFlow + three models) and a container host.

| Option | Cost | Notes |
|---|---|---|
| **Run locally** | free | `docs`/README *Getting Started*; ideal for demos and interviews |
| **Hugging Face Space (Docker)** | **paid** since mid-2026 | New accounts see the Docker SDK marked *Paid*; `deploy/huggingface/` contains a ready Dockerfile if you have a plan |
| **Google Cloud Run** | free tier (2 M requests, limited CPU-seconds) but needs a billing account | Use `deploy/huggingface/Dockerfile` with the repository root as build context; set max instances to 1 and a budget alert |
| Render / Koyeb free web services | free | 512 MB RAM — too small for TensorFlow with three models |

Uploaded images are processed in memory and are never stored.
