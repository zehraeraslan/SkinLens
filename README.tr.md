# 🔬 SkinLens — Görüntü İşleme ile Cilt Hastalıklarının Tespiti ve Bilgi Sistemi

Üsküdar Üniversitesi Yazılım Mühendisliği bitirme projesi. Tek bir fotoğraftan **cilt tipi**, **cilt hastalığı** ve **cilt sorunu** analizi yapan; sonuçları **Grad-CAM** ile görselleştiren tam kapsamlı (full-stack) web uygulamasıdır.

> ⚠️ **Tıbbi uyarı:** SkinLens eğitim ve ön tarama amaçlıdır; tıbbi cihaz değildir ve doktor teşhisinin yerine geçmez.

## Modeller
- **Cilt hastalığı:** DenseNet121, 3 aşamalı eğitim (sınıf ağırlıkları → ince ayar → focal loss). Test doğruluğu **%87,97** (1.430 görüntü).
- **Cilt tipi:** DenseNet121 + 26 boyutlu LBP hibrit model (Kuru/Normal/Yağlı/Hassas). Test doğruluğu **%92** (235 görüntü).
- **Cilt sorunu:** Akne, Siyah Nokta, Gözenek, Kırışıklık.
- %70 güven eşiği, Grad-CAM ısı haritaları ve kural tabanlı bakım önerileri.

## Mimari
React + TypeScript (frontend) → Express.js (proxy) → FastAPI + TensorFlow (AI backend).

Kurulum, API ve dağıtım için [İngilizce README](README.md), [docs/deployment.md](docs/deployment.md) ve [docs/model-card.md](docs/model-card.md) dosyalarına bakınız.

## Lisans
Kod MIT lisansı altındadır. Veri setleri kendi orijinal lisanslarına tabidir.

**Yazar:** Zehra Eraslan
