# Metadata & Scoring Module

## Overview

This module is responsible for analyzing metadata and generating decision outputs for document forgery detection. It acts as a central decision engine that receives inputs from different detection modules and produces structured output in the required submission format.

---

## Objectives

* Analyze detection signals (duplicate, overwrite, spacing, watermark)
* Assign appropriate Category ID (C1–C10)
* Generate structured JSON output for submission
* Support multiple tampered regions in a document

---

## Category Decision Logic

The system uses rule-based conditions to assign categories:

* **C1** → Copy-paste detected (duplicate content)
* **C2** → Overwriting detected
* **C6** → Watermark removal detected
* **C7** → Irregular spacing detected
* **C10** → No forgery detected

### Decision Function

```python
def decide_category(duplicate, overwrite, spacing, watermark):
    if duplicate:
        return "C1"
    elif overwrite:
        return "C2"
    elif spacing:
        return "C7"
    elif watermark:
        return "C6"
    else:
        return "C10"
```

---

## JSON Output Generation

The module generates output in the required hackathon format:

### Single Output Format

```json
[
  {
    "link": "sample.pdf",
    "page_number": 1,
    "category_id": "C1"
  }
]
```

---

## Multiple Detection Handling

The system supports multiple tampered regions using bounding boxes.

### Example Output

```json
[
  {
    "link": "sample.pdf",
    "page_number": 1,
    "bbox": [10, 20, 100, 200],
    "category_id": "C1"
  },
  {
    "link": "sample.pdf",
    "page_number": 1,
    "bbox": [50, 60, 150, 250],
    "category_id": "C2"
  }
]
```

---

## Multi-Region Output Function

```python
def generate_multiple_outputs(file_name, detections):
    output = []
    for det in detections:
        item = {
            "link": file_name,
            "page_number": 1,
            "bbox": det["bbox"],
            "category_id": det["category"]
        }
        output.append(item)
    return output
```

---

## Key Learnings

* Python function structure and execution flow
* Conditional logic for classification
* JSON formatting for structured output
* Handling multiple detections in a single document

---

## Role in System

This module acts as the **final decision layer**, integrating outputs from:

* ELA Module (image inconsistencies)
* OCR Module (text extraction)
* Duplicate Detection Module

It ensures correct classification and submission-ready output generation.

---

## Future Improvements

* Integrate real-time inputs from other modules
* Add metadata-based anomaly detection
* Improve scoring logic for prioritization
* Optimize for real-world document variations

---
