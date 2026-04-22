from PIL import Image, ImageChops, ImageEnhance

def ela(image_path):
    original = Image.open(image_path).convert('RGB')

    # Save recompressed image
    temp_path = "temp.jpg"
    original.save(temp_path, 'JPEG', quality=90)

    recompressed = Image.open(temp_path)

    # Difference
    diff = ImageChops.difference(original, recompressed)

    # Enhance brightness
    enhancer = ImageEnhance.Brightness(diff)
    ela_image = enhancer.enhance(5)

    ela_image.show()

ela("test.jpg")