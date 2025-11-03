"""
Content Quality Scoring Module
Loads model and predicts content quality
"""

import joblib
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import streamlit as st
from pathlib import Path


@st.cache_resource
def load_quality_model():
    """Load and cache the trained Random Forest model"""
    model_path = Path(__file__).parent.parent / 'models' / 'quality_model.pkl'
    try:
        model = joblib.load(model_path)
        return model
    except FileNotFoundError:
        st.error(f"Model file not found at {model_path}")
        return None


def predict_quality(features: Dict[str, any]) -> str:
    """
    Predict content quality using trained model.
    
    Args:
        features: Dictionary with required features:
            - word_count
            - sentence_count
            - flesch_reading_ease
            - avg_word_length
            
    Returns:
        Quality label: 'Low', 'Medium', or 'High'
    """
    model = load_quality_model()
    
    if model is None:
        return 'Unknown'
    
    # Prepare features in correct order
    feature_vector = pd.DataFrame([{
        'word_count': features.get('word_count', 0),
        'sentence_count': features.get('sentence_count', 0),
        'flesch_reading_ease': features.get('flesch_reading_ease', 0),
        'avg_word_length': features.get('avg_word_length', 0)
    }])
    
    try:
        prediction = model.predict(feature_vector)[0]
        return prediction
    except Exception as e:
        st.error(f"Prediction error: {e}")
        return 'Unknown'


def get_quality_score_interpretation(quality: str, features: Dict[str, any]) -> Dict[str, str]:
    """
    Get interpretation and recommendations for quality score.
    
    Args:
        quality: Quality label
        features: Feature dictionary
        
    Returns:
        Dictionary with interpretation and recommendations
    """
    word_count = features.get('word_count', 0)
    flesch = features.get('flesch_reading_ease', 0)
    
    interpretations = {
        'High': {
            'emoji': '🟢',
            'message': 'Excellent content quality!',
            'description': 'This content has strong indicators of high quality with good length and readability.',
            'recommendations': []
        },
        'Medium': {
            'emoji': '🟡',
            'message': 'Good content, but room for improvement',
            'description': 'This content meets basic quality standards but could be enhanced.',
            'recommendations': []
        },
        'Low': {
            'emoji': '🔴',
            'message': 'Content needs significant improvement',
            'description': 'This content falls short of quality standards.',
            'recommendations': []
        },
        'Unknown': {
            'emoji': '⚪',
            'message': 'Unable to assess quality',
            'description': 'Quality assessment unavailable.',
            'recommendations': []
        }
    }
    
    result = interpretations.get(quality, interpretations['Unknown']).copy()
    
    # Add specific recommendations
    recommendations = []
    
    if word_count < 500:
        recommendations.append("📝 Increase content length (current: {0} words, recommended: 500+ words)".format(word_count))
    elif word_count < 1500:
        recommendations.append("📝 Consider expanding content (current: {0} words, optimal: 1500+ words)".format(word_count))
    
    if flesch < 30:
        recommendations.append("📖 Simplify language for better readability (Flesch score: {0:.1f}/100)".format(flesch))
    elif flesch < 50:
        recommendations.append("📖 Improve readability with simpler sentences (Flesch score: {0:.1f}/100)".format(flesch))
    
    if quality == 'Low':
        recommendations.append("✨ Review content structure and add more value")
        recommendations.append("🎯 Focus on user intent and comprehensive coverage")
    
    result['recommendations'] = recommendations
    
    return result


def is_thin_content(word_count: int, threshold: int = 500) -> bool:
    """
    Check if content is considered 'thin' (too short).
    
    Args:
        word_count: Number of words
        threshold: Minimum word count
        
    Returns:
        True if thin content
    """
    return word_count < threshold


def calculate_composite_score(features: Dict[str, any]) -> float:
    """
    Calculate a composite quality score (0-100).
    
    Args:
        features: Feature dictionary
        
    Returns:
        Score from 0 to 100
    """
    word_count = features.get('word_count', 0)
    sentence_count = features.get('sentence_count', 0)
    flesch = features.get('flesch_reading_ease', 0)
    avg_word_length = features.get('avg_word_length', 0)
    
    # Normalize components
    word_score = min(word_count / 2000, 1.0) * 30  # Max 30 points
    readability_score = min(max(flesch, 0) / 100, 1.0) * 40  # Max 40 points
    sentence_score = min(sentence_count / 50, 1.0) * 20  # Max 20 points
    word_length_score = min(avg_word_length / 6, 1.0) * 10  # Max 10 points
    
    total = word_score + readability_score + sentence_score + word_length_score
    
    return min(total, 100)


def get_score_color(score: float) -> str:
    """Get color for score visualization"""
    if score >= 75:
        return '#28a745'  # Green
    elif score >= 50:
        return '#ffc107'  # Yellow
    else:
        return '#dc3545'  # Red
