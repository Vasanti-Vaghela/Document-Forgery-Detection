import os
import cv2
import numpy as np
from pdf2image import convert_from_path
from tensorflow.keras import layers, models
from sklearn.cluster import KMeans

IMG_SIZE = 128
DATASET_PATH = "Claim_Documents"

# ----------------------------
# PDF → IMAGE
# ----------------------------
def pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)
    imgs = []
    for img in images:
        imgs.append(np.array(img))
    return imgs

# ----------------------------
# LOAD DATA (NO LABELS)
# ----------------------------
def load_dataset(path):
    X = []

    for root, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)

            try:
                if file.lower().endswith(".pdf"):
                    images = pdf_to_images(full_path)
                    for img in images:
                        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
                        X.append(img)

                else:
                    img = cv2.imread(full_path)
                    if img is None:
                        continue

                    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
                    X.append(img)

            except Exception as e:
                print("Error:", e)

    X = np.array(X) / 255.0
    print("Total images:", len(X))
    return X

# ----------------------------
# LOAD
# ----------------------------
X = load_dataset(DATASET_PATH)

if len(X) == 0:
    raise ValueError("Dataset empty")

X = X.reshape(-1, IMG_SIZE, IMG_SIZE, 3)

# ----------------------------
# AUTOENCODER
# ----------------------------
input_img = layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3))

x = layers.Conv2D(32, (3,3), activation='relu', padding='same')(input_img)
x = layers.MaxPooling2D((2,2), padding='same')(x)

x = layers.Conv2D(16, (3,3), activation='relu', padding='same')(x)
encoded = layers.MaxPooling2D((2,2), padding='same')(x)

x = layers.Conv2D(16, (3,3), activation='relu', padding='same')(encoded)
x = layers.UpSampling2D((2,2))(x)

x = layers.Conv2D(32, (3,3), activation='relu', padding='same')(x)
x = layers.UpSampling2D((2,2))(x)

decoded = layers.Conv2D(3, (3,3), activation='sigmoid', padding='same')(x)

autoencoder = models.Model(input_img, decoded)
autoencoder.compile(optimizer='adam', loss='mse')

# TRAIN
autoencoder.fit(X, X, epochs=5, batch_size=16)

# ----------------------------
# RECONSTRUCTION ERROR
# ----------------------------
def get_reconstruction_error(img):
    img = img.reshape(1, IMG_SIZE, IMG_SIZE, 3)
    recon = autoencoder.predict(img, verbose=0)
    error = np.mean((img - recon) ** 2)
    return error

# ----------------------------
# THRESHOLD (REAL vs FAKE)
# ----------------------------
errors = [get_reconstruction_error(img) for img in X]
threshold = np.mean(errors) + np.std(errors)

print("Threshold:", threshold)

# ----------------------------
# FEATURE EXTRACTION
# ----------------------------
encoder = models.Model(input_img, encoded)

features = encoder.predict(X)
features = features.reshape(len(features), -1)

# ----------------------------
# CLUSTERING (10 categories)
# ----------------------------
kmeans = KMeans(n_clusters=10, random_state=42)
cluster_labels = kmeans.fit_predict(features)

print("Cluster labels:", cluster_labels[:20])

# ----------------------------
# FINAL PREDICT FUNCTION
# ----------------------------
def predict_document(image_path):
    if image_path.lower().endswith(".pdf"):
        imgs = pdf_to_images(image_path)
        img = imgs[0]
    else:
        img = cv2.imread(image_path)

    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE)) / 255.0

    # REAL / FAKE
    error = get_reconstruction_error(img)
    label = "REAL" if error < threshold else "FAKE"

    # CATEGORY
    feat = encoder.predict(img.reshape(1, IMG_SIZE, IMG_SIZE, 3), verbose=0)
    feat = feat.reshape(1, -1)
    category = kmeans.predict(feat)[0]

    return label, category, error

# ----------------------------
# TEST
# ----------------------------
result, category, err = predict_document("test.jpg")

print("Result:", result)
print("Category:", category)
print("Error:", err)