def create_yaml(detections):
    yaml_data = "annotations:\n"

    for det in detections:
        x, y, w, h = det["bbox"]
        category = det["category"]

        yaml_data += f"""  - category: {category}
    x: {x}
    y: {y}
    w: {w}
    h: {h}
"""

    return yaml_data