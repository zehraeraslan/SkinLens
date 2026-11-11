"""Evaluates the STAGE 2 model (finetuned_skin_model.keras) on final_dataset/test. (Originally named mel.py.)
Use it to fill the missing Stage 2 test accuracy in the thesis."""
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report

# -----------------------------
# AYARLAR
# -----------------------------
IMG_SIZE = 224
BATCH_SIZE = 32

CLASS_NAMES = ['Acne',
               'Atopic Dermatitis',
               'Melanoma',
               'Tinea Ringworm Candidiasis',
               'benign_lesion']

TEST_DIR = "final_dataset/test"   # ⚠️ test klasör yolun neyse onu yaz

# -----------------------------
# TEST GENERATOR
# -----------------------------
test_datagen = ImageDataGenerator(rescale=1./255)

test_generator = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

# -----------------------------
# MODEL YÜKLE
# -----------------------------
print("\n📊 TEST DEĞERLENDİRME")

best = load_model("finetuned_skin_model.keras")

test_loss, test_acc = best.evaluate(test_generator)
print("Test Accuracy:", test_acc)

# -----------------------------
# CLASSIFICATION REPORT
# -----------------------------
pred = best.predict(test_generator)
y_pred = np.argmax(pred, axis=1)
y_true = test_generator.classes

print("\nClassification Report:\n")
print(classification_report(y_true, y_pred, target_names=CLASS_NAMES))
