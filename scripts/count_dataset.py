"""Print image counts per split/class (works on macOS, Linux, Windows).

Usage: python scripts/count_dataset.py /path/to/final_dataset
"""
import os, sys

root = sys.argv[1] if len(sys.argv) > 1 else "final_dataset"
if not os.path.isdir(root):
    sys.exit(f"Folder not found: {root}\nTip (macOS/Linux): find ~ -maxdepth 5 -type d -name final_dataset 2>/dev/null")

EXT = (".jpg", ".jpeg", ".png", ".jfif", ".webp")
totals = {}
for split in sorted(os.listdir(root)):
    sp = os.path.join(root, split)
    if not os.path.isdir(sp): continue
    print(f"\n[{split}]")
    for cls in sorted(os.listdir(sp)):
        cd = os.path.join(sp, cls)
        if not os.path.isdir(cd): continue
        n = sum(f.lower().endswith(EXT) for f in os.listdir(cd))
        totals[split] = totals.get(split, 0) + n
        print(f"  {cls:<35}{n:>7}")
print("\nTotals:", totals)
