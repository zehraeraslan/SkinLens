from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. AYARLAR VE PATHLER ---
# Burayı kendi klasör yapına göre güncelle
BASE_DIR = "final_dataset"  # Oluşturduğun son dataset klasörü
TRAIN_DIR = os.path.join(BASE_DIR, "train")
VAL_DIR = os.path.join(BASE_DIR, "valid")
TEST_DIR = os.path.join(BASE_DIR, "test")

IMG_SIZE = (224, 224)  # DenseNet için standart boyut
BATCH_SIZE = 32
EPOCHS = 30  # EarlyStopping olduğu için yüksek verebiliriz, gerekirse erken durur.

# --- 2. VERİ YÜKLEME (DATA GENERATORS) ---
# Bellek dostu yükleme. Resimleri tek tek değil, ihtiyaç oldukça yükler.

# Eğitim için Augmentation (Eğitim sırasında canlı çeşitlendirme)
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Validasyon ve Test için SADECE ölçekleme (Resimler bozulmamalı)
val_test_datagen = ImageDataGenerator(rescale=1. / 255)

print("💾 Veri Yükleniyor...")
train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=True
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
    shuffle=False  # Değerlendirme için sırayı bozmamalıyız
)

# Sınıf isimlerini ve sayısını otomatik al
CLASS_NAMES = list(train_generator.class_indices.keys())
NUM_CLASSES = len(CLASS_NAMES)
print(f"✅ Tespit Edilen Sınıflar ({NUM_CLASSES}): {CLASS_NAMES}")

# --- 3. SINIF AĞIRLIKLARINI HESAPLAMA ---
# Dengesiz veri setlerinde modelin azınlık sınıfları (Melanoma gibi) önemsemesini sağlar.
print("⚖️ Sınıf Ağırlıkları Hesaplanıyor...")
train_classes = train_generator.classes
class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(train_classes),
    y=train_classes
)
class_weights_dict = dict(enumerate(class_weights))
print(f"Sınıf Ağırlıkları: {class_weights_dict}")

# --- 4. MODEL MİMARİSİ (TRANSFER LEARNING) ---
# DenseNet121: Tıbbi görüntülemede çok başarılıdır.
base_model = DenseNet121(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Başlangıçta base modelin ağırlıklarını donduruyoruz (Sadece kendi katmanlarımızı eğiteceğiz)
base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = BatchNormalization()(x)  # Eğitimi hızlandırır ve stabilize eder
x = Dense(256, activation='relu')(x)
x = Dropout(0.5)(x)  # Overfitting'i engeller
predictions = Dense(NUM_CLASSES, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

model.compile(optimizer=Adam(learning_rate=1e-4),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# --- 5. CALLBACKS (AKILLI EĞİTİM YÖNETİCİLERİ) ---
callbacks = [
    # En iyi modeli kaydet (Validasyon başarısı artarsa)
    ModelCheckpoint("best_skin_model.keras", monitor='val_accuracy', save_best_only=True, mode='max', verbose=1),

    # Model 8 epoch boyunca gelişmezse eğitimi durdur
    EarlyStopping(monitor='val_loss', patience=8, restore_best_weights=True, verbose=1),

    # Başarı duraksarsa öğrenme hızını düşür (Daha hassas öğren)
    ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-7, verbose=1)
]

# --- 6. EĞİTİM BAŞLIYOR ---
print("\n🚀 Eğitim Başlıyor...")
history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=val_generator,
    class_weight=class_weights_dict,  # Kritik nokta: Ağırlıkları ekliyoruz
    callbacks=callbacks
)


# --- 7. SONUÇLARI GÖRSELLEŞTİRME ---
def plot_history(history):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs_range = range(len(acc))

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()


plot_history(history)

# --- 8. DETAYLI TEST VE RAPORLAMA ---
print("\n📊 Test Seti Üzerinde Değerlendirme Yapılıyor...")

# En iyi modeli yükle (Eğitim sırasındaki en iyi an)
best_model = load_model("best_skin_model.keras")

# Test seti tahminleri
test_loss, test_acc = best_model.evaluate(test_generator)
print(f"Test Accuracy: {test_acc:.4f}")

# Detaylı Rapor (Precision, Recall, F1-Score)
predictions = best_model.predict(test_generator)
y_pred = np.argmax(predictions, axis=1)
y_true = test_generator.classes

print("\n📋 Sınıflandırma Raporu:")
print(classification_report(y_true, y_pred, target_names=CLASS_NAMES))

# Confusion Matrix
cm = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES)
plt.xlabel('Tahmin Edilen (Predicted)')
plt.ylabel('Gerçek (True)')
plt.title('Confusion Matrix')
plt.show()