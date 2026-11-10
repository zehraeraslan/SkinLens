"""Download trained model files into ./models (set BASE_URL to your GitHub Release or Hugging Face URL)."""
import pathlib, urllib.request

BASE_URL = "https://github.com/YOUR_USERNAME/SkinLens/releases/download/v1.0.0"
FILES = [
    "focal_finetuned_skin_model.keras",
    "best_hybrid_model.h5",
    "skin_concern_final_model.keras",
]

dest = pathlib.Path(__file__).resolve().parent.parent / "models"
dest.mkdir(exist_ok=True)
for name in FILES:
    target = dest / name
    if target.exists():
        print(f"✔ {name} already present"); continue
    print(f"↓ {name}")
    urllib.request.urlretrieve(f"{BASE_URL}/{name}", target)
print("Done.")
