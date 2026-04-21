import streamlit as st
import pandas as pd
import re
from rapidfuzz import process, fuzz
import networkx as nx

st.title("🔍 Duplicate Detection System")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    st.write("### Preview Data")
    st.dataframe(df.head())

    text_columns = st.multiselect("Select text columns", df.columns)

    if text_columns:
        df['combined'] = df[text_columns].fillna('').agg(' '.join, axis=1)

        def clean_text(text):
            text = text.lower()
            text = re.sub(r'hospital|hosp|clinic|medicare', '', text)
            text = re.sub(r'[^a-z0-9 ]', '', text)
            return re.sub(r'\s+', ' ', text).strip()

        df['cleaned'] = df['combined'].apply(clean_text)

        threshold = st.slider("Similarity Threshold", 70, 100, 85)

        if st.button("Run Duplicate Detection"):

            df['block'] = df['cleaned'].str[:3]

            G = nx.Graph()

            for i in range(len(df)):
                G.add_node(i)

            for block, group in df.groupby('block'):
                texts = group['cleaned'].tolist()
                indices = group.index.tolist()

                scores = process.cdist(texts, texts, scorer=fuzz.token_sort_ratio)

                for i in range(len(texts)):
                    for j in range(i+1, len(texts)):
                        if scores[i][j] > threshold:
                            G.add_edge(indices[i], indices[j])

            clusters = list(nx.connected_components(G))

            output = []
            cluster_id = 0

            for cluster in clusters:
                if len(cluster) > 1:
                    for idx in cluster:
                        output.append({
                            "cluster_id": cluster_id,
                            "row": idx,
                            "text": df['combined'][idx]
                        })
                    cluster_id += 1

            output_df = pd.DataFrame(output)

            st.write("### Duplicate Clusters Found:", cluster_id)
            st.dataframe(output_df)

            csv = output_df.to_csv(index=False).encode('utf-8')

            st.download_button(
                "Download Results",
                csv,
                "duplicates.csv",
                "text/csv"
            )