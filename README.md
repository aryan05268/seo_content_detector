# SEO Content Quality Analyzer

A comprehensive machine learning pipeline for analyzing SEO content quality, detecting duplicates, and identifying thin content. This project extracts features from HTML content, generates embeddings using transformer models, and trains a Random Forest classifier to predict content quality.

## 🎯 Features

- **HTML Parsing**: Extract clean text, titles, and body content from raw HTML
- **Feature Engineering**: Calculate readability scores, word/sentence counts, TF-IDF keywords, and semantic embeddings
- **Duplicate Detection**: Identify similar content using cosine similarity on 384-dimensional embeddings
- **Thin Content Flagging**: Automatically flag pages with <500 words
- **Quality Classification**: ML model (Random Forest) to predict content quality (Low/Medium/High)
- **URL Analysis API**: Analyze any URL in real-time with the trained model

## 📊 Project Structure

```
seo-content-detector/
├── data/
│   ├── data.csv                      # Input: URLs + HTML content (81 pages)
│   ├── extracted_content.csv         # Step 1: Parsed titles and body text
│   ├── features.csv                  # Step 2: Engineered features + embeddings
│   └── duplicates.csv                # Step 3: Duplicate pairs (77 found)
├── notebooks/
│   └── seo_pipeline.ipynb            # Main pipeline (5 cells)
├── models/
│   └── quality_model.pkl             # Trained Random Forest model (96% accuracy)
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore rules
└── README.md                         # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- 2GB+ RAM (for transformer model)

### Installation

```powershell
# Clone the repository
git clone https://github.com/yourusername/seo-content-detector.git
cd seo-content-detector

# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate virtual environment (Linux/Mac)
# source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Running the Notebook

```powershell
# Launch Jupyter
jupyter notebook notebooks/seo_pipeline.ipynb

# Or use Jupyter Lab
jupyter lab notebooks/seo_pipeline.ipynb
```

## 📝 Pipeline Overview

The notebook contains 5 main cells that execute sequentially:

### Cell 1: HTML Parsing
- **Input**: `data/data.csv` (81 URLs with HTML content)
- **Output**: `data/extracted_content.csv`
- **Processing**: Extracts titles, body text, and word counts from HTML
- **Duration**: ~10 seconds

### Cell 2: Feature Engineering
- **Input**: `data/extracted_content.csv`
- **Output**: `data/features.csv`
- **Processing**:
  - Text cleaning and normalization
  - Readability scoring (Flesch Reading Ease)
  - TF-IDF keyword extraction (top 5 per document)
  - Sentence embeddings (all-MiniLM-L6-v2, 384 dimensions)
- **Duration**: ~47 seconds (includes model download first time)

### Cell 3: Duplicate Detection
- **Input**: `data/features.csv`
- **Output**: `data/duplicates.csv`, `data/data_features_with_thin_content.csv`
- **Processing**:
  - Cosine similarity calculation on embeddings
  - Identifies pairs with >80% similarity
  - Flags thin content (<500 words)
- **Results**:
  - 77 duplicate pairs found
  - 24 thin content pages (29.6%)
- **Duration**: <1 second

### Cell 4: Quality Classification (Simple Labels)
- **Input**: `data/features.csv`
- **Output**: `models/quality_model.pkl`
- **Processing**:
  - Creates quality labels using rule-based heuristics
  - Trains Random Forest classifier (100 estimators)
  - Generates confusion matrix and feature importance
- **Results**:
  - Baseline accuracy: 48%
  - RF accuracy: 100% (may indicate overfitting on small dataset)
- **Duration**: ~4 seconds

### Cell 5: Quality Classification (Composite Score)
- **Input**: `data/features.csv`
- **Output**: Updated `models/quality_model.pkl`
- **Processing**:
  - Improved labeling using composite scoring
  - Balanced classes (27 Low, 27 Medium, 27 High)
  - Trains optimized Random Forest
- **Results**:
  - Baseline accuracy: 76%
  - RF accuracy: 96%
  - Top features: sentence_count (44%), flesch_reading_ease (35%)
- **Duration**: <1 second

### Cell 6: Real-time URL Analysis
- **Input**: Any URL (via `analyze_url()` function)
- **Output**: JSON with quality prediction and similar pages
- **Processing**:
  - Scrapes URL content
  - Extracts features
  - Predicts quality using trained model
  - Finds 3 most similar pages from dataset
- **Note**: May fail on sites with bot protection (403 errors)

## 📈 Results Summary

| Metric | Value |
|--------|-------|
| **Total Pages Analyzed** | 81 |
| **Duplicate Pairs Found** | 77 |
| **Thin Content Pages** | 24 (29.6%) |
| **Model Accuracy** | 96% |
| **Baseline Accuracy** | 76% |
| **Most Important Feature** | sentence_count (43.6%) |
| **Second Important** | flesch_reading_ease (35.4%) |

## 🔧 Configuration

### Key Parameters (can be adjusted in notebook)

```python
# Cell 3: Duplicate Detection
SIMILARITY_THRESHOLD = 0.80      # Cosine similarity threshold
THIN_CONTENT_THRESHOLD = 500     # Word count threshold

# Cell 4/5: Model Training
n_estimators = 100               # Random Forest trees
test_size = 0.3                  # Train/test split ratio
random_state = 42                # Reproducibility seed
```

## 📦 Dependencies

Core libraries used:
- **pandas 2.3.1**: Data manipulation
- **scikit-learn 1.4.2**: Machine learning
- **sentence-transformers 5.1.2**: Semantic embeddings
- **beautifulsoup4 4.12.3**: HTML parsing
- **nltk 3.8.1**: Text processing
- **matplotlib 3.10.0 / seaborn 0.13.2**: Visualization

See `requirements.txt` for complete list.

## 🤝 Usage Examples

### Analyzing a New URL

```python
# Run cells 1-5 first to train the model

# Then in Cell 6:
result = analyze_url("https://example.com/article")
print(json.dumps(result, indent=2))
```

Output:
```json
{
  "url": "https://example.com/article",
  "word_count": 1250,
  "sentence_count": 45,
  "avg_word_length": 5.2,
  "readability": 62.3,
  "quality_label": "High",
  "is_thin": false,
  "similar_to": [
    {"url": "https://...", "similarity": 0.87},
    {"url": "https://...", "similarity": 0.82}
  ]
}
```

## 📊 Model Performance

### Confusion Matrix (Cell 5)
```
           Predicted
Actual    Low  Med  High
Low        8    0    0
Medium     0    9    0
High       0    1    7
```

### Feature Importance
1. sentence_count: 43.6%
2. flesch_reading_ease: 35.4%
3. word_count: 21.0%

## 🛠️ Troubleshooting

### Common Issues

**1. HTTP 403 errors when analyzing URLs**
- Add user-agent headers to requests
- Some sites block automated scrapers

**2. NLTK punkt tokenizer not found**
- The notebook auto-downloads on first run
- Manual: `python -m nltk.downloader punkt punkt_tab`

**3. Out of memory during embedding generation**
- Reduce batch size in SentenceTransformer
- Process data in chunks

**4. Model file not found**
- Run Cell 4 or 5 first to train and save model
- Check `models/` directory exists

## 📄 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- Dataset: Cybersecurity blog URLs
- Transformer model: [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- Readability scoring: [textstat library](https://github.com/shivam5992/textstat)

## 📧 Contact

For questions or collaboration, please open an issue on GitHub.
