"""Rebuild the disease dataset WITHOUT train/test leakage.

Reads an existing final_dataset, ignores augmented copies (*_aug<N>.jpg), pools every original image,
removes byte-identical duplicates (and images whose duplicates carry different labels), groups
images that share a source name, splits whole groups 80/10/10 per class, and optionally augments
the TRAIN split only.

Usage:
  python scripts/build_clean_disease_dataset.py --src final_dataset --dst final_dataset_clean --seed 42
  python scripts/build_clean_disease_dataset.py --src final_dataset --dst final_dataset_clean --augment Melanoma=3
"""
import argparse, collections, hashlib, os, random, re, shutil

ap = argparse.ArgumentParser()
ap.add_argument("--src", required=True); ap.add_argument("--dst", required=True)
ap.add_argument("--ratio", nargs=3, type=float, default=[0.8, 0.1, 0.1])
ap.add_argument("--seed", type=int, default=42)
ap.add_argument("--augment", nargs="*", default=[], help='e.g. Melanoma=3 "Tinea Ringworm Candidiasis"=1')
a = ap.parse_args()
EXT = (".jpg", ".jpeg", ".png", ".jfif")
AUG = re.compile(r"_aug\d+\.[a-z]+$", re.I)

def md5(p):
    with open(p, "rb") as f: return hashlib.md5(f.read()).hexdigest()

def stem(name):                       # 'train_ISIC_001.jpg' -> 'ISIC_001'
    n = os.path.splitext(name)[0]
    n = re.sub(r"^(train|valid|test)_", "", n)
    n = re.sub(r"^(Benign keratosis|Melanocytic nevus)_", "", n)
    return re.sub(r"^(train|valid|test)_", "", n)

# 1. pool originals ---------------------------------------------------------
items, skipped_aug = [], 0
for split in ("train", "valid", "test"):
    sp = os.path.join(a.src, split)
    for cls in sorted(os.listdir(sp)):
        cd = os.path.join(sp, cls)
        if not os.path.isdir(cd): continue
        for f in sorted(os.listdir(cd)):
            if not f.lower().endswith(EXT): continue
            if AUG.search(f): skipped_aug += 1; continue
            items.append((cls, f, os.path.join(cd, f)))
print(f"Originals: {len(items)} | augmented copies ignored: {skipped_aug}")

# 2. drop duplicates / label conflicts -------------------------------------------
by_hash = collections.defaultdict(list)
for it in items: by_hash[md5(it[2])].append(it)
unique, dup_removed, conflicts = [], 0, 0
for h, group in by_hash.items():
    if len({g[0] for g in group}) > 1: conflicts += len(group); continue    # same image, different labels
    unique.append(group[0]); dup_removed += len(group) - 1
print(f"Duplicates removed: {dup_removed} | images dropped for conflicting labels: {conflicts} | unique kept: {len(unique)}")

# 3. group by source name (union-find on stem) ----------------------------------------
parent = {}
def find(x):
    parent.setdefault(x, x)
    while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
    return x
for cls, f, p in unique: find((cls, stem(f)))
groups = collections.defaultdict(lambda: collections.defaultdict(list))
for cls, f, p in unique: groups[cls][find((cls, stem(f)))].append((f, p))

# 4. group-wise stratified split ---------------------------------------------------------
rng = random.Random(a.seed); names = ["train", "valid", "test"]
if os.path.exists(a.dst): raise SystemExit(f"{a.dst} already exists - remove it or choose another --dst")
stats = collections.defaultdict(collections.Counter)
for cls, gs in groups.items():
    keys = list(gs); rng.shuffle(keys)
    total = sum(len(gs[k]) for k in keys); target = [r * total for r in a.ratio]; filled = [0, 0, 0]
    for k in keys:
        i = max(range(3), key=lambda j: target[j] - filled[j])
        out = os.path.join(a.dst, names[i], cls); os.makedirs(out, exist_ok=True)
        for f, p in gs[k]: shutil.copy2(p, os.path.join(out, f))
        filled[i] += len(gs[k]); stats[names[i]][cls] += len(gs[k])

# 5. optional augmentation of TRAIN only -----------------------------------------------------
if a.augment:
    import cv2, albumentations as A
    pipe = A.Compose([A.HorizontalFlip(p=0.5), A.Rotate(limit=20, p=0.7), A.RandomBrightnessContrast(p=0.4),
                      A.Affine(scale=(0.95, 1.05), translate_percent=0.05, p=0.3), A.GaussNoise(p=0.2)])
    for spec in a.augment:
        cls, m = spec.rsplit("=", 1); folder = os.path.join(a.dst, "train", cls)
        for f in sorted(os.listdir(folder)):
            im = cv2.imread(os.path.join(folder, f))
            if im is None: continue
            im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            for i in range(int(m)):
                out = cv2.cvtColor(pipe(image=im)["image"], cv2.COLOR_RGB2BGR)
                cv2.imwrite(os.path.join(folder, f"{os.path.splitext(f)[0]}_aug{i}.jpg"), out); stats["train"][cls] += 1

print("\nResult:")
for n in names: print(f"  {n:<6}", dict(stats[n]), "total", sum(stats[n].values()))
print("\nNext: python scripts/audit_split_leakage.py", a.dst, "(identical images must be 0 for every pair)")
