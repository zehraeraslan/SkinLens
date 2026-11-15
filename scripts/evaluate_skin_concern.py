"""Evaluate the skin concern model with the SAME preprocessing as training (bilinear resize via
image_dataset_from_directory) overall and on a leakage-free subset.

Usage: python scripts/evaluate_skin_concern.py --data data/skin_concern --model models/skin_concern_final_model.keras
"""
import argparse, os
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
import numpy as np, tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
from split_utils import base_name, md5

ap = argparse.ArgumentParser(); ap.add_argument("--data", required=True); ap.add_argument("--model", required=True); a = ap.parse_args()
ds = tf.keras.utils.image_dataset_from_directory(os.path.join(a.data, "test"), image_size=(224, 224), batch_size=32, shuffle=False, label_mode="int")
classes, paths = ds.class_names, ds.file_paths
y = np.concatenate([l for _, l in ds])
model = tf.keras.models.load_model(a.model, compile=False)
P = model.predict(ds, verbose=0); pred = P.argmax(1)
print("Accuracy", round(float((pred == y).mean()), 4), "n =", len(y))
print(classification_report(y, pred, target_names=classes, digits=2)); print(confusion_matrix(y, pred))
tr_b, tr_h = set(), set()
for c in classes:
    for f in os.listdir(os.path.join(a.data, "train", c)):
        tr_b.add((c, base_name(f))); tr_h.add(md5(os.path.join(a.data, "train", c, f)))
clean = np.array([(classes[i], base_name(os.path.basename(p))) not in tr_b and md5(p) not in tr_h for p, i in zip(paths, y)])
print("Leakage-free subset: n =", clean.sum(), "accuracy", round(float((pred[clean] == y[clean]).mean()), 4), "| others:", round(float((pred[~clean] == y[~clean]).mean()), 4))
conf = P.max(1); print("Mean confidence", round(float(conf.mean()), 3), "| below 0.70:", int((conf < 0.7).sum()), "| accuracy of the rest:", round(float((pred[conf >= 0.7] == y[conf >= 0.7]).mean()), 4))
