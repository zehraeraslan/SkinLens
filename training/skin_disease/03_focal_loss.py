from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from sklearn.metrics import classification_report

# =====================
# PATH AYARLARI
# =====================
BASE_DIR = "final_dataset"   # eğitimde kullandığın klasör
TRAIN_DIR = os.path.join(BASE_DIR, "train")
VAL_DIR   = os.path.join(BASE_DIR, "valid")
TEST_DIR  = os.path.join(BASE_DIR, "test")

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10

# =====================
# DATA GENERATORS
# =====================
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=15,
    zoom_range=0.1,
    horizontal_flip=True
)

val_test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

val_generator = val_test_datagen.flow_from_directory(
    VAL_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

test_generator = val_test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

CLASS_NAMES = list(train_generator.class_indices.keys())

# =====================
# FOCAL LOSS
# =====================
def focal_loss(gamma=2., alpha=0.25):
    def loss(y_true, y_pred):
        y_pred = tf.clip_by_value(y_pred, 1e-7, 1 - 1e-7)
        cross_entropy = -y_true * tf.math.log(y_pred)
        weight = alpha * tf.pow(1 - y_pred, gamma)
        loss = weight * cross_entropy
        return tf.reduce_sum(loss, axis=1)
    return loss

# =====================
# MODEL YÜKLE
# =====================
print("\n🔥 Fine-tuned model yükleniyor...")
model = load_model("finetuned_skin_model.keras")

# Tüm katmanları açık bırakıyoruz
for layer in model.layers:
    layer.trainable = True

# =====================
# RECOMPILE (FOCAL LOSS)
# =====================
model.compile(
    optimizer=Adam(1e-5),
    loss=focal_loss(gamma=2, alpha=0.25),
    metrics=['accuracy']
)

# =====================
# CALLBACKS
# =====================
callbacks = [
    ModelCheckpoint("focal_finetuned_skin_model.keras",
                    monitor="val_accuracy",
                    save_best_only=True,
                    verbose=1),

    EarlyStopping(monitor="val_loss",
                  patience=5,
                  restore_best_weights=True),

    ReduceLROnPlateau(monitor="val_loss",
                      patience=2,
                      factor=0.2,
                      min_lr=1e-7)
]

# =====================
# EĞİTİM
# =====================
print("\n🚀 Focal Loss ile eğitim başlıyor...\n")

model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=val_generator,
    callbacks=callbacks
)

# =====================
# TEST DEĞERLENDİRME
# =====================
print("\n📊 TEST DEĞERLENDİRME")

best = load_model("focal_finetuned_skin_model.keras",
                  custom_objects={'loss': focal_loss(gamma=2, alpha=0.25)})

test_loss, test_acc = best.evaluate(test_generator)
print("Test Accuracy:", test_acc)

pred = best.predict(test_generator)
y_pred = np.argmax(pred, axis=1)
y_true = test_generator.classes

print("\nClassification Report:\n")
print(classification_report(y_true, y_pred, target_names=CLASS_NAMES))

