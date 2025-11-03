"""
SEO Content Quality Analyzer - Streamlit App
A production-ready web application for analyzing SEO content quality
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils import (
    scrape_url,
    parse_html_content,
    extract_basic_features,
    extract_all_features,
    predict_quality,
    is_thin_content,
    calculate_composite_score,
    get_quality_score_interpretation,
    get_score_color,
    calculate_similarity
)

# Page configuration
st.set_page_config(
    page_title="SEO Content Quality Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .quality-badge {
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        font-weight: bold;
        display: inline-block;
    }
    .quality-high {
        background-color: #d4edda;
        color: #155724;
    }
    .quality-medium {
        background-color: #fff3cd;
        color: #856404;
    }
    .quality-low {
        background-color: #f8d7da;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🔍 SEO Content Quality Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Analyze content quality, detect duplicates, and get actionable insights</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/seo.png", width=80)
        st.title("Analysis Options")
        
        analysis_mode = st.radio(
            "Choose Analysis Mode:",
            ["Single URL", "Batch Analysis", "Text Input", "Compare URLs"]
        )
        
        st.markdown("---")
        st.markdown("### About")
        st.info("""
        This tool uses machine learning to analyze SEO content quality based on:
        - **Word count** & length
        - **Readability** scores
        - **Semantic embeddings**
        - **Content structure**
        """)
        
        st.markdown("---")
        st.markdown("**Model**: Random Forest Classifier")
        st.markdown("**Accuracy**: 96%")
        st.markdown("**Features**: 4 core metrics")
    
    # Main content based on mode
    if analysis_mode == "Single URL":
        single_url_analysis()
    elif analysis_mode == "Batch Analysis":
        batch_analysis()
    elif analysis_mode == "Text Input":
        text_input_analysis()
    elif analysis_mode == "Compare URLs":
        compare_urls()


def single_url_analysis():
    """Analyze a single URL"""
    st.header("📄 Single URL Analysis")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        url = st.text_input(
            "Enter URL to analyze:",
            placeholder="https://example.com/article",
            help="Enter a complete URL including http:// or https://"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)
    
    if analyze_button and url:
        with st.spinner("Scraping and analyzing content..."):
            # Scrape URL
            result = scrape_url(url)
            
            if result['status'] == 'error':
                st.error(f"❌ Error: {result['error']}")
                st.info("💡 **Tip**: Some websites block automated requests. Try the 'Text Input' mode instead.")
                return
            
            # Extract features
            features = extract_basic_features(result['body_text'])
            
            # Predict quality
            quality = predict_quality(features)
            interpretation = get_quality_score_interpretation(quality, features)
            
            # Composite score
            composite_score = calculate_composite_score(features)
            
            # Display results
            display_analysis_results(result, features, quality, interpretation, composite_score)


def text_input_analysis():
    """Analyze directly entered text"""
    st.header("📝 Text Input Analysis")
    
    st.markdown("Paste your content below for analysis:")
    
    text = st.text_area(
        "Content Text:",
        height=300,
        placeholder="Paste your article or webpage content here...",
        help="Enter the main body text of your content"
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        analyze_button = st.button("🔍 Analyze Text", type="primary", use_container_width=True)
    
    if analyze_button and text:
        with st.spinner("Analyzing content..."):
            # Extract features
            features = extract_basic_features(text)
            
            # Predict quality
            quality = predict_quality(features)
            interpretation = get_quality_score_interpretation(quality, features)
            
            # Composite score
            composite_score = calculate_composite_score(features)
            
            # Display results
            result = {
                'url': 'Text Input',
                'title': 'Direct Text Analysis',
                'body_text': text,
                'word_count': features['word_count']
            }
            
            display_analysis_results(result, features, quality, interpretation, composite_score)


def batch_analysis():
    """Batch analyze multiple URLs or CSV upload"""
    st.header("📊 Batch Analysis")
    
    tab1, tab2 = st.tabs(["Upload CSV", "Enter Multiple URLs"])
    
    with tab1:
        st.markdown("Upload a CSV file with 'url' and optionally 'html_content' columns")
        
        uploaded_file = st.file_uploader(
            "Choose CSV file",
            type=['csv'],
            help="CSV should have 'url' column, optionally 'html_content' column"
        )
        
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            
            st.success(f"✅ Loaded {len(df)} rows")
            st.dataframe(df.head(), use_container_width=True)
            
            if st.button("🚀 Analyze All", type="primary"):
                process_batch_analysis(df)
    
    with tab2:
        st.markdown("Enter multiple URLs (one per line)")
        
        urls_text = st.text_area(
            "URLs:",
            height=200,
            placeholder="https://example.com/article1\nhttps://example.com/article2\nhttps://example.com/article3"
        )
        
        if st.button("🚀 Analyze URLs", type="primary"):
            urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
            if urls:
                df = pd.DataFrame({'url': urls})
                process_batch_analysis(df)


def compare_urls():
    """Compare two URLs side by side"""
    st.header("⚖️ Compare Two URLs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("URL 1")
        url1 = st.text_input("First URL:", key="url1", placeholder="https://example.com/page1")
    
    with col2:
        st.subheader("URL 2")
        url2 = st.text_input("Second URL:", key="url2", placeholder="https://example.com/page2")
    
    if st.button("🔄 Compare", type="primary"):
        if url1 and url2:
            with st.spinner("Analyzing both URLs..."):
                result1 = scrape_url(url1)
                result2 = scrape_url(url2)
                
                if result1['status'] == 'error' or result2['status'] == 'error':
                    st.error("❌ Error scraping one or both URLs")
                    return
                
                # Extract features
                features1 = extract_basic_features(result1['body_text'])
                features2 = extract_basic_features(result2['body_text'])
                
                # Predict quality
                quality1 = predict_quality(features1)
                quality2 = predict_quality(features2)
                
                # Calculate similarity
                similarity = calculate_similarity(result1['body_text'], result2['body_text'])
                
                # Display comparison
                display_comparison(result1, result2, features1, features2, quality1, quality2, similarity)


def display_analysis_results(result, features, quality, interpretation, composite_score):
    """Display analysis results"""
    
    # Quality Badge
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        quality_class = f"quality-{quality.lower()}"
        st.markdown(
            f'<div class="quality-badge {quality_class}">{interpretation["emoji"]} {quality} Quality</div>',
            unsafe_allow_html=True
        )
        st.markdown(f"**{interpretation['message']}**")
        st.caption(interpretation['description'])
    
    with col2:
        st.metric("Composite Score", f"{composite_score:.1f}/100")
    
    with col3:
        thin = "Yes ❌" if is_thin_content(features['word_count']) else "No ✅"
        st.metric("Thin Content", thin)
    
    # Score Gauge
    st.markdown("---")
    fig = create_score_gauge(composite_score)
    st.plotly_chart(fig, use_container_width=True)
    
    # Feature Metrics
    st.markdown("---")
    st.subheader("📊 Content Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Word Count", f"{features['word_count']:,}")
    with col2:
        st.metric("Sentences", features['sentence_count'])
    with col3:
        st.metric("Readability Score", f"{features['flesch_reading_ease']:.1f}")
    with col4:
        st.metric("Avg Word Length", f"{features['avg_word_length']:.2f}")
    
    # Recommendations
    if interpretation['recommendations']:
        st.markdown("---")
        st.subheader("💡 Recommendations")
        for rec in interpretation['recommendations']:
            st.markdown(f"- {rec}")
    
    # Content Preview
    with st.expander("📄 View Content Preview"):
        st.markdown(f"**Title:** {result.get('title', 'N/A')}")
        st.markdown(f"**URL:** {result.get('url', 'N/A')}")
        st.text_area("Content:", result['body_text'][:1000] + "...", height=200)


def display_comparison(result1, result2, features1, features2, quality1, quality2, similarity):
    """Display side-by-side comparison"""
    
    st.markdown("---")
    
    # Similarity Score
    st.subheader("📊 Content Similarity")
    similarity_pct = similarity * 100
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.metric("Similarity Score", f"{similarity_pct:.1f}%")
        
        if similarity_pct > 80:
            st.error("⚠️ High similarity detected! Possible duplicate content.")
        elif similarity_pct > 50:
            st.warning("🔸 Moderate similarity. Consider differentiating content.")
        else:
            st.success("✅ Content is sufficiently unique.")
    
    st.markdown("---")
    
    # Side-by-side comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("URL 1")
        st.markdown(f"**Quality:** {quality1}")
        st.markdown(f"**Word Count:** {features1['word_count']}")
        st.markdown(f"**Readability:** {features1['flesch_reading_ease']:.1f}")
        st.markdown(f"**Sentences:** {features1['sentence_count']}")
    
    with col2:
        st.subheader("URL 2")
        st.markdown(f"**Quality:** {quality2}")
        st.markdown(f"**Word Count:** {features2['word_count']}")
        st.markdown(f"**Readability:** {features2['flesch_reading_ease']:.1f}")
        st.markdown(f"**Sentences:** {features2['sentence_count']}")
    
    # Comparison Chart
    st.markdown("---")
    st.subheader("📈 Feature Comparison")
    
    comparison_df = pd.DataFrame({
        'Metric': ['Word Count', 'Sentences', 'Readability', 'Avg Word Length'],
        'URL 1': [
            features1['word_count'],
            features1['sentence_count'],
            features1['flesch_reading_ease'],
            features1['avg_word_length']
        ],
        'URL 2': [
            features2['word_count'],
            features2['sentence_count'],
            features2['flesch_reading_ease'],
            features2['avg_word_length']
        ]
    })
    
    fig = px.bar(
        comparison_df,
        x='Metric',
        y=['URL 1', 'URL 2'],
        barmode='group',
        title="Feature Comparison"
    )
    st.plotly_chart(fig, use_container_width=True)


def process_batch_analysis(df):
    """Process batch analysis"""
    
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, row in df.iterrows():
        status_text.text(f"Processing {idx + 1}/{len(df)}...")
        
        # Get content
        if 'html_content' in df.columns and pd.notna(row.get('html_content')):
            title, body_text, word_count = parse_html_content(row['html_content'])
            url = row['url']
        else:
            scraped = scrape_url(row['url'])
            if scraped['status'] == 'error':
                continue
            url = scraped['url']
            body_text = scraped['body_text']
        
        # Extract features
        features = extract_basic_features(body_text)
        quality = predict_quality(features)
        composite_score = calculate_composite_score(features)
        
        results.append({
            'URL': url,
            'Quality': quality,
            'Score': composite_score,
            'Word Count': features['word_count'],
            'Readability': features['flesch_reading_ease'],
            'Thin Content': is_thin_content(features['word_count'])
        })
        
        progress_bar.progress((idx + 1) / len(df))
    
    status_text.text("Analysis complete!")
    
    # Display results
    if results:
        results_df = pd.DataFrame(results)
        
        st.success(f"✅ Analyzed {len(results)} pages")
        
        # Summary stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Avg Score", f"{results_df['Score'].mean():.1f}")
        with col2:
            high_quality = (results_df['Quality'] == 'High').sum()
            st.metric("High Quality", high_quality)
        with col3:
            thin_count = results_df['Thin Content'].sum()
            st.metric("Thin Content", thin_count)
        with col4:
            avg_words = results_df['Word Count'].mean()
            st.metric("Avg Words", f"{avg_words:.0f}")
        
        # Results table
        st.dataframe(results_df, use_container_width=True)
        
        # Download button
        csv = results_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Results CSV",
            data=csv,
            file_name="seo_analysis_results.csv",
            mime="text/csv"
        )


def create_score_gauge(score):
    """Create a gauge chart for score"""
    
    color = get_score_color(score)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Quality Score"},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 75], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 75
            }
        }
    ))
    
    fig.update_layout(height=300)
    
    return fig


if __name__ == "__main__":
    main()
