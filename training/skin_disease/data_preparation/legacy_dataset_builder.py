"""EARLIER (superseded) dataset preparation script - augments dataset/train in place, merges benign classes, undersamples."""
import os
import random
import cv2
import albumentations as A
from tqdm import tqdm
import shutil

# ================= CONFIG =================

TRAIN_DIR = "dataset/train"

BENIGN_CLASSES = [
    "Benign keratosis",
    "Melanocytic nevus",
]

MERGED_BENIGN = "benign_lesion"

UNDERSAMPLE_CONFIG = {
    "benign_lesion": 4500
}

AUGMENT_CONFIG = {
    "Melanoma": 4,
    "Tinea Ringworm Candidiasis": 2,
    "Melanocytic nevus": 1
}

# ========================================

aug_pipeline = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.Rotate(limit=20, p=0.7),
    A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),
    A.Affine(scale=(0.95,1.05), translate_percent=0.05, p=0.3),
    A.GaussNoise(p=0.2)
])

def get_images(folder):
    return [f for f in os.listdir(folder)
            if f.lower().endswith((".jpg",".jpeg",".png"))]

# ----------------------------------------------------

def augment_class(class_name, multiplier):
    if multiplier<=0: return

    folder = os.path.join(TRAIN_DIR,class_name)
    if not os.path.exists(folder): return

    images = get_images(folder)

    print(f"\n🧪 {class_name}: augment x{multiplier}")

    for img_name in tqdm(images):
        path = os.path.join(folder,img_name)

        img = cv2.imread(path)
        if img is None:
            continue

        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        for i in range(multiplier):
            augmented = aug_pipeline(image=img)["image"]
            augmented = cv2.cvtColor(augmented,cv2.COLOR_RGB2BGR)

            base = os.path.splitext(img_name)[0]
            new_name = f"{base}_aug{i}.jpg"

            cv2.imwrite(os.path.join(folder,new_name), augmented)

# ----------------------------------------------------

def merge_benign():
    target = os.path.join(TRAIN_DIR,MERGED_BENIGN)
    os.makedirs(target,exist_ok=True)

    print("\n🔀 Merging benign classes...")

    for cls in BENIGN_CLASSES:
        folder = os.path.join(TRAIN_DIR,cls)
        if not os.path.exists(folder): continue

        for img in get_images(folder):
            shutil.move(
                os.path.join(folder,img),
                os.path.join(target,f"{cls}_{img}")
            )

        shutil.rmtree(folder)

# ----------------------------------------------------

def undersample(cls,target_count):
    folder = os.path.join(TRAIN_DIR,cls)
    if not os.path.exists(folder): return

    imgs = get_images(folder)

    if len(imgs)<=target_count:
        print(f"✅ {cls} already below limit")
        return

    remove_n = len(imgs)-target_count
    print(f"✂️ {cls}: removing {remove_n}")

    for f in random.sample(imgs,remove_n):
        os.remove(os.path.join(folder,f))

# ----------------------------------------------------

def main():

    print("\n🚀 DATASET PREPARATION STARTED\n")

    # STEP 1 — AUGMENT
    print("STEP 1: Augmentation")
    for c,m in AUGMENT_CONFIG.items():
        augment_class(c,m)

    # STEP 2 — MERGE
    print("\nSTEP 2: Benign merge")
    merge_benign()

    # STEP 3 — UNDERSAMPLE
    print("\nSTEP 3: Undersample")
    for c,t in UNDERSAMPLE_CONFIG.items():
        undersample(c,t)

    print("\n✅ DONE.")
    print("➡ şimdi: python dataset_check.py")

if __name__=="__main__":
    main()
