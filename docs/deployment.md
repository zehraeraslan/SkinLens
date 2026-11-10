# Deployment (free options)

## Recommended free setup
| Part | Platform | Why |
|---|---|---|
| FastAPI + TensorFlow backend | **Hugging Face Spaces** (Docker, CPU basic) | Free, generous RAM — TensorFlow/DenseNet needs more than most free web hosts offer |
| React frontend (+ Express proxy if needed) | **Vercel / Netlify / Cloudflare Pages** | Free static hosting, auto-deploy from GitHub |
| Model files | **GitHub Releases** or **Hugging Face Hub** | Avoid the 100 MB git limit |

Set the frontend's API base URL (`BACKEND_URL`) to the Space URL.

## Replit
Replit's free *Starter* plan allows 1 published project with limited credits; apps may go offline and always-on hosting needs a paid deployment. Fine for a demo; use the setup above for a permanent link.
