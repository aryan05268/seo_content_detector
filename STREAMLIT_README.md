# SEO Content Quality Analyzer - Streamlit Web App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_DEPLOYMENT_URL_HERE)

> **Live Demo**: [YOUR_DEPLOYMENT_URL_HERE]  
> _Update this link after deploying to Streamlit Cloud_

A production-ready web application for analyzing SEO content quality using machine learning. This tool helps SEO professionals and content creators evaluate content effectiveness, detect duplicates, and get actionable improvement recommendations.

![App Screenshot](https://via.placeholder.com/800x400?text=App+Screenshot+Here)

## 🎯 Features

### 🔍 Analysis Modes
1. **Single URL Analysis** - Analyze any webpage URL in real-time
2. **Batch Analysis** - Process multiple URLs via CSV upload or list input
3. **Text Input** - Directly paste content for analysis
4. **URL Comparison** - Side-by-side comparison with similarity detection

### 📊 Metrics & Insights
- **Quality Prediction**: ML-powered quality classification (Low/Medium/High)
- **Composite Score**: 0-100 quality score based on multiple factors
- **Readability Analysis**: Flesch Reading Ease scoring
- **Thin Content Detection**: Automatic flagging of short content (<500 words)
- **Duplicate Detection**: Semantic similarity calculation between content
- **Actionable Recommendations**: Specific improvement suggestions

### 🎨 Visualizations
- Interactive gauge charts for quality scores
- Feature comparison bar charts
- Batch analysis results tables
- Downloadable CSV reports

## 🚀 Quick Start

### Local Development

```bash
# Clone repository
git clone https://github.com/aryan05268/seo-content-detector.git
cd seo-content-detector

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app/app.py
```

The app will open at `http://localhost:8501`

## ☁️ Deploy to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at https://streamlit.io/cloud)

### Deployment Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Streamlit app ready for deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository: `aryan05268/seo-content-detector`
   - Main file path: `streamlit_app/app.py`
   - Click "Deploy"

3. **Update README with Deployed URL**
   - After deployment, copy your app URL (e.g., `https://username-reponame.streamlit.app`)
   - Update the badge and link at the top of this README

### Deployment Configuration

The app automatically:
- Downloads required NLTK data on first run
- Caches the ML model and transformer model for performance
- Handles missing dependencies gracefully

## 📂 Project Structure

```
seo-content-detector/
├── data/                                  # Data files
│   ├── data.csv                          # Input dataset (81 URLs)
│   ├── extracted_content.csv             # Parsed content
│   ├── features.csv                      # Engineered features
│   └── duplicates.csv                    # Duplicate pairs
├── notebooks/                            # Analysis notebooks
│   └── seo_pipeline.ipynb               # Main pipeline (5 cells)
├── streamlit_app/                        # Streamlit application
│   ├── app.py                           # Main Streamlit app
│   ├── utils/                           # Utility modules
│   │   ├── __init__.py                  # Package init
│   │   ├── parser.py                    # HTML parsing & scraping
│   │   ├── features.py                  # Feature extraction
│   │   └── scorer.py                    # Quality prediction
│   └── models/                          # ML models
│       └── quality_model.pkl            # Trained Random Forest (96% accuracy)
├── requirements.txt                      # Python dependencies
├── .gitignore                           # Git ignore rules
└── README.md                            # This file
```

## 🔧 Configuration

### Model Parameters

The ML model uses 4 key features:
- `word_count`: Total words in content
- `sentence_count`: Number of sentences
- `flesch_reading_ease`: Readability score (0-100)
- `avg_word_length`: Average characters per word

### Thresholds

```python
# Thin content threshold
THIN_CONTENT_THRESHOLD = 500  # words

# Duplicate similarity threshold
SIMILARITY_THRESHOLD = 0.80  # 80% cosine similarity

# Quality score ranges
# 0-50: Low quality
# 50-75: Medium quality
# 75-100: High quality
```

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| **Model Type** | Random Forest Classifier |
| **Accuracy** | 96% |
| **Training Samples** | 56 |
| **Test Samples** | 25 |
| **Features** | 4 core metrics |
| **Classes** | Low, Medium, High |

### Feature Importance
1. **sentence_count**: 43.6%
2. **flesch_reading_ease**: 35.4%
3. **word_count**: 21.0%

## 💻 Usage Examples

### Single URL Analysis
```python
# Visit the app
# Select "Single URL" mode
# Enter: https://example.com/article
# Click "Analyze"
```

### Batch Processing
```python
# Prepare CSV with columns: url, html_content (optional)
# Upload via "Batch Analysis" → "Upload CSV"
# Click "Analyze All"
# Download results
```

### Text Analysis
```python
# Select "Text Input" mode
# Paste your content
# Click "Analyze Text"
# View quality score and recommendations
```

### URL Comparison
```python
# Select "Compare URLs" mode
# Enter two URLs
# Click "Compare"
# View similarity score and side-by-side metrics
```

## 🛠️ Technical Details

### Dependencies
- **streamlit 1.32.0**: Web app framework
- **pandas 2.3.1**: Data manipulation
- **scikit-learn 1.4.2**: Machine learning
- **sentence-transformers 5.1.2**: Semantic embeddings (384-dim)
- **beautifulsoup4 4.12.3**: HTML parsing
- **plotly 5.22.0**: Interactive visualizations
- **nltk 3.8.1**: Text processing
- **textstat 0.7.4**: Readability scoring

### Architecture
- **Parser Module** (`utils/parser.py`): Web scraping and HTML cleaning
- **Features Module** (`utils/features.py`): NLP feature extraction and embeddings
- **Scorer Module** (`utils/scorer.py`): ML prediction and quality assessment
- **Main App** (`app.py`): Streamlit UI and orchestration

### Performance Optimizations
- `@st.cache_resource`: Caches ML model and transformer model
- `@st.cache_data`: Caches expensive computations
- Lazy loading of NLTK data
- Efficient batch processing with progress tracking

## 🚨 Troubleshooting

### Common Issues

**1. App crashes on startup**
```bash
# Check Python version (requires 3.8+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**2. Model file not found**
```bash
# Ensure model exists
ls streamlit_app/models/quality_model.pkl

# Copy from notebooks if needed
cp models/quality_model.pkl streamlit_app/models/
```

**3. NLTK data errors**
```python
# The app auto-downloads, but you can manually run:
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
```

**4. URL scraping fails (403 errors)**
- Some websites block automated requests
- Use "Text Input" mode as alternative
- The app includes user-agent headers to reduce blocking

**5. Slow embedding generation**
- First run downloads ~90MB transformer model
- Model is cached for subsequent runs
- Consider reducing batch size for large datasets

## 📈 Future Enhancements

- [ ] Multi-language support
- [ ] Custom quality criteria configuration
- [ ] Historical trend tracking
- [ ] API endpoint for programmatic access
- [ ] Integration with popular SEO tools
- [ ] Competitor content comparison
- [ ] Keyword density analysis
- [ ] Mobile responsiveness scoring

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- **Dataset**: Cybersecurity blog URLs (81 pages)
- **Transformer Model**: [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- **Readability Library**: [textstat](https://github.com/shivam5992/textstat)
- **Framework**: [Streamlit](https://streamlit.io)

## 📧 Contact

**Developer**: Aryan  
**GitHub**: [@aryan05268](https://github.com/aryan05268)  
**Repository**: [seo-content-detector](https://github.com/aryan05268/seo_content_detector)

For questions or support, please open an issue on GitHub.

---

**⭐ If you find this tool useful, please star the repository!**
