"""
HTML Content Parsing Module
Extracts clean text, titles, and body content from HTML
"""

from bs4 import BeautifulSoup
import re
import requests
from typing import Tuple, Dict


def parse_html_content(html: str) -> Tuple[str, str, int]:
    """
    Parses raw HTML to extract title and clean main body text.
    
    Prioritizes <main> and <article> tags, then falls back to <body>.
    
    Args:
        html: Raw HTML string
        
    Returns:
        Tuple of (title, body_text, word_count)
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # 1. Extract Title
        title = soup.title.string.strip() if soup.title else ''
        
        # 2. Extract Main Content
        main_content = soup.find('main')
        if not main_content:
            main_content = soup.find('article')
        if not main_content:
            main_content = soup.find('body')
        
        if main_content:
            # Remove script and style tags
            for tag in main_content(['script', 'style']):
                tag.decompose()
            
            # Get clean text
            body_text = main_content.get_text(separator=' ', strip=True)
            body_text = re.sub(r'\s+', ' ', body_text)
        else:
            body_text = ''
            
        # 3. Calculate Word Count
        word_count = len(body_text.split())
        
        return title, body_text, word_count
    
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return '', '', 0


def scrape_url(url: str, timeout: int = 10) -> Dict[str, any]:
    """
    Scrapes a URL and extracts content.
    
    Args:
        url: URL to scrape
        timeout: Request timeout in seconds
        
    Returns:
        Dictionary with url, title, body_text, word_count, or error
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, timeout=timeout, headers=headers)
        response.raise_for_status()
        
        title, body_text, word_count = parse_html_content(response.text)
        
        return {
            'url': url,
            'title': title,
            'body_text': body_text,
            'word_count': word_count,
            'status': 'success'
        }
    except requests.exceptions.RequestException as e:
        return {
            'url': url,
            'error': str(e),
            'status': 'error'
        }
    except Exception as e:
        return {
            'url': url,
            'error': f"Parsing error: {str(e)}",
            'status': 'error'
        }
