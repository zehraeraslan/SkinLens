"""Evaluate the disease model on the test set — overall AND on a leakage-free subset.

A test image is "leaked" if a byte-identical file exists in train or valid.

Usage:
    python scripts/evaluate_skin_disease.py \
        --data ~/PycharmProjects/turker/final_dataset \
        --model models/focal_finetuned_skin_model.keras
"""
import argparse, collections, hashlib, os
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
import numpy as np
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix

ap = argparse.ArgumentParser()
ap.add_argument("--data", required=True)
ap.add_argument("--model", required=True)
a = ap.parse_args()

EXT = (".jpg", ".jpeg", ".png", ".jfif", ".webp")
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
classes = sorted(d for d in os.listdir(os.path.join(a.data, "train")) if os.path.isdir(os.path.join(a.data, "train", d)))
print("Class order (same as Keras flow_from_directory):", classes)

def files(split):
    out = []
    for i, c in enumerate(classes):
        d = os.path.join(a.data, split, c)
        out += [(os.path.join(d, f), i) for f in sorted(os.listdir(d)) if f.lower().endswith(EXT)]
    return out

test = files("test")
other = {}                                   # hash -> set(class) for train + valid
for split in ("train", "valid"):
    for p, y in files(split):
        other.setdefault(md5(p), set()).add(y)

leak = np.array([md5(p) in other for p, _ in test])
y_true = np.array([y for _, y in test])
conflict = sum(1 for (p, y), l in zip(test, leak) if l and y not in other[md5(p)])
print(f"Test images: {len(test)} | identical to train/valid: {leak.sum()} ({100*leak.mean():.1f} %) | "
      f"same image but different label: {conflict}")

model = tf.keras.models.load_model(a.model, compile=False)
X = np.stack([tf.keras.utils.img_to_array(tf.keras.utils.load_img(p, target_size=(224, 224))) for p, _ in test]) / 255.0
pred = model.predict(X, batch_size=32, verbose=0).argmax(1)

def report(title, m):
    print(f"\n===== {title} (n={m.sum()}) | accuracy {(pred[m] == y_true[m]).mean():.4f}")
    labels = [i for i in range(len(classes)) if (y_true[m] == i).any()]
    print(classification_report(y_true[m], pred[m], labels=labels, target_names=[classes[i] for i in labels], digits=2, zero_division=0))

report("ALL test images", np.ones(len(test), bool))
report("CLEAN test images (not in train/valid)", ~leak)
print("\nLeaked images accuracy: %.4f (n=%d)" % ((pred[leak] == y_true[leak]).mean(), leak.sum()) if leak.any() else "\nNo leaked images")
print("\nLeaked per class:", {classes[i]: int(((y_true == i) & leak).sum()) for i in range(len(classes))})
print("Confusion matrix (clean subset):\n", confusion_matrix(y_true[~leak], pred[~leak], labels=range(len(classes))))
