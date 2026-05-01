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

    return None


def process_document(file_name, detections):

    results = []

    for item in detections:
        category = decide_category(item["features"])

        if category is None:
            continue

        results.append({
            "link": file_name,
            "page_number": 1,
            "bbox": item["bbox"],
            "Category_ID": category
        })

    if len(results) == 0:
        results.append({
            "link": file_name,
            "page_number": 1,
            "bbox": [0,0,0,0],
            "Category_ID": "C10"
        })

    return results