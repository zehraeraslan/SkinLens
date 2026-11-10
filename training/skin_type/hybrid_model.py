# ==========================================================
# HYBRID MODEL: DenseNet121 + LBP (Production Ready)
# ==========================================================

from tensorflow.keras.layers import (
    Input, Dense, Dropout, BatchNormalization,
    GlobalAveragePooling2D, Concatenate
)
from tensorflow.keras.models import Model
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras.optimizers import Adam


def build_hybrid_model(num_classes):
    # ---------------------------
    # 1️⃣ IMAGE INPUT (CNN BRANCH - DenseNet121)
    # ---------------------------
    image_input = Input(shape=(224, 224, 3), name="image_input")

    base_model = DenseNet121(
        weights="imagenet",
        include_top=False,
        input_tensor=image_input
    )

    base_model.trainable = False  # İlk aşamada donduruyoruz

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = BatchNormalization()(x)

    # SENİN HARİKA DENGELEME KATMANIN: DenseNet'in 1024 boyutunu 256'ya eziyoruz.
    x = Dense(256, activation="relu")(x)
    x = Dropout(0.4)(x)

    # ---------------------------
    # 2️⃣ LBP INPUT (TEXTURE BRANCH)
    # ---------------------------
    lbp_input = Input(shape=(26,), name="lbp_input")

    y = Dense(64, activation="relu")(lbp_input)
    y = BatchNormalization()(y)
    y = Dropout(0.3)(y)
    y = Dense(32, activation="relu")(y)

    # ---------------------------
    # 3️⃣ FUSION (BİRLEŞTİRME)
    # ---------------------------
    combined = Concatenate()([x, y])

    z = Dense(128, activation="relu")(combined)
    z = BatchNormalization()(z)
    z = Dropout(0.4)(z)

    output = Dense(num_classes, activation="softmax")(z)

    model = Model(
        inputs=[image_input, lbp_input],
        outputs=output
    )

    model.compile(
        optimizer=Adam(learning_rate=1e-4),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model