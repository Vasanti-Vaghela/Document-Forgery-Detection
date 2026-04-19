from PIL import Image, ImageChops, ImageEnhance
import os

# 🔹 Function
def ela_check(image_path, output_path="ela_output.jpg", quality=90):
    original = Image.open(image_path).convert('RGB')

    temp_path = "temp_ela.jpg"
    original.save(temp_path, 'JPEG', quality=quality)

    recompressed = Image.open(temp_path)

    diff = ImageChops.difference(original, recompressed)

    extrema = diff.getextrema()
    max_diff = max([ex[1] for ex in extrema])

    scale = 255.0 / max_diff if max_diff != 0 else 1

    enhancer = ImageEnhance.Brightness(diff)
    ela_image = enhancer.enhance(scale)

    ela_image.save(output_path)
    ela_image.show()

    os.remove(temp_path)

    return max_diff


# 🔹 MAIN BLOCK (yahi likhna hai end me)
if __name__ == "__main__":
    ela_check("testing1.jpeg", "ela1.jpg")
    ela_check("Testing2.jpeg", "ela2.jpg")
