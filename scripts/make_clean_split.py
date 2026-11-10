"""Create a leakage-free train/val/test split.

All images from every split are pooled, exact duplicates are removed, images that derive from the
same source picture (flip/rotate/Roboflow copies) are grouped, and whole groups are assigned to a
single split (stratified per class). Evaluate on `test` only once, at the very end.

Usage: python scripts/make_clean_split.py data/skin_type data/skin_type_clean [--ratio 0.8 0.1 0.1] [--seed 42]
"""
import argparse, collections, os, random, shutil
from split_utils import list_images, md5, base_name

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("dst")
ap.add_argument("--ratio", nargs=3, type=float, default=[0.8, 0.1, 0.1])
ap.add_argument("--seed", type=int, default=42)
a = ap.parse_args()

# 1. pool, drop exact duplicates, group by source image (union-find over hash + base name)
parent = {}
def find(x):
    parent.setdefault(x, x)
    while parent[x] != x:
        parent[x] = parent[parent[x]]; x = parent[x]
    return x
def union(x, y): parent[find(x)] = find(y)

seen, items = set(), []
for _, cls, f, p in list_images(a.src):
    h = md5(p)
    if h in seen: continue
    seen.add(h); items.append((cls, f, p, h))
    union(("h", h), ("b", cls, base_name(f)))

groups = collections.defaultdict(lambda: collections.defaultdict(list))
for cls, f, p, h in items:
    groups[cls][find(("h", h))].append((f, p))

# 2. stratified, group-wise assignment
rng = random.Random(a.seed)
names = ["train", "validation", "test"]
stats = collections.defaultdict(collections.Counter)
for cls, gs in groups.items():
    keys = list(gs); rng.shuffle(keys)
    total = sum(len(gs[k]) for k in keys)
    targets = [r * total for r in a.ratio]; filled = [0, 0, 0]
    for k in keys:
        i = max(range(3), key=lambda j: targets[j] - filled[j])   # fill the split furthest below target
        out = os.path.join(a.dst, names[i], cls); os.makedirs(out, exist_ok=True)
        for f, p in gs[k]:
            shutil.copy2(p, os.path.join(out, f))
        filled[i] += len(gs[k]); stats[names[i]][cls] += len(gs[k])

for n in names: print(n, dict(stats[n]), "total", sum(stats[n].values()))
