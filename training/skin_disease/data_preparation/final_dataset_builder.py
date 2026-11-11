"""ORIGINAL SCRIPT that produced final_dataset (kept unchanged below).
Pools the source train/valid/test, merges Benign keratosis + Melanocytic nevus into benign_lesion,
undersamples benign_lesion to 4500, splits 80/10/10 per class, then augments TRAIN only.
KNOWN ISSUE: no de-duplication before the random split -> byte-identical images end up in train AND test.
Use scripts/build_clean_disease_dataset.py instead."""
import os
import shutil
import random
import cv2
import albumentations as A
from sklearn.model_selection import train_test_split
from tqdm import tqdm

BASE = "dataset"
RAW = "raw_all"
FINAL = "final_dataset"

CLASSES = ["benign_lesion","Acne","Melanoma","Tinea Ringworm Candidiasis","Atopic Dermatitis"]

BENIGN_PARTS = ["Benign keratosis","Melanocytic nevus"]

UNDERSAMPLE = {
    "benign_lesion":4500
}

AUGMENT = {
    "Melanoma":4,
    "Tinea Ringworm Candidiasis":2
}

aug = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.Rotate(limit=20,p=0.7),
    A.RandomBrightnessContrast(p=0.4),
    A.Affine(scale=(0.95,1.05),translate_percent=0.05,p=0.3),
    A.GaussNoise(p=0.2)
])

def collect_raw():
    if os.path.exists(RAW): shutil.rmtree(RAW)
    for c in CLASSES:
        os.makedirs(os.path.join(RAW,c),exist_ok=True)

    for split in ["train","valid","test"]:
        for c in CLASSES:
            src=os.path.join(BASE,split,c)
            if not os.path.exists(src): continue
            for f in os.listdir(src):
                shutil.copy(src+"/"+f,RAW+"/"+c+"/"+split+"_"+f)

    # merge benign
    benign=os.path.join(RAW,"benign_lesion")
    os.makedirs(benign,exist_ok=True)

    for part in BENIGN_PARTS:
        for split in ["train","valid","test"]:
            src=os.path.join(BASE,split,part)
            if not os.path.exists(src): continue
            for f in os.listdir(src):
                shutil.copy(src+"/"+f,benign+"/"+part+"_"+f)

def undersample():
    for c,n in UNDERSAMPLE.items():
        files=os.listdir(RAW+"/"+c)
        if len(files)<=n: continue
        for f in random.sample(files,len(files)-n):
            os.remove(RAW+"/"+c+"/"+f)

def split():
    if os.path.exists(FINAL): shutil.rmtree(FINAL)

    for sp in ["train","valid","test"]:
        for c in CLASSES:
            os.makedirs(FINAL+"/"+sp+"/"+c,exist_ok=True)

    for c in CLASSES:
        files=os.listdir(RAW+"/"+c)
        train,rest=train_test_split(files,test_size=0.2,random_state=42)
        val,test=train_test_split(rest,test_size=0.5,random_state=42)

        for f in train:
            shutil.copy(RAW+"/"+c+"/"+f,FINAL+"/train/"+c+"/"+f)
        for f in val:
            shutil.copy(RAW+"/"+c+"/"+f,FINAL+"/valid/"+c+"/"+f)
        for f in test:
            shutil.copy(RAW+"/"+c+"/"+f,FINAL+"/test/"+c+"/"+f)

def augment():
    for c,m in AUGMENT.items():
        folder=FINAL+"/train/"+c
        imgs=os.listdir(folder)

        for f in tqdm(imgs,desc=f"augment {c}"):
            im=cv2.imread(folder+"/"+f)
            im=cv2.cvtColor(im,cv2.COLOR_BGR2RGB)

            for i in range(m):
                out=aug(image=im)["image"]
                out=cv2.cvtColor(out,cv2.COLOR_RGB2BGR)
                cv2.imwrite(folder+"/"+f[:-4]+f"_aug{i}.jpg",out)

def main():
    collect_raw()
    undersample()
    split()
    augment()
    print("\n✅ FINAL DATASET READY")

if __name__=="__main__":
    main()
