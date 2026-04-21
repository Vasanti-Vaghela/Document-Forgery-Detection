# =========================
# 🔴 1. IMPORT LIBRARIES
# =========================
import pandas as pd
import numpy as np
import re
from rapidfuzz import fuzz, process
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt


# =========================
# 🔴 2. LOAD DATASET
# =========================
file_path = "data.csv"   # 👉 Change if needed

df = pd.read_csv(file_path)

print("Columns in dataset:", df.columns)
print("\nSample Data:\n", df.head())


# =========================
# 🔴 3. SELECT COLUMNS
# =========================
text_columns = ['name', 'address']   # 👉 Change as per dataset

df['combined'] = df[text_columns].fillna('').agg(' '.join, axis=1)


# =========================
# 🔴 4. CLEAN TEXT
# =========================
stopwords = ['hospital', 'hosp', 'clinic', 'center', 'medicare']

def clean_text(text):
    text = text.lower()
    
    for word in stopwords:
        text = text.replace(word, '')
    
    text = re.sub(r'[^a-z0-9 ]', '', text)
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

df['cleaned'] = df['combined'].apply(clean_text)

print("\nCleaned Data Sample:\n", df['cleaned'].head())


# =========================
# 🔴 5. FUZZY MATCHING (OPTIMIZED)
# =========================
fuzzy_threshold = 85
fuzzy_duplicates = []

texts = df['cleaned'].tolist()

for i, text in enumerate(texts):
    matches = process.extract(text, texts, limit=5)
    
    for match_text, score, j in matches:
        if i != j and score > fuzzy_threshold:
            fuzzy_duplicates.append((i, j, score))

print("\nFuzzy Duplicates Found:", len(fuzzy_duplicates))


# =========================
# 🔴 6. TF-IDF + COSINE SIMILARITY
# =========================
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['cleaned'])

similarity_matrix = cosine_similarity(X)

tfidf_threshold = 0.8
tfidf_duplicates = []

for i in range(len(df)):
    for j in range(i+1, len(df)):
        if similarity_matrix[i][j] > tfidf_threshold:
            tfidf_duplicates.append((i, j, similarity_matrix[i][j]))

print("TF-IDF Duplicates Found:", len(tfidf_duplicates))


# =========================
# 🔴 7. COMBINE RESULTS
# =========================
final_duplicates = set(fuzzy_duplicates) | set(tfidf_duplicates)

print("Total Unique Duplicates:", len(final_duplicates))


# =========================
# 🔴 8. SHOW RESULTS
# =========================
def show_duplicates(duplicates, method_name):
    print(f"\nTop {method_name} Duplicates:\n")
    
    for i, j, score in list(duplicates)[:5]:
        print(f"Row {i} ↔ Row {j} | Score: {score:.2f}")
        print("Text 1:", df['combined'][i])
        print("Text 2:", df['combined'][j])
        print("-"*50)

show_duplicates(final_duplicates, "Final")


# =========================
# 🔴 9. SAVE OUTPUT
# =========================
output = []

for i, j, score in final_duplicates:
    output.append({
        "row_1": i,
        "row_2": j,
        "similarity": score,
        "text_1": df['combined'][i],
        "text_2": df['combined'][j]
    })

output_df = pd.DataFrame(output)

output_df.to_csv("duplicates_output.csv", index=False)

print("\n✅ Duplicate results saved to duplicates_output.csv")


# =========================
# 🔴 10. VISUALIZATION
# =========================
counts = [len(fuzzy_duplicates), len(tfidf_duplicates)]

plt.bar(['Fuzzy', 'TF-IDF'], counts)
plt.title("Duplicate Detection Comparison")
plt.xlabel("Methods")
plt.ylabel("Number of Duplicates")
plt.show()