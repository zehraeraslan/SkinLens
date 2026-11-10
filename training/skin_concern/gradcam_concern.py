import numpy as np
import tensorflow as tf
import cv2
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input

# =========================
# 1. AYARLAR
# =========================
MODEL_PATH = "skin_concern_final_model.keras"
# Usage: python gradcam_concern.py path/to/image.jpg
import sys
IMG_PATH = sys.argv[1] if len(sys.argv) > 1 else "sample.jpg"
IMG_SIZE = (224, 224)

print("Model yükleniyor...")
model = keras.models.load_model(MODEL_PATH)

# Ana modelin içindeki EfficientNet bloğunu bul
base_model = None
for layer in model.layers:
    if "efficientnet" in layer.name.lower():
        base_model = layer
        break

if base_model is None:
    raise ValueError("Model içinde EfficientNet katmanı bulunamadı!")

# =========================
# 2. ÜST KATMANLARI AYIRMA (Sınıflandırıcı Model)
# =========================
# EfficientNet'ten sonra gelen GAP, Dropout, Dense gibi katmanları
# yeni ve tertemiz bir modele taşıyoruz. Böylece hata almayacağız.
classifier_input = keras.Input(shape=base_model.output_shape[1:])
x = classifier_input
found_base = False

for layer in model.layers:
    if found_base:
        x = layer(x)
    elif layer.name == base_model.name:
        found_base = True

classifier_model = keras.Model(inputs=classifier_input, outputs=x)

# =========================
# 3. GÖRSEL İŞLEME VE ÖZELLİK ÇIKARMA
# =========================
img = image.load_img(IMG_PATH, target_size=IMG_SIZE)
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)

# Veriyi EfficientNet için hazırlıyoruz (Augmentation'ı atlıyoruz, inference'de gerekmez)
img_array = preprocess_input(img_array)

# Base modelden özellikleri (feature map) alıyoruz (Burası 7x7 uzamsal boyuttadır)
feature_map = base_model(img_array, training=False)

# =========================
# 4. TENSÖR İZLEME VE GRAD-CAM HESABI
# =========================
# Özellik haritasını Tensör'e çeviriyoruz
feature_map_tensor = tf.convert_to_tensor(feature_map)

with tf.GradientTape() as tape:
    # Keras yerine Tape ile manuel izleme başlatıyoruz
    tape.watch(feature_map_tensor)

    # Tensörü sınıflandırıcı modele verip tahmini alıyoruz
    predictions = classifier_model(feature_map_tensor, training=False)

    # Modelin en yüksek olasılık verdiği sınıf
    pred_index = tf.argmax(predictions[0])
    class_channel = predictions[:, pred_index]

# Hedef sınıfın özelliğe göre gradyanını (türevini) al
grads = tape.gradient(class_channel, feature_map_tensor)

# Kanal bazında uzamsal ortalamaları bul (GAP simülasyonu)
pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

# Haritayı ağırlıklandır
feature_map_tensor = feature_map_tensor[0]
heatmap = feature_map_tensor @ pooled_grads[..., tf.newaxis]
heatmap = tf.squeeze(heatmap)

# Sıfırdan küçük değerleri at (ReLU) ve Normalleştir (0-1 arası)
heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-10)
heatmap = heatmap.numpy()

# =========================
# 5. GÖRSELLEŞTİRME VE KAYIT
# =========================
try:
    # Orijinal resmi OpenCV ile yükle
    img_cv2 = cv2.imread(IMG_PATH)
    img_cv2 = cv2.resize(img_cv2, IMG_SIZE)

    # Heatmap boyutunu orijinal resimle aynı yap
    heatmap = cv2.resize(heatmap, (img_cv2.shape[1], img_cv2.shape[0]))
    heatmap = np.uint8(255 * heatmap)

    # Renk haritası uygula (Mavi=Düşük, Kırmızı=Yüksek odak)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    # İkisini üst üste bindir
    result = cv2.addWeighted(img_cv2, 0.6, heatmap, 0.4, 0)

    # Sonucu kaydet
    output_filename = "gradcam_kusursuz_sonuc.jpg"
    cv2.imwrite(output_filename, result)
    print(f"Başarılı! Sonuç kaydedildi: {output_filename}")

    # Ekranda göster
    plt.figure(figsize=(8, 8))
    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    plt.title("Grad-CAM: Modelin Karar Odak Noktası")
    plt.axis("off")
    plt.show()

except Exception as e:
    print(f"Görselleştirme sırasında bir hata oluştu: {e}")