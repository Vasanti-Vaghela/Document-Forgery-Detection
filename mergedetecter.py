import cv2
import numpy as np
from PIL import Image
import pytesseract
import io
import os
import matplotlib.pyplot as plt
from tensorflow.keras import layers, models
from tensorflow.keras.models import load_model

# -----------------------------
# 🔧 SETTINGS
# -----------------------------
IMG_SIZE = 128
MODEL_PATH = "merge_model.h5"
THRESHOLD = 0.5



if os.name == "nt":  # Windows only
    possible_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(possible_path):
        pytesseract.pytesseract.tesseract_cmd = possible_path

# -----------------------------
# ELA
# -----------------------------
def ela_image(image, quality=90):
    pil_img = Image.fromarray(image)

    buffer = io.BytesIO()
    pil_img.save(buffer, "JPEG", quality=quality)
    buffer.seek(0)

    compressed = Image.open(buffer)
    ela = np.abs(np.array(pil_img) - np.array(compressed))

    return cv2.normalize(ela, None, 0, 255, cv2.NORM_MINMAX)

# -----------------------------
# MODEL
# -----------------------------
def build_model():
    input_img = layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3))

    x = layers.Conv2D(32, 3, activation='relu', padding='same')(input_img)
    x = layers.MaxPooling2D(2)(x)
    x = layers.Conv2D(64, 3, activation='relu', padding='same')(x)
    x = layers.MaxPooling2D(2)(x)

    x = layers.Conv2D(64, 3, activation='relu', padding='same')(x)
    x = layers.UpSampling2D(2)(x)
    x = layers.Conv2D(32, 3, activation='relu', padding='same')(x)
    x = layers.UpSampling2D(2)(x)

    output = layers.Conv2D(3, 3, activation='sigmoid', padding='same')(x)

    model = models.Model(input_img, output)
    model.compile(optimizer='adam', loss='mse')
    return model

# -----------------------------
# PATCHES
# -----------------------------
def get_patches(img, size=128):
    patches = []
    h, w, _ = img.shape

    for y in range(0, h, size):
        for x in range(0, w, size):
            patch = img[y:y+size, x:x+size]
            if patch.shape[0] == size and patch.shape[1] == size:
                patches.append(patch)

    return patches

# -----------------------------
# ERROR
# -----------------------------
def patch_error(model, patch):
    patch = patch / 255.0
    patch = np.expand_dims(patch, axis=0)
    recon = model.predict(patch, verbose=0)
    return np.mean((patch - recon) ** 2)

# -----------------------------
# OCR CHECK
# -----------------------------
def text_inconsistency(img):
    try:
        text = pytesseract.image_to_string(img)
        lines = text.split("\n")
        lengths = [len(l) for l in lines if len(l) > 5]

        if len(lengths) < 2:
            return 0

        return np.var(lengths)
    except:
        return 0

# -----------------------------
# HEATMAP
# -----------------------------
def generate_heatmap(img, patch_scores, size=128):
    heatmap = np.zeros((img.shape[0], img.shape[1]))

    idx = 0
    for y in range(0, img.shape[0], size):
        for x in range(0, img.shape[1], size):
            if y+size <= img.shape[0] and x+size <= img.shape[1]:
                heatmap[y:y+size, x:x+size] = patch_scores[idx]
                idx += 1

    heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX).astype("uint8")
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    return cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)

# -----------------------------
# TRAIN
# -----------------------------
def train(folder="Claim_Documents"):

    model = build_model()
    images = []

    for file in os.listdir(folder):

        if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        path = os.path.join(folder, file)
        img = cv2.imread(path)

        if img is None:
            print("Skipping:", file)
            continue

        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        images.append(img / 255.0)

    images = np.array(images)

    print("Training on", len(images), "images...")

    model.fit(images, images, epochs=10)
    model.save(MODEL_PATH)

    print("✅ Model Saved!")

# -----------------------------
# DETECT IMAGE
# -----------------------------
def detect_image(path, show=True):

    if not os.path.exists(MODEL_PATH):
        print("❌ Model not found, run train first")
        return "ERROR"

    model = load_model(MODEL_PATH, compile=False)

    img = cv2.imread(path)

    if img is None:
        print(f"❌ Invalid image: {path}")
        return "ERROR"

    ela = ela_image(img)
    patches = get_patches(ela)

    if len(patches) == 0:
        print("❌ No valid patches:", path)
        return "ERROR"

    patch_scores = [patch_error(model, p) for p in patches]

    visual_score = np.mean(patch_scores)
    text_score = text_inconsistency(img)

    final_score = visual_score + (text_score * 0.001)

    result = "MERGED" if final_score > THRESHOLD else "NORMAL"

    print(f"{path} → {result} | Score:{final_score:.4f}")

    if show:
        heatmap = generate_heatmap(img, patch_scores)
        plt.imshow(cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB))
        plt.title(result)
        plt.axis("off")
        plt.show()

    return result

# -----------------------------
# DATASET TEST (FULL VIEW)
# -----------------------------
def test_dataset(folder="Claim_Documents"):

    print("\n🔍 Testing dataset...\n")

    images = []
    titles = []

    correct = 0
    total = 0

    for file in os.listdir(folder):

        if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        path = os.path.join(folder, file)

        print("Processing:", file)

        result = detect_image(path, show=False)

        if result == "ERROR":
            continue

        if result == "NORMAL":
            correct += 1

        total += 1

        img = cv2.imread(path)
        img = cv2.resize(img, (256,256))

        images.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        titles.append(f"{result}\n{file}")

    if total == 0:
        print("❌ No valid images found")
        return

    cols = 4
    rows = int(np.ceil(len(images)/cols))

    plt.figure(figsize=(15,10))

    for i in range(len(images)):
        plt.subplot(rows, cols, i+1)
        plt.imshow(images[i])
        plt.title(titles[i], fontsize=8)
        plt.axis("off")

    accuracy = (correct/total)*100

    plt.suptitle(f"Dataset Results | Accuracy: {accuracy:.2f}%", color="red")
    plt.tight_layout()
    plt.show()

    print("✅ Accuracy:", accuracy)

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":

    choice = input("Enter option (train / test / detect): ").strip().lower()

    if choice == "train":
        train()

    elif choice == "test":
        test_dataset()

    elif choice == "detect":
        path = input("Enter image path: ")
        detect_image(path)

    else:
        print("❌ Invalid choice")