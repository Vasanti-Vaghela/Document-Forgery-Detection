# testing4 (75% preferred)



# from PIL import Image, ImageChops, ImageEnhance
# import os
# import numpy as np


# # 🔹 ELA FUNCTION
# def ela_check(image_path, output_path="ela_output.jpg", quality=90):
#     original = Image.open(image_path).convert('RGB')

#     temp_path = "temp_ela.jpg"
#     original.save(temp_path, 'JPEG', quality=quality)

#     recompressed = Image.open(temp_path)

#     # Difference
#     diff = ImageChops.difference(original, recompressed)

#     # Brightness scale
#     extrema = diff.getextrema()
#     max_diff = max([ex[1] for ex in extrema])
#     scale = 255.0 / max_diff if max_diff != 0 else 1

#     enhancer = ImageEnhance.Brightness(diff)
#     ela_image = enhancer.enhance(scale)

#     # Save output
#     ela_image.save(output_path)
#     # ela_image.show()   # ❌ comment kiya (har image open karna annoying hota hai)

#     os.remove(temp_path)

#     # 🔥 Feature extraction
#     ela_array = np.array(ela_image)

#     bright_pixels = np.sum(ela_array > 200)

#     height, width, _ = ela_array.shape
#     total_pixels = height * width

#     ratio = bright_pixels / total_pixels

#     return max_diff, bright_pixels, ratio


# # 🔹 SMART DECISION FUNCTION (final tuned)
# def check(max_diff, bright_pixels, ratio):

#     # ✅ Spread editing (most reliable)
#     if ratio > 0.00005:
#         return "⚠️ suspicious"

#     # ✅ Local strong editing
#     if max_diff > 22 and bright_pixels > 40:
#         return "⚠️ suspicious"

#     # ✅ Noise / compression case (false positive avoid)
#     if ratio < 0.00002 and bright_pixels < 30:
#         return "✅ normal"

#     return "✅ normal"


# # 🔹 MAIN BLOCK
# if __name__ == "__main__":

#     images = [
#         "testing1.jpeg",
#         "Testing2.jpeg",
#         "Testing3.jpeg",
#         "Testing4.jpeg",
#         "testing5.jpeg",
#         "Testing6.jpeg",
#         "Testing7.jpeg",
#         "Testing8.jpeg"
#     ]

#     results = []

#     # 🔥 LOOP (clean code instead of repeat)
#     for i, img in enumerate(images):
#         max_d, bright, ratio = ela_check(img, f"ela{i+1}.jpg")
#         results.append((img, max_d, bright, ratio))

#     print("\n--- RAW VALUES ---")
#     for i, (img, max_d, bright, ratio) in enumerate(results):
#         print(f"Image{i+1}: {max_d}, {bright}, {ratio}")

#     print("\n--- FINAL RESULT ---")
#     for i, (img, max_d, bright, ratio) in enumerate(results):
#         print(f"Image{i+1}: {check(max_d, bright, ratio)}")


# testing7 (25% accuracy)

# from PIL import Image, ImageChops, ImageEnhance
# import os
# import numpy as np


# # 🔹 ELA FUNCTION
# def ela_check(image_path, output_path="ela_output.jpg", quality=90):
#     original = Image.open(image_path).convert('RGB')

#     temp_path = "temp_ela.jpg"
#     original.save(temp_path, 'JPEG', quality=quality)

#     recompressed = Image.open(temp_path)

#     # Difference
#     diff = ImageChops.difference(original, recompressed)

#     # Brightness scale
#     extrema = diff.getextrema()
#     max_diff = max([ex[1] for ex in extrema])
#     scale = 255.0 / max_diff if max_diff != 0 else 1

#     enhancer = ImageEnhance.Brightness(diff)
#     ela_image = enhancer.enhance(scale)

#     # Save output
#     ela_image.save(output_path)
#     os.remove(temp_path)

#     # 🔥 Feature extraction
#     ela_array = np.array(ela_image)
#     gray = ela_array.mean(axis=2)

#     # ✅ Better threshold
#     bright_pixels = np.sum(gray > 50)

#     height, width = gray.shape
#     total_pixels = height * width

#     ratio = bright_pixels / total_pixels

#     # Percentiles
#     p95 = np.percentile(gray, 95)
#     p99 = np.percentile(gray, 99)

#     return max_diff, bright_pixels, ratio, p95, p99


# # 🔹 SMART DECISION (RELATIVE + SCORE)
# def check(max_diff, bright, ratio, p99, avg_bright, avg_ratio):

#     score = 0

#     # 🔥 Strong signal
#     if max_diff > 24:
#         score += 2

#     # 🔥 Relative comparison (MOST IMPORTANT)
#     if bright > avg_bright * 1.6:
#         score += 2

#     if ratio > avg_ratio * 1.4:
#         score += 2

#     # 🔥 Distribution
#     if p99 > 130:
#         score += 1

#     # ❌ Noise case
#     if ratio < avg_ratio * 0.5:
#         score -= 1

#     # 🎯 Final decision
#     if score >= 3:
#         return "⚠️ suspicious"
#     else:
#         return "✅ normal"


# # 🔹 MAIN BLOCK
# if __name__ == "__main__":

#     images = [
#         "testing1.jpeg",
#         "Testing2.jpeg",
#         "Testing3.jpeg",
#         "Testing4.jpeg",
#         "testing5.jpeg",
#         "Testing6.jpeg",
#         "Testing7.jpeg",
#         "Testing8.jpeg"
#     ]

#     results = []

#     # 🔥 Step 1: Extract features
#     for i, img in enumerate(images):
#         max_d, bright, ratio, p95, p99 = ela_check(img, f"ela{i+1}.jpg")
#         results.append((img, max_d, bright, ratio, p95, p99))

#     # 🔥 Step 2: Calculate averages (IMPORTANT)
#     avg_bright = sum(r[2] for r in results) / len(results)
#     avg_ratio = sum(r[3] for r in results) / len(results)

#     print("\n--- RAW VALUES ---")
#     for i, (img, max_d, bright, ratio, p95, p99) in enumerate(results):
#         print(f"Image{i+1}: max={max_d}, bright={bright}, ratio={ratio}, p99={p99}")

#     print("\n--- FINAL RESULT ---")
#     for i, (img, max_d, bright, ratio, p95, p99) in enumerate(results):
#         result = check(max_d, bright, ratio, p99, avg_bright, avg_ratio)
#         print(f"Image{i+1}: {result}")