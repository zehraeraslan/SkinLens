# Uploading to GitHub — step by step

## 0. One-time setup
```bash
git config --global user.name  "Zehra Eraslan"
git config --global user.email "YOUR_GITHUB_EMAIL"
```
Create an **empty** repo on github.com → *New repository* → name `SkinLens`, Public, **no** README/licence/.gitignore (they already exist here).

## 1. Push with a clean history
```bash
cd SkinLens
git init -b main
git add LICENSE .gitignore CITATION.cff .env.example && git commit -m "chore: add licence, gitignore, citation"
git add README.md README.tr.md docs && git commit -m "docs: add README, architecture, model card, deployment guide"
git add data scripts && git commit -m "feat(data): dataset docs, leakage audit and clean-split scripts"
git add training/skin_type && git commit -m "feat(skin-type): hybrid DenseNet121 + LBP pipeline"
git add training/skin_concern && git commit -m "feat(skin-concern): EfficientNetB0 training and Grad-CAM"
git add training/skin_disease && git commit -m "feat(disease): three-stage DenseNet121 training"
git add backend frontend server notebooks models && git commit -m "chore: project skeleton"
git remote add origin https://github.com/YOUR_USERNAME/SkinLens.git
git push -u origin main
```

## 2. Model files → GitHub Release (not git)
Repo page → *Releases* → *Draft a new release* → tag `v1.0.0` → drag in `focal_finetuned_skin_model.keras`, `best_hybrid_model.h5`, `skin_concern_final_model.keras` (each < 2 GB) → *Publish*. Put the URL base into `scripts/download_models.py`.

## 3. Before every push — safety check
```bash
git status --short            # no .venv, .idea, .env, *.zip, images
git ls-files | xargs -I{} du -k "{}" | sort -n | tail -5   # nothing near 100 MB
grep -rniE "api[_-]?key|secret|token|password" --exclude-dir=.git . | head
```
