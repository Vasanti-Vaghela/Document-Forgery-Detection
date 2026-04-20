# # from PIL import Image, ImageChops, ImageEnhance
# # import os

# # # 🔹 Function
# # def ela_check(image_path, output_path="ela_output.jpg", quality=90):
# #     original = Image.open(image_path).convert('RGB')

# #     temp_path = "temp_ela.jpg"
# #     original.save(temp_path, 'JPEG', quality=quality)

# #     recompressed = Image.open(temp_path)

# #     diff = ImageChops.difference(original, recompressed)

# #     extrema = diff.getextrema()
# #     max_diff = max([ex[1] for ex in extrema])

# #     scale = 255.0 / max_diff if max_diff != 0 else 1

# #     enhancer = ImageEnhance.Brightness(diff)
# #     ela_image = enhancer.enhance(scale)

# #     ela_image.save(output_path)
# #     ela_image.show()

# #     os.remove(temp_path)

# #     return max_diff

# # if __name__ == "__main__":
# #     result1 = ela_check("testing1.jpeg", "ela1.jpg")
# #     result2 = ela_check("Testing2.jpeg", "ela2.jpg")

# # if result1 > 20:
# #     print("Image 1 suspicious")
# # else:
# #     print("Image 1 Normal")


# # if result2 > 20:
# #     print("Image 2 suspicious")
# # else:
# #     print("Image 2 Normal")

# #testing 2

# # from PIL import Image, ImageChops, ImageEnhance
# # import os
# # import numpy as np

# # # 🔹 Function
# # def ela_check(image_path, output_path="ela_output.jpg", quality=90):
# #     original = Image.open(image_path).convert('RGB')

# #     temp_path = "temp_ela.jpg"
# #     original.save(temp_path, 'JPEG', quality=quality)

# #     recompressed = Image.open(temp_path)

# #     # Difference
# #     diff = ImageChops.difference(original, recompressed)

# #     # Brightness scale
# #     extrema = diff.getextrema()
# #     max_diff = max([ex[1] for ex in extrema])
# #     scale = 255.0 / max_diff if max_diff != 0 else 1

# #     enhancer = ImageEnhance.Brightness(diff)
# #     ela_image = enhancer.enhance(scale)

# #     # Save & show
# #     ela_image.save(output_path)
# #     ela_image.show()

# #     os.remove(temp_path)

# #     # 🔥 NEW: Better detection (bright pixels)
# #     ela_array = np.array(ela_image)
# #     bright_pixels = np.sum(ela_array > 200)

# #     return max_diff, bright_pixels


# # # 🔹 MAIN BLOCK
# # if __name__ == "__main__":
# #     result1, bright1 = ela_check("testing1.jpeg", "ela1.jpg")
# #     result2, bright2 = ela_check("Testing2.jpeg", "ela2.jpg")
# #     result3, bright3 = ela_check("Testing3.jpeg", "ela3.jpg")

# #     print("Image1 max_diff:", result1, " bright_pixels:", bright1)
# #     print("Image2 max_diff:", result2, " bright_pixels:", bright2)
# #     print("Image3 max_diff:", result3, " bright_pixels:", bright3)

# #     # 🔥 Decision (better logic)
# #     if bright1 > 30:
# #         print("⚠️ Image 1 suspicious")
# #     else:
# #         print("✅ Image 1 normal")

# #     if bright2 > 30:
# #         print("⚠️ Image 2 suspicious")
# #     else:
# #         print("✅ Image 2 normal")

# #     if bright3 > 30:
# #         print("⚠️ Image 3 suspicious")
# #     else:
# #         print("✅ Image 3 normal")

# #testing 3 (75%)


# from PIL import Image, ImageChops, ImageEnhance
# import os
# import numpy as np

# # 🔹 Function
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

#     # Save & show
#     ela_image.save(output_path)
#     ela_image.show()

#     os.remove(temp_path)

#     # 🔥 Better detection
#     ela_array = np.array(ela_image)

#     bright_pixels = np.sum(ela_array > 200)

#     height, width, _ = ela_array.shape
#     total_pixels = height * width

#     ratio = bright_pixels / total_pixels   # ⭐ important

#     return max_diff, bright_pixels, ratio


# # 🔹 Decision function (SMART LOGIC)
# # def check(max_diff, bright_pixels, ratio):
# #     if max_diff > 18 and ratio > 0.00002:
# #         return "⚠️ suspicious"
# #     else:
# #         return "✅ normal"
    
# # def check(max_diff, bright_pixels, ratio):
# #     # Strong signal
# #     if max_diff > 20:
# #         return "⚠️ suspicious"

# #     # Medium signal (distributed edits)
# #     if ratio > 0.00005:
# #         return "⚠️ suspicious"

# #     # Backup rule (noise vs real edit separate karne ke liye)
# #     if bright_pixels > 120 and ratio < 0.00002:
# #         return "✅ normal"

# #     return "✅ normal"

# def check(max_diff, bright_pixels, ratio):
#     # 1) Strong, spread edits
#     if ratio > 0.00005:
#         return "⚠️ suspicious"

#     # 2) Strong local edit (intense + enough bright area)
#     if max_diff > 22 and bright_pixels > 40:
#         return "⚠️ suspicious"

#     # 3) Noise / compression case (high max_diff but very low spread)
#     if ratio < 0.00002 and bright_pixels < 30:
#         return "✅ normal"

#     # 4) Default
#     return "✅ normal"


