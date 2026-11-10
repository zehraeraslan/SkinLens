import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input

from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import classification_report, confusion_matrix

import os

# =========================
# DATASET PATH
# =========================

DATASET_PATH = "skin_concern"

IMG_SIZE = (224,224)
BATCH_SIZE = 32

# =========================
# DATASET LOAD
# =========================

train_dataset = tf.keras.utils.image_dataset_from_directory(
    os.path.join(DATASET_PATH,"train"),
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int"
)

valid_dataset = tf.keras.utils.image_dataset_from_directory(
    os.path.join(DATASET_PATH,"valid"),
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int"
)

test_dataset = tf.keras.utils.image_dataset_from_directory(
    os.path.join(DATASET_PATH,"test"),
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False,
    label_mode="int"
)

class_names = train_dataset.class_names
num_classes = len(class_names)

print("Classes:",class_names)

# =========================
# PERFORMANCE OPTIMIZATION
# =========================

AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(AUTOTUNE)
valid_dataset = valid_dataset.prefetch(AUTOTUNE)
test_dataset = test_dataset.prefetch(AUTOTUNE)

# =========================
# CLASS WEIGHTS
# =========================

y_train = np.concatenate([y for x,y in train_dataset],axis=0)

class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(y_train),
    y=y_train
)

class_weights = dict(enumerate(class_weights))

print("Class weights:",class_weights)

# =========================
# DATA AUGMENTATION
# =========================

data_augmentation = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])

# =========================
# MODEL
# =========================

base_model = EfficientNetB0(
    include_top=False,
    weights="imagenet",
    input_shape=(224,224,3)
)

base_model.trainable = False

inputs = keras.Input(shape=(224,224,3))

x = data_augmentation(inputs)
x = preprocess_input(x)

x = base_model(x,training=False)

x = layers.GlobalAveragePooling2D()(x)

x = layers.BatchNormalization()(x)

x = layers.Dense(256,activation="swish")(x)

x = layers.Dropout(0.4)(x)

outputs = layers.Dense(num_classes,activation="softmax")(x)

model = keras.Model(inputs,outputs)

# =========================
# COMPILE
# =========================

model.compile(

    optimizer=keras.optimizers.Adam(learning_rate=1e-3),

    loss="sparse_categorical_crossentropy",

    metrics=["accuracy"]

)

model.summary()

# =========================
# CALLBACKS
# =========================

callbacks = [

keras.callbacks.EarlyStopping(
    patience=5,
    restore_best_weights=True
),

keras.callbacks.ReduceLROnPlateau(
    factor=0.3,
    patience=3
),

keras.callbacks.ModelCheckpoint(
    "best_concern_checkpoint.keras",
    save_best_only=True
)

]

# =========================
# STAGE 1 TRAINING
# =========================

print("Stage 1 Training...")

history = model.fit(

    train_dataset,

    validation_data=valid_dataset,

    epochs=15,

    class_weight=class_weights,

    callbacks=callbacks

)

# =========================
# FINE TUNING
# =========================

print("Fine Tuning...")

base_model.trainable = True

for layer in base_model.layers[:-30]:
    layer.trainable = False

model.compile(

optimizer=keras.optimizers.Adam(1e-5),

loss="sparse_categorical_crossentropy",

metrics=["accuracy"]

)

history_fine = model.fit(

    train_dataset,

    validation_data=valid_dataset,

    epochs=10,

    class_weight=class_weights,

    callbacks=callbacks

)

# =========================
# SAVE MODEL
# =========================

model.save("skin_concern_final_model.keras")

print("Model saved")

# =========================
# PLOT TRAINING GRAPH
# =========================

acc = history.history["accuracy"] + history_fine.history["accuracy"]
val_acc = history.history["val_accuracy"] + history_fine.history["val_accuracy"]

loss = history.history["loss"] + history_fine.history["loss"]
val_loss = history.history["val_loss"] + history_fine.history["val_loss"]

plt.figure()

plt.plot(acc,label="train_accuracy")
plt.plot(val_acc,label="val_accuracy")

plt.legend()

plt.title("Accuracy")

plt.show()

plt.figure()

plt.plot(loss,label="train_loss")
plt.plot(val_loss,label="val_loss")

plt.legend()

plt.title("Loss")

plt.show()

# =========================
# TEST EVALUATION
# =========================

print("Test Evaluation")

test_loss,test_acc = model.evaluate(test_dataset)

print("Test Accuracy:",test_acc)

# =========================
# PREDICTIONS
# =========================

y_pred = np.argmax(model.predict(test_dataset),axis=1)

y_true = np.concatenate([y for x,y in test_dataset],axis=0)

# =========================
# CLASSIFICATION REPORT
# =========================

print("Classification Report")

print(

classification_report(

y_true,

y_pred,

target_names=class_names

)

)

# =========================
# CONFUSION MATRIX
# =========================

cm = confusion_matrix(y_true,y_pred)

print("Confusion Matrix")

print(cm)

# =========================
# CONFUSION MATRIX GRAPH
# =========================

plt.figure(figsize=(8,6))

sns.heatmap(

cm,

annot=True,

fmt="d",

cmap="Blues",

xticklabels=class_names,

yticklabels=class_names

)

plt.xlabel("Predicted")

plt.ylabel("True")

plt.title("Confusion Matrix")

plt.show()