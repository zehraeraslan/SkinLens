"""Deletes unreadable/corrupt images IN PLACE from final_dataset (destructive - keep a backup)."""
import os
from PIL import Image

BASE_DIR = "final_dataset"   # senin dataset klasörün

bad_images = []

for split in ["train", "valid", "test"]:
    split_path = os.path.join(BASE_DIR, split)

    for cls in os.listdir(split_path):
        cls_path = os.path.join(split_path, cls)

        if not os.path.isdir(cls_path):
            continue

        for img_name in os.listdir(cls_path):
            img_path = os.path.join(cls_path, img_name)

            try:
                img = Image.open(img_path)
                img.verify()
            except:
                bad_images.append(img_path)

print(f"\n🧨 Found {len(bad_images)} corrupted images")

for img in bad_images:
    print("Deleting:", img)
    os.remove(img)

print("\n✅ Cleanup finished.")
