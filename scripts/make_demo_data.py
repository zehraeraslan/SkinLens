"""Regenerate the static-demo data (app/client/public/demo/*.json + sample.jpg) from your own image.

1. Start the full application locally (inference server + Express, see app/README.md).
2. python scripts/make_demo_data.py path/to/your_photo.jpg [--url http://localhost:5000]

The four JSON files are real model outputs (prediction, Grad-CAM, recommendations) for that image.
"""
import argparse, pathlib, shutil, requests

ap = argparse.ArgumentParser(); ap.add_argument("image"); ap.add_argument("--url", default="http://localhost:5000"); a = ap.parse_args()
out = pathlib.Path(__file__).resolve().parent.parent / "app" / "client" / "public" / "demo"
out.mkdir(parents=True, exist_ok=True)
shutil.copy(a.image, out / "sample.jpg")
for mode in ("full", "skin_type", "disease", "concern"):
    with open(a.image, "rb") as f:
        r = requests.post(f"{a.url}/api/analyze", files={"image": ("sample.jpg", f, "image/jpeg")}, data={"mode": mode}, timeout=300)
    r.raise_for_status()
    (out / f"{mode}.json").write_text(r.text)
    print("wrote", out / f"{mode}.json")
