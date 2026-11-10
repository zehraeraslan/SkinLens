# ==========================================================
# HYBRID SKIN TYPE CLASSIFICATION - DATA PIPELINE
# LBP + CNN Dual Input Generator (Production Ready)
# ==========================================================

import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.utils import Sequence
from skimage.feature import local_binary_pattern


# ==========================================================
# 1️⃣ LBP FEATURE EXTRACTION MODULE
# ==========================================================

def extract_lbp_features(img_batch, radius=3):
    """
    Extract uniform LBP histogram features from RGB image batch.

    Parameters:
        img_batch : numpy array (B, H, W, 3) normalized 0-1
        radius    : LBP radius (default=3)

    Returns:
        numpy array (B, 26)
    """

    n_points = 8 * radius
    n_bins = n_points + 2  # uniform LBP bins

    lbp_features = []

    for img in img_batch:

        # Normalize check
        if np.max(img) <= 1.0:
            img_uint8 = (img * 255).astype(np.uint8)
        else:
            img_uint8 = img.astype(np.uint8)

        # Convert RGB → Grayscale
        gray = cv2.cvtColor(img_uint8, cv2.COLOR_RGB2GRAY)

        # Compute LBP
        lbp = local_binary_pattern(
            gray,
            P=n_points,
            R=radius,
            method="uniform"
        )

        # Histogram
        hist, _ = np.histogram(
            lbp.ravel(),
            bins=np.arange(0, n_bins + 1),
            range=(0, n_bins)
        )

        # Normalize histogram
        hist = hist.astype("float32")
        hist /= (hist.sum() + 1e-8)

        lbp_features.append(hist)

    return np.array(lbp_features, dtype="float32")


# ==========================================================
# 2️⃣ HYBRID DATA GENERATOR
# ==========================================================

class HybridSkinGenerator(Sequence):
    """
    Custom Keras Sequence for Dual Input Model:
        - CNN Image Input
        - LBP Texture Input
    """

    def __init__(self,
                 directory,
                 batch_size=32,
                 target_size=(224, 224),
                 shuffle=True,
                 augment=False):

        if not os.path.exists(directory):
            raise ValueError(f"Directory not found: {directory}")

        self.batch_size = batch_size
        self.shuffle = shuffle

        # Image Augmentation (Optional)
        if augment:
            self.datagen = tf.keras.preprocessing.image.ImageDataGenerator(
                rescale=1./255,
                horizontal_flip=True,
                rotation_range=20,
                zoom_range=0.1,
                brightness_range=[0.9, 1.1]
            )
        else:
            self.datagen = tf.keras.preprocessing.image.ImageDataGenerator(
                rescale=1./255
            )

        # Flow from directory
        self.gen = self.datagen.flow_from_directory(
            directory=directory,
            target_size=target_size,
            batch_size=batch_size,
            class_mode="categorical",
            shuffle=shuffle
        )

        self.classes = self.gen.classes
        self.class_indices = self.gen.class_indices
        self.num_classes = len(self.class_indices)

        # DEBUG INFO
        print("\n================ DATASET INFO ================")
        print("Directory:", directory)
        print("Classes detected:", self.class_indices)
        print("Number of classes:", self.num_classes)
        print("Total samples:", self.gen.samples)
        print("Batch size:", self.batch_size)
        print("==============================================\n")

        # Safety check
        if self.num_classes < 2:
            raise ValueError("Dataset must contain at least 2 classes.")

    # ------------------------------------------------------

    def __len__(self):
        return int(np.ceil(self.gen.samples / self.batch_size))

    # ------------------------------------------------------

    def __getitem__(self, index):
        imgs, labels = self.gen[index]

        # Extract LBP features
        lbp_features = extract_lbp_features(imgs)

        return [imgs, lbp_features], labels

    # ------------------------------------------------------

    def on_epoch_end(self):
        if self.shuffle:
            self.gen.on_epoch_end()


# ==========================================================
# 3️⃣ QUICK SANITY TEST FUNCTION
# ==========================================================

def test_generator(generator):
    print("Running sanity check...")

    (imgs, lbps), labels = generator[0]

    print("Image batch shape:", imgs.shape)
    print("LBP batch shape:", lbps.shape)
    print("Label shape:", labels.shape)

    assert imgs.shape[1:] == (224, 224, 3), "Image shape mismatch"
    assert lbps.shape[1] == 26, "LBP feature size must be 26"
    assert labels.shape[1] == generator.num_classes, "Label class mismatch"

    print("Sanity check passed ✅\n")


# ==========================================================
# 4️⃣ USAGE EXAMPLE
# ==========================================================

if __name__ == "__main__":

    train_gen = HybridSkinGenerator(
        directory="skin_type/train",
        batch_size=8,
        augment=True
    )

    val_gen = HybridSkinGenerator(
        directory="skin_type/validation",
        batch_size=8,
        shuffle=False
    )

    test_gen = HybridSkinGenerator(
        directory="skin_type/test",
        batch_size=8,
        shuffle=False
    )

    # Test pipeline
    test_generator(train_gen)
