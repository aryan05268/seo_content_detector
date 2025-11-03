"""Utility package initializer"""

from .parser import parse_html_content, scrape_url
from .features import (
    extract_basic_features,
    extract_all_features,
    extract_keywords,
    generate_embeddings,
    calculate_similarity
)
from .scorer import (
    predict_quality,
    is_thin_content,
    calculate_composite_score,
    get_quality_score_interpretation,
    get_score_color
)

__all__ = [
    'parse_html_content',
    'scrape_url',
    'extract_basic_features',
    'extract_all_features',
    'extract_keywords',
    'generate_embeddings',
    'calculate_similarity',
    'predict_quality',
    'is_thin_content',
    'calculate_composite_score',
    'get_quality_score_interpretation',
    'get_score_color'
]
