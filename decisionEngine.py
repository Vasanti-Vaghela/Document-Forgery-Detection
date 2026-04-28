import json

# Category decide function
def decide_category(features):

    if features.get("duplicate"):
        return "C1"

    elif features.get("overwrite"):
        return "C2"

    elif features.get("added"):
        return "C3"

    elif features.get("removed"):
        return "C4"

    elif features.get("merged"):
        return "C5"

    elif features.get("watermark"):
        return "C6"

    elif features.get("spacing"):
        return "C7"

    elif features.get("ai_generated"):
        return "C8"

    elif features.get("partial_edit"):
        return "C9"

    else:
        return "C10"


# Process full document (multiple regions)
def process_document(file_name, detections):

    results = []

    for item in detections:
        category = decide_category(item["features"])

        results.append({
            "link": file_name,
            "page_number": 1,
            "bbox": item["bbox"],
            "Category_ID": category
        })

    return results


# MAIN BLOCK 
if __name__ == "__main__":

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
    }
]

    output = process_document("sample.pdf", detections)

    print(json.dumps(output, indent=2))