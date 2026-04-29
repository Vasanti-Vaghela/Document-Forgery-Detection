import json
from yaml_generator import create_yaml


# CATEGORY DECISION FUNCTION
def decide_category(features):

    if features.get("duplicate"):
        return "C1"

    if features.get("overwrite"):
        return "C2"

    if features.get("added"):
        return "C3"

    if features.get("removed"):
        return "C4"

    if features.get("merged"):
        return "C5"

    if features.get("watermark"):
        return "C6"

    if features.get("spacing"):
        return "C7"

    if features.get("ai_generated"):
        return "C8"

    if features.get("partial_edit"):
        return "C9"

    return None   # IMPORTANT FIX


# PROCESS DOCUMENT FUNCTION
def process_document(file_name, detections):

    results = []

    for item in detections:
        category = decide_category(item["features"])

        # Skip invalid detections
        if category is None:
            continue

        results.append({
            "link": file_name,
            "page_number": 1,
            "bbox": item["bbox"],
            "Category_ID": category
        })

    return results

# MAIN BLOCK (TESTING)

if __name__ == "__main__":

    # Dummy detections (testing)
    detections = [
        {
            "bbox": [10, 20, 100, 200],
            "features": {"duplicate": True}
        },
        {
            "bbox": [50, 60, 150, 250],
            "features": {"overwrite": True}
        },
        {
            "bbox": [80, 90, 180, 280],
            "features": {"ai_generated": True}
        },
        {
            "bbox": [100, 120, 200, 300],
            "features": {}   # should be skipped
        }
    ]

    # JSON OUTPUT
    output = process_document("sample.pdf", detections)

    print("JSON Output:\n")
    print(json.dumps(output, indent=2))


    # YAML OUTPUT
    yaml_output = create_yaml([
        {
            "bbox": item["bbox"],
            "category": item["Category_ID"]
        }
        for item in output
    ])

    print("\nYAML Output:\n")
    print(yaml_output)