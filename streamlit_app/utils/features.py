"""
Feature Engineering Module
Extracts NLP and readability features from text
"""

import re
import numpy as np
import pandas as pd
import nltk
import textstat
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from typing import Dict, List, Tuple
import streamlit as st


# Download NLTK data if not available
def ensure_nltk_data():
    """Download required NLTK data"""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)


@st.cache_resource
def load_embedding_model():
    """Load and cache the sentence transformer model"""
    return SentenceTransformer('all-MiniLM-L6-v2')


def clean_text(text: str) -> str:
    """
    Clean and normalize text.
    
    Args:
        text: Raw text string
        
    Returns:
        Cleaned text (lowercase, normalized whitespace)
    """
    text = str(text).lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_basic_features(text: str) -> Dict[str, any]:
    """
    Extract basic text features: word count, sentence count, readability.
    
    Args:
        text: Input text
        
    Returns:
        Dictionary with basic features
    """
    ensure_nltk_data()
    
    clean = clean_text(text)
    
    # Basic counts
    word_count = len(clean.split())
    sentence_count = len(nltk.sent_tokenize(clean)) if clean else 0
    
    # Readability
    flesch_score = textstat.flesch_reading_ease(clean) if clean else 0
    
    # Average word length
    words = clean.split()
    avg_word_length = np.mean([len(w) for w in words]) if words else 0
    
    return {
        'word_count': word_count,
        'sentence_count': sentence_count,
        'flesch_reading_ease': flesch_score,
        'avg_word_length': float(avg_word_length)
    }


def extract_keywords(texts: List[str], top_n: int = 5) -> List[str]:
    """
    Extract top keywords using TF-IDF.
    
    Args:
        texts: List of text documents
        top_n: Number of top keywords to extract
        
    Returns:
        List of keyword strings (pipe-separated)
    """
    if not texts or all(not t for t in texts):
        return [''] * len(texts)
    
    # Clean texts
    clean_texts = [clean_text(t) if t else '' for t in texts]
    
    # TF-IDF
    vectorizer = TfidfVectorizer(
        stop_words='english',
        max_features=1000,
        min_df=min(2, len(texts))  # Adjust for small datasets
    )
    
    try:
        tfidf_matrix = vectorizer.fit_transform(clean_texts)
        feature_names = vectorizer.get_feature_names_out()
        
        keywords_list = []
        dense_matrix = tfidf_matrix.toarray()
        
        for doc_vector in dense_matrix:
            sorted_indices = doc_vector.argsort()[-top_n:][::-1]
            keywords = [feature_names[i] for i in sorted_indices if doc_vector[i] > 0]
            keywords_list.append("|".join(keywords))
        
        return keywords_list
    except Exception as e:
        print(f"Keyword extraction error: {e}")
        return [''] * len(texts)


def generate_embeddings(texts: List[str]) -> np.ndarray:
    """
    Generate sentence embeddings using transformer model.
    
    Args:
        texts: List of text documents
        
    Returns:
        Numpy array of embeddings (n_docs x 384)
    """
    model = load_embedding_model()
    clean_texts = [clean_text(t) if t else '' for t in texts]
    embeddings = model.encode(clean_texts, show_progress_bar=False)
    return embeddings


def extract_all_features(text: str, include_embeddings: bool = False) -> Dict[str, any]:
    """
    Extract all features from a single text document.
    
    Args:
        text: Input text
        include_embeddings: Whether to include semantic embeddings
        
    Returns:
        Dictionary with all features
    """
    features = extract_basic_features(text)
    
    # Keywords (single document - may not be meaningful)
    keywords = extract_keywords([text], top_n=5)[0]
    features['top_keywords'] = keywords
    
    # Embeddings
    if include_embeddings:
        embedding = generate_embeddings([text])[0]
        features['embedding'] = embedding.tolist()
    
    return features


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate cosine similarity between two texts using embeddings.
    
    Args:
        text1: First text
        text2: Second text
        
    Returns:
        Similarity score (0-1)
    """
    from sklearn.metrics.pairwise import cosine_similarity
    
    embeddings = generate_embeddings([text1, text2])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return float(similarity)
