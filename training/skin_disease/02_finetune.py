from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

# ================= PATHS =================
BASE_DIR = "final_dataset"
TRAIN_DIR = os.path.join(BASE_DIR, "train")
VAL_DIR = os.path.join(BASE_DIR, "valid")

IMG_SIZE = (224,224)
BATCH_SIZE = 32
EPOCHS = 15

# ================= DATA =================
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=15,
    zoom_range=0.1,
    horizontal_flip=True
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_gen = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

val_gen = val_datagen.flow_from_directory(
    VAL_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

# ================= MODEL LOAD =================
print("\n🔥 Model yükleniyor...")
model = load_model("best_skin_model.keras")

print("Toplam layer sayısı:", len(model.layers))

# ================= UNFREEZE LAST 60 LAYERS =================

for layer in model.layers:
    layer.trainable = False

for layer in model.layers[-60:]:
    layer.trainable = True

print("🔓 Son 60 katman açıldı.")

# ================= RECOMPILE =================
model.compile(
    optimizer=Adam(1e-5),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# ================= CALLBACKS =================
callbacks = [
    ModelCheckpoint("finetuned_skin_model.keras",
                    monitor="val_accuracy",
                    save_best_only=True,
                    verbose=1),

    EarlyStopping(monitor="val_loss",
                  patience=6,
                  restore_best_weights=True),

    ReduceLROnPlateau(monitor="val_loss",
                      patience=3,
                      factor=0.2,
                      min_lr=1e-7)
]

# ================= TRAIN =================
print("\n🚀 Fine-Tuning başlıyor...\n")

model.fit(
    train_gen,
    epochs=EPOCHS,
    validation_data=val_gen,
    callbacks=callbacks
)

print("\n✅ Fine tuning tamamlandı.")
