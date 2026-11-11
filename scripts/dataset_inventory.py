"""Create a compact inventory (CSV) of every image under a folder - NO image content is stored.

Columns: path (relative), bytes, width, height, format, mode, md5, modified (UTC).
The CSV reveals duplicates, augmentation naming, file-name patterns (= sources) and image
sizes per class, which is enough to reconstruct how a dataset was built.

Usage:
    python scripts/dataset_inventory.py ~/PycharmProjects/turker/final_dataset inventory_final.zip
"""
import csv, datetime, hashlib, io, os, sys, zipfile

EXT = (".jpg", ".jpeg", ".png", ".jfif", ".webp", ".bmp", ".gif", ".tif", ".tiff")
root = os.path.expanduser(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else "inventory.zip"
if not os.path.isdir(root): sys.exit(f"Folder not found: {root}")
try:
    from PIL import Image, ImageFile
    ImageFile.LOAD_TRUNCATED_IMAGES = True
except ImportError:
    Image = None; print("Pillow not installed - width/height will be empty")

buf = io.StringIO(); w = csv.writer(buf)
w.writerow(["path", "bytes", "width", "height", "format", "mode", "md5", "modified_utc"])
n = 0
for dp, dn, fs in os.walk(root):
    dn[:] = [d for d in dn if not d.startswith(".")]
    for f in sorted(fs):
        if not f.lower().endswith(EXT): continue
        p = os.path.join(dp, f); st = os.stat(p)
        with open(p, "rb") as fh: h = hashlib.md5(fh.read()).hexdigest()
        wd = ht = fmt = mode = ""
        if Image:
            try:
                with Image.open(p) as im: wd, ht = im.size; fmt = im.format; mode = im.mode
            except Exception: fmt = "UNREADABLE"
        w.writerow([os.path.relpath(p, root), st.st_size, wd, ht, fmt, mode, h,
                    datetime.datetime.fromtimestamp(st.st_mtime, datetime.timezone.utc).strftime("%Y-%m-%d %H:%M")])
        n += 1
        if n % 2000 == 0: print(f"  {n} files...")
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z: z.writestr("inventory.csv", buf.getvalue())
print(f"Done: {n} images -> {out} ({os.path.getsize(out)/1024:.0f} KB). Upload this file to the chat.")
