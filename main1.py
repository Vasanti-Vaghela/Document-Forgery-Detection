import os
import cv2

from preprocessing.loader import load_input
from models.c4_removed_wrapper import run_c4
from models.c5_merge_wrapper import run_c5
from models.c9_partial_wrapper import run_c9

from engine.decision_engine import process_document
from utils.yaml_generator import create_yaml


OUTPUT_DIR = "final_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def draw_boxes(image, detections):
    for d in detections:
        x, y, w, h = d["bbox"]
        cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 2)
    return image


def run_pipeline(input_path):

    pages = load_input(input_path)

    all_yaml_data = []

    for idx, page in enumerate(pages):

        print(f"\n📄 Processing Page {idx+1}: {page}")

        all_detections = []

        # Run all models
        
        c4, _ = run_c4(page)
        c5, _ = run_c5(page)
        c9, _ = run_c9(page)

        all_detections.extend(c4)
        all_detections.extend(c5)
        all_detections.extend(c9)

        # Decision
        processed = process_document(page, all_detections)

        # Draw

        img = cv2.imread(page)
        img = draw_boxes(img, all_detections)


        img = draw_boxes(img, all_detections)

        out_img_path = os.path.join(OUTPUT_DIR, f"page_{idx+1}.png")
        cv2.imwrite(out_img_path, img)

        # YAML prepare
        yaml_input = []
        for item in processed:
            yaml_input.append({
                "bbox": item["bbox"],
                "category": item["Category_ID"]
            })

        yaml_text = create_yaml(yaml_input)

        yaml_path = os.path.join(OUTPUT_DIR, f"page_{idx+1}.yaml")
        with open(yaml_path, "w") as f:
            f.write(yaml_text)

        print(f"✅ Saved: {out_img_path}")
        print(f"✅ Saved: {yaml_path}")


def test_dataset(folder="Claim_Documents"):

    print("\n🔥 Testing full dataset...\n")

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        if not file.lower().endswith((".png",".jpg",".jpeg",".pdf")):
            continue

        print(f"\n🧪 Testing: {file}")
        run_pipeline(path)


if __name__ == "__main__":

    choice = input("Enter (run / test): ").strip().lower()

    if choice == "run":
        path = input("Enter file path: ")
        run_pipeline(path)

    elif choice == "test":
        test_dataset()

    else:
        print("Invalid option")