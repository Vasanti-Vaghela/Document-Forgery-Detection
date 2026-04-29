import os
import cv2
import fitz  # PyMuPDF
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras import layers, models
from tensorflow.keras.models import load_model
from skimage.metrics import structural_similarity as ssim

IMG_SIZE = 128
DATASET_PATH = "Claim_Documents"
MODEL_PATH = "model.h5"
BASELINE_STATS_PATH = "baseline_stats.npy"

# ----------------------------
# PDF → IMAGES
# ----------------------------
def pdf_to_images(pdf_path, output_folder="temp_images"):
    os.makedirs(output_folder, exist_ok=True)

    doc = fitz.open(pdf_path)
    paths = []

    for i, page in enumerate(doc):
        pix = page.get_pixmap()
        img_path = os.path.join(output_folder, f"page_{i+1}.jpg")
        pix.save(img_path)
        paths.append(img_path)

    return paths

# ----------------------------
# LOAD DATA
# ----------------------------
def load_images(path):
    data = []
    for file in os.listdir(path):
        img = cv2.imread(os.path.join(path, file))
        if img is None:
            continue
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE)) / 255.0
        data.append(img)
    return np.array(data)

# ----------------------------
# MODEL
# ----------------------------
def build_model():
    inp = layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3))

    x = layers.Conv2D(64,3,activation='relu',padding='same')(inp)
    x = layers.MaxPooling2D(2)(x)
    x = layers.Conv2D(128,3,activation='relu',padding='same')(x)
    x = layers.MaxPooling2D(2)(x)

    x = layers.Conv2D(128,3,activation='relu',padding='same')(x)
    x = layers.UpSampling2D(2)(x)
    x = layers.Conv2D(64,3,activation='relu',padding='same')(x)
    x = layers.UpSampling2D(2)(x)

    out = layers.Conv2D(3,3,activation='sigmoid',padding='same')(x)

    model = models.Model(inp, out)
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# ----------------------------
# TRAIN
# ----------------------------
def train():
    X = load_images(DATASET_PATH)
    model = build_model()

    model.fit(X, X, epochs=30, batch_size=16)
    model.save(MODEL_PATH)

    scores = []
    for img in X:
        recon = model.predict(img[np.newaxis,...])[0]
        error = np.abs(img - recon)
        scores.append(np.mean(error))

    np.save(BASELINE_STATS_PATH, [np.mean(scores), np.std(scores)])
    print("✅ Training Done")

# ----------------------------
# DETECT CORE
# ----------------------------
def detect_image(path, show=True):
    model = load_model(MODEL_PATH, compile=False)
    mean_score, std_score = np.load(BASELINE_STATS_PATH)

    img = cv2.imread(path)
    orig = img.copy()

    img_resized = cv2.resize(img, (IMG_SIZE, IMG_SIZE)) / 255.0
    recon = model.predict(img_resized[np.newaxis,...])[0]

    error = np.abs(img_resized - recon)
    heatmap = np.mean(error, axis=2)

    heatmap_norm = (heatmap - heatmap.min()) / (heatmap.max() - heatmap.min())
    mask = (heatmap_norm > 0.15).astype(np.uint8)

    # -------- LOGICS --------
    score = np.mean(error)
    threshold = mean_score + 3*std_score

    percentage = (np.sum(mask) / mask.size) * 100

    gray1 = cv2.cvtColor((img_resized*255).astype("uint8"), cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor((recon*255).astype("uint8"), cv2.COLOR_BGR2GRAY)
    ssim_score, _ = ssim(gray1, gray2, full=True)

    # FINAL DECISION
    if score > threshold or percentage > 15 or ssim_score < 0.75:
        result = "FAKE"
    else:
        result = "ORIGINAL"

    print(f"{path} → {result} | Score:{score:.3f} | %:{percentage:.1f} | SSIM:{ssim_score:.2f}")

    if show:
        highlight = orig.copy()
        mask_full = cv2.resize(mask, (orig.shape[1], orig.shape[0]))
        highlight[mask_full > 0] = [0,0,255]

        plt.imshow(cv2.cvtColor(highlight, cv2.COLOR_BGR2RGB))
        plt.title(result)
        plt.axis("off")
        plt.show()

    return result

# ----------------------------
# DATASET TEST (IMPORTANT 🔥)
# ----------------------------
def test_dataset_visual():

    print("\n🔍 Testing FULL dataset with visualization...\n")

    model = load_model(MODEL_PATH, compile=False)
    mean_score, std_score = np.load(BASELINE_STATS_PATH)

    images = []
    titles = []

    correct = 0
    total = 0

    for file in os.listdir(DATASET_PATH):

        path = os.path.join(DATASET_PATH, file)
        img = cv2.imread(path)

        if img is None:
            continue

        orig = img.copy()
        img_resized = cv2.resize(img, (IMG_SIZE, IMG_SIZE)) / 255.0

        recon = model.predict(img_resized[np.newaxis,...])[0]

        error = np.abs(img_resized - recon)
        heatmap = np.mean(error, axis=2)

        heatmap_norm = (heatmap - heatmap.min()) / (heatmap.max() - heatmap.min())
        mask = (heatmap_norm > 0.15).astype(np.uint8)

        # LOGICS
        score = np.mean(error)
        threshold = mean_score + 3*std_score
        percentage = (np.sum(mask) / mask.size) * 100

        gray1 = cv2.cvtColor((img_resized*255).astype("uint8"), cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor((recon*255).astype("uint8"), cv2.COLOR_BGR2GRAY)
        ssim_score, _ = ssim(gray1, gray2, full=True)

        if score > threshold or percentage > 15 or ssim_score < 0.75:
            result = "FAKE"
        else:
            result = "ORIGINAL"

        # accuracy check (dataset original hai)
        if result == "ORIGINAL":
            correct += 1

        total += 1

        # highlight image
        mask_full = cv2.resize(mask, (orig.shape[1], orig.shape[0]))
        highlight = orig.copy()
        highlight[mask_full > 0] = [0,0,255]

        images.append(cv2.cvtColor(highlight, cv2.COLOR_BGR2RGB))
        titles.append(f"{result}\n{file}")

    # -------- GRID DISPLAY --------
    cols = 4
    rows = int(np.ceil(len(images) / cols))

    plt.figure(figsize=(15, 10))

    for i in range(len(images)):
        plt.subplot(rows, cols, i+1)
        plt.imshow(images[i])
        plt.title(titles[i], fontsize=8)
        plt.axis("off")

    accuracy = (correct/total)*100 if total > 0 else 0

    plt.suptitle(f"Dataset Results | Accuracy: {accuracy:.2f}%", fontsize=16, color="red")
    plt.tight_layout()
    plt.show()

    print(f"\n✅ Accuracy on dataset: {accuracy:.2f}%")

# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":

    choice = input("train / detect / pdf / test: ")

    if choice == "train":
        train()

    elif choice == "detect":
        path = input("Enter image path: ")
        detect_image(path)

    elif choice == "pdf":
        pdf_path = input("Enter PDF path: ")
        images = pdf_to_images(pdf_path)

        for img in images:
            detect_image(img)

    elif choice == "test":
        test_dataset_visual()

    else:
        print("❌ Invalid choice")