"""Audit a train/val/test image folder for data leakage.

Usage: python scripts/audit_split_leakage.py data/skin_type
Reports (a) byte-identical images shared between splits and (b) splits that contain
augmented copies of the same source image.
"""
import collections, itertools, sys
from split_utils import list_images, md5, base_name

root = sys.argv[1] if len(sys.argv) > 1 else "data/skin_type"
hashes, bases = collections.defaultdict(set), collections.defaultdict(set)
count = collections.Counter()
for split, cls, f, p in list_images(root):
    split = split.lower(); count[split] += 1
    hashes[split].add(md5(p)); bases[split].add((cls, base_name(f)))

print("Images per split:", dict(count))
for a, b in itertools.combinations(sorted(count), 2):
    dup = len(hashes[a] & hashes[b]); grp = len(bases[a] & bases[b])
    print(f"{a:>10} vs {b:<10} identical images: {dup:4d} | shared source images: {grp:4d} / {len(bases[b])}")
