# SkinLens - single-container deployment for Hugging Face Spaces (Docker SDK, free CPU hardware)
# Build context: a Space repository that contains this Dockerfile and the `app/` folder of the GitHub repo.
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates gnupg \
 && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
 && apt-get install -y --no-install-recommends nodejs \
 && rm -rf /var/lib/apt/lists/*

# Hugging Face Spaces run the container as user 1000
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user PATH=/home/user/.local/bin:$PATH
WORKDIR /home/user/app

# Python dependencies (cached layer)
COPY --chown=user app/python_backend/requirements.txt python_backend/requirements.txt
RUN pip install --no-cache-dir -r python_backend/requirements.txt

# Node dependencies (cached layer)
COPY --chown=user app/package.json app/package-lock.json ./
RUN npm ci --no-audit --no-fund

# Application code + production build of the web UI and the Express server
COPY --chown=user app/ ./
RUN npm run build

# Trained model weights are published as GitHub release assets (the repository must be public)
ARG RELEASE_URL=https://github.com/zehraeraslan/SkinLens/releases/download/v1.0.0
RUN mkdir -p python_backend/models \
 && for f in focal_finetuned_skin_model.keras best_hybrid_model.h5 skin_concern_final_model.keras; do \
      curl -fsSL -o "python_backend/models/$f" "$RELEASE_URL/$f"; \
    done

ENV NODE_ENV=production PORT=7860 BACKEND_PORT=8000 PYTHON_BACKEND_URL=http://127.0.0.1:8000 TF_CPP_MIN_LOG_LEVEL=2
EXPOSE 7860
CMD ["bash", "start.sh"]
