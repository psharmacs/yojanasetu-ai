import pandas as pd
from sentence_transformers import SentenceTransformer, util
import streamlit as st
import pickle
import os

@st.cache_resource
def load_data_and_model():
    # 1. Load the FULL dataset
    df = pd.read_csv('updated_data.csv')
    df = df.fillna("Information not specified")
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # 2. Embedding Cache (Scaling for 3400+ schemes)
    embedding_cache_path = 'scheme_embeddings.pkl'
    
    if os.path.exists(embedding_cache_path):
        # Instant load if already calculated
        with open(embedding_cache_path, 'rb') as f:
            item_embeddings = pickle.load(f)
    else:
        # Calculate once (will take ~1 min the first time)
        text_to_index = df['scheme_name'] + " " + df['details'] + " " + df['schemeCategory']
        item_embeddings = model.encode(text_to_index.tolist(), convert_to_tensor=True)
        with open(embedding_cache_path, 'wb') as f:
            pickle.dump(item_embeddings, f)
            
    return df, model, item_embeddings

def find_schemes(user_query, selected_state="National (All India)", top_n=5):
    df, model, item_embeddings = load_data_and_model()
    query_embedding = model.encode(user_query, convert_to_tensor=True)
    
    # Get high volume of hits to filter properly
    hits = util.semantic_search(query_embedding, item_embeddings, top_k=100)
    best_indices = [hit['corpus_id'] for hit in hits[0]]
    results = df.iloc[best_indices]
    
    # Universal Filter Logic
    if selected_state != "National (All India)":
        # Search for either the specific State/UT OR Central/National schemes
        final_results = results[
            (results['level'].str.contains('Central', case=False, na=False)) | 
            (results['level'].str.contains('National', case=False, na=False)) | 
            (results['level'].str.contains(selected_state, case=False, na=False))
        ]
    else:
        # If National is selected, focus on Central/National but allow broad matches
        final_results = results
        
    return final_results.head(top_n)