# Free deployment (Hugging Face Spaces)

The whole application (Express + FastAPI + TensorFlow) runs in **one Docker container** on a free Hugging Face Space (CPU basic: 2 vCPU, 16 GB RAM). The free tier sleeps after about 48 h of inactivity and the first request after sleeping takes roughly a minute while the models load — fine for a portfolio demo.

## Prerequisites
1. The GitHub repository is **public** and release `v1.0.0` contains the three model files (the Docker build downloads them).
2. A free account on huggingface.co and an access token with *write* permission (Settings → Access Tokens).

## Steps
1. Create the Space: huggingface.co → *New* → *Space* → name `skinlens`, SDK **Docker** (blank template), hardware **CPU basic (free)**, visibility Public.
2. Assemble and push the Space repository:
   ```bash
   git clone https://huggingface.co/spaces/<HF_USERNAME>/skinlens space && cd space
   cp -R ~/Downloads/SkinLens/app ./app
   cp ~/Downloads/SkinLens/deploy/huggingface/Dockerfile ~/Downloads/SkinLens/deploy/huggingface/README.md .
   rm -rf app/node_modules app/dist
   git add . && git commit -m "Deploy SkinLens" && git push
   ```
   (When asked for a password, paste the access token.)
3. Watch *Logs* on the Space page: the build takes about 8–12 minutes. When the status turns **Running**, open the Space URL.
4. Put the URL into the *Live Demo* section of the README.

## Notes
- Uploaded images are processed in memory and are not stored.
- To pin different model files, change `RELEASE_URL` in the Dockerfile.
- Replit is not needed for hosting; the Replit-specific files were removed from the repository.
