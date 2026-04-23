#text_columns = ['name', 'address']   # change this based on dataset

#df['combined'] = df[text_columns].fillna('').agg(' '.join, axis=1)
import pandas as pd
import numpy as np
import re
from rapidfuzz import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =========================
# 🔴 STEP 1: LOAD DATASET
# =========================
# 👉 CHANGE THIS: file name as given in hackathon
file_path = "data.csv"  

df = pd.read_csv(file_path)   # 👉 if excel: use pd.read_excel("file.xlsx")

print("Columns in dataset:", df.columns)
print("\nSample Data:\n", df.head())


# =========================
# 🔴 STEP 2: SELECT COLUMNS
# =========================
# 👉 CHANGE THESE: based on dataset columns
# Example: ['hospital_name', 'address', 'city']
text_columns = ['name', 'address']  

df['combined'] = df[text_columns].fillna('').agg(' '.join, axis=1)


# =========================
# STEP 3: BEFORE CLEANING
# =========================
print("\nBefore Cleaning:\n", df['combined'].head(5))


# =========================
# 🔴 STEP 4: CLEAN TEXT
# =========================
def clean_text(text):
    text = text.lower()
    
#👉 OPTIONAL: remove common hospital words (improves accuracy)
    text = re.sub(r'hospital|hosp|clinic|medicare', '', text)
    
    text = re.sub(r'[^a-z0-9 ]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

df['cleaned'] = df['combined'].apply(clean_text)


# =========================
# STEP 5: AFTER CLEANING
# =========================
print("\nAfter Cleaning:\n", df['cleaned'].head(5))


# =========================
# 🔴 STEP 6: (OPTIONAL) ID-BASED DUPLICATES
# =========================
# 👉 CHANGE COLUMN NAME if dataset has ID (like 'registration_id')
id_column = None  # e.g., 'registration_id'

if id_column and id_column in df.columns:
    exact_duplicates = df[df.duplicated(id_column)]
    print("\nExact duplicates based on ID:", len(exact_duplicates))


# =========================
# 🔴 STEP 7: FUZZY MATCHING
# =========================
# 👉 CHANGE THRESHOLD (80–90 best)
fuzzy_threshold = 85  

fuzzy_duplicates = []

for i in range(len(df)):
    for j in range(i+1, len(df)):
        score = fuzz.ratio(df['cleaned'][i], df['cleaned'][j])
        if score > fuzzy_threshold:
            fuzzy_duplicates.append((i, j, score))

print("\nFuzzy Duplicates Found:", len(fuzzy_duplicates))


# =========================
# 🔴 STEP 8: TF-IDF + COSINE
# =========================
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['cleaned'])

similarity_matrix = cosine_similarity(X)

# 👉 CHANGE THRESHOLD (0.75–0.85 best for messy data)
tfidf_threshold = 0.8  

tfidf_duplicates = []

for i in range(len(df)):
    for j in range(i+1, len(df)):
        if similarity_matrix[i][j] > tfidf_threshold:
            tfidf_duplicates.append((i, j, similarity_matrix[i][j]))

print("TF-IDF Duplicates Found:", len(tfidf_duplicates))


# =========================
# STEP 9: SHOW RESULTS
# =========================
def show_duplicates(duplicates, method_name):
    print(f"\nTop {method_name} Duplicates:\n")
    for i, j, score in duplicates[:5]:
        print(f"Row {i} ↔ Row {j} | Score: {score:.2f}")
        print("Text 1:", df['combined'][i])
        print("Text 2:", df['combined'][j])
        print("-"*50)

show_duplicates(fuzzy_duplicates, "Fuzzy")
show_duplicates(tfidf_duplicates, "TF-IDF")


# =========================
# STEP 10: SAVE OUTPUT
# =========================
output = []

for i, j, score in tfidf_duplicates:
    output.append({
        "row_1": i,
        "row_2": j,
        "similarity": score,
        "text_1": df['combined'][i],
        "text_2": df['combined'][j]
    })

output_df = pd.DataFrame(output)

# 👉 CHANGE FILE NAME if needed
output_df.to_csv("duplicates_output.csv", index=False)

print("\n  Duplicate results saved to duplicates_output.csv")