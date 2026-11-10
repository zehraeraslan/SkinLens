"""Shared helpers: find the *source image* behind augmented copies (flip / rotate / Roboflow hash)."""
import hashlib, os, re

IMG_EXT = (".jpg", ".jpeg", ".png")

def md5(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def base_name(filename):
    """'images (10)_resized_rotated_180_flipped_vertical.jpg' -> 'images (10)'"""
    n = os.path.splitext(filename)[0]
    n = re.sub(r"(_resized)?(_rotated_\d+)?(_flipped_(horizontal|vertical))?$", "", n)
    n = re.sub(r"_resized$", "", n)
    n = re.sub(r"\.rf\.[0-9a-f]+$", "", n)       # Roboflow suffix
    return n

def list_images(root):
    """Yield (split, class, filename, path) for root/<split>/<class>/<file>."""
    for split in sorted(os.listdir(root)):
        sp = os.path.join(root, split)
        if not os.path.isdir(sp): continue
        for cls in sorted(os.listdir(sp)):
            cd = os.path.join(sp, cls)
            if not os.path.isdir(cd): continue
            for f in sorted(os.listdir(cd)):
                if f.lower().endswith(IMG_EXT):
                    yield split, cls, f, os.path.join(cd, f)