# # 🔹 MAIN BLOCK
# if __name__ == "__main__":
#     max1, bright1, ratio1 = ela_check("testing1.jpeg", "ela1.jpg")
#     max2, bright2, ratio2 = ela_check("Testing2.jpeg", "ela2.jpg")
#     max3, bright3, ratio3 = ela_check("Testing3.jpeg", "ela3.jpg")
#     max4, bright4, ratio4 = ela_check("Testing4.jpeg", "ela4.jpg")
#     max5, bright5, ratio5 = ela_check("testing5.jpeg", "ela5.jpg")
#     max6, bright6, ratio6 = ela_check("Testing6.jpeg", "ela6.jpg")
#     max7, bright7, ratio7 = ela_check("Testing7.jpeg", "ela7.jpg")
#     max8, bright8, ratio8 = ela_check("Testing8.jpeg", "ela8.jpg")


#     print("Image1:", max1, bright1, ratio1)
#     print("Image2:", max2, bright2, ratio2)
#     print("Image3:", max3, bright3, ratio3)
#     print("Image4:", max4, bright4, ratio4)
#     print("Image5:", max5, bright5, ratio5)
#     print("Image6:", max6, bright6, ratio6)
#     print("Image7:", max7, bright7, ratio7)
#     print("Image8:", max8, bright8, ratio8)

#     print("Image1:", check(max1, bright1, ratio1))
#     print("Image2:", check(max2, bright2, ratio2))
#     print("Image3:", check(max3, bright3, ratio3))
#     print("Image4:", check(max4, bright4, ratio4))
#     print("Image5:", check(max5, bright5, ratio5))
#     print("Image6:", check(max6, bright6, ratio6))
#     print("Image7:", check(max7, bright7, ratio7))
#     print("Image8:", check(max8, bright8, ratio8))



#testing4 (75% preferred)



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


#testing (50%)

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

#     bright_pixels = np.sum(gray > 200)

#     height, width = gray.shape
#     total_pixels = height * width

#     ratio = bright_pixels / total_pixels

#     # 🔥 Dynamic thresholds (IMPORTANT)
#     p95 = np.percentile(gray, 95)
#     p99 = np.percentile(gray, 99)

#     return max_diff, bright_pixels, ratio, p95, p99


# # 🔹 SMART DECISION FUNCTION (UPGRADED)
# def check(max_diff, bright_pixels, ratio, p95, p99):

#     score = 0

#     # 🔥 Strong intensity signal
#     if max_diff > 22:
#         score += 2

#     # 🔥 Spread signal (MOST IMPORTANT)
#     if ratio > 0.00003:
#         score += 2

#     # 🔥 Area signal
#     if bright_pixels > 60:
#         score += 1

#     # 🔥 Distribution signal (NEW 🔥)
#     if p99 > 180:
#         score += 1

#     # ❌ Noise case (reduce score)
#     if ratio < 0.000015 and bright_pixels < 25:
#         score -= 2

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

#     for i, img in enumerate(images):
#         max_d, bright, ratio, p95, p99 = ela_check(img, f"ela{i+1}.jpg")
#         results.append((img, max_d, bright, ratio, p95, p99))

#     print("\n--- RAW VALUES ---")
#     for i, (img, max_d, bright, ratio, p95, p99) in enumerate(results):
#         print(f"Image{i+1}: max={max_d}, bright={bright}, ratio={ratio}, p99={p99}")

#     print("\n--- FINAL RESULT ---")
#     for i, (img, max_d, bright, ratio, p95, p99) in enumerate(results):
#         print(f"Image{i+1}: {check(max_d, bright, ratio, p95, p99)}")



#testing (50%)

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

#     # ✅ FIX 1: LOWER threshold (IMPORTANT)
#     bright_pixels = np.sum(gray > 40)

#     height, width = gray.shape
#     total_pixels = height * width

#     # ✅ FIX 2: proper ratio
#     ratio = bright_pixels / total_pixels

#     # ✅ FIX 3: better percentiles
#     p95 = np.percentile(gray, 95)
#     p99 = np.percentile(gray, 99)

#     return max_diff, bright_pixels, ratio, p95, p99


# # 🔹 SMART DECISION FUNCTION (FINAL TUNED)
# def check(max_diff, bright_pixels, ratio, p95, p99):

#     score = 0

#     # 🔥 Strong intensity
#     if max_diff > 22:
#         score += 2

#     # 🔥 Spread signal (MOST IMPORTANT)
#     if ratio > 0.00001:
#         score += 2

#     # 🔥 Area signal
#     if bright_pixels > 50:
#         score += 1

#     # 🔥 Distribution (softer threshold)
#     if p99 > 120:
#         score += 1

#     # ❌ Noise case (important)
#     if ratio < 0.000005 and bright_pixels < 20:
#         score -= 2

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

#     for i, img in enumerate(images):
#         max_d, bright, ratio, p95, p99 = ela_check(img, f"ela{i+1}.jpg")
#         results.append((img, max_d, bright, ratio, p95, p99))

#     print("\n--- RAW VALUES ---")
#     for i, (img, max_d, bright, ratio, p95, p99) in enumerate(results):
#         print(f"Image{i+1}: max={max_d}, bright={bright}, ratio={ratio}, p99={p99}")

#     print("\n--- FINAL RESULT ---")
#     for i, (img, max_d, bright, ratio, p95, p99) in enumerate(results):
#         print(f"Image{i+1}: {check(max_d, bright, ratio, p95, p99)}")



# testing (25% accuracy)

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