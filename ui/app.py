import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.config import Config
from src.analytics.dashboard import Dashboard
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="ContentRadar",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(Config.PROCESSED_DIR / "content.csv")
        logger.info(f"Loaded {len(df)} items")
        return df
    except Exception as e:
        logger.warning(f"Data not loaded: {e}")
        return None

# Main app
def create_app():
    df = load_data()
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50?text=ContentRadar", use_container_width=True)
        st.markdown("---")
        
        # Navigation
        pages = {
            "🏠 Home": "home",
            "🔍 Search": "search",
            "⭐ Recommendations": "recommendations",
            "📊 Analytics": "analytics",
            "👤 Profile": "profile",
            "🎯 Skills": "skills"
        }
        
        for label, page_id in pages.items():
            if st.button(label, use_container_width=True):
                st.session_state['page'] = page_id
                st.rerun()
        
        st.markdown("---")
        
        # Stats
        if df is not None:
            st.markdown("### 📊 Stats")
            st.metric("Total Content", len(df))
            if 'popularity' in df.columns:
                st.metric("Avg Popularity", f"{df['popularity'].mean():.1f}")
    
    # Main content
    st.markdown('<div class="main-header"><h1>📡 ContentRadar</h1><p>Smart Content Recommendation System</p></div>', unsafe_allow_html=True)
    
    # Page routing
    page = st.session_state.get('page', 'home')
    
    if page == "home":
        show_home(df)
    elif page == "search":
        show_search(df)
    elif page == "recommendations":
        show_recommendations(df)
    elif page == "analytics":
        show_analytics(df)
    elif page == "profile":
        show_profile()
    elif page == "skills":
        show_skills(df)

def show_home(df):
    if df is not None:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="stat-card"><h3>📚 Total</h3><h2>{}</h2></div>'.format(len(df)), unsafe_allow_html=True)
        
        with col2:
            types = df['content_type'].value_counts()
            st.markdown('<div class="stat-card"><h3>📺 Types</h3><h2>{}</h2></div>'.format(len(types)), unsafe_allow_html=True)
        
        with col3:
            if 'popularity' in df.columns:
                avg_pop = df['popularity'].mean()
                st.markdown('<div class="stat-card"><h3>⭐ Popularity</h3><h2>{:.1f}</h2></div>'.format(avg_pop), unsafe_allow_html=True)
        
        with col4:
            sources = df['source'].value_counts()
            st.markdown('<div class="stat-card"><h3>📡 Sources</h3><h2>{}</h2></div>'.format(len(sources)), unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🎬 Recent Content")
        
        # Show sample content
        sample = df.head(12)
        cols = st.columns(4)
        
        for i, (_, row) in enumerate(sample.iterrows()):
            with cols[i % 4]:
                if row.get('image'):
                    st.image(row['image'], use_container_width=True)
                st.caption(row.get('title', 'Untitled')[:50])
    else:
        st.info("📊 No data loaded. Please run data collection first.")

def show_search(df):
    st.markdown("### 🔍 Search Content")
    query = st.text_input("Search for content...", placeholder="e.g., action movies, leadership, anime...")
    
    if query:
        st.markdown("### Results")
        # Simple search
        mask = df['title'].str.contains(query, case=False, na=False) | \
               df['description'].str.contains(query, case=False, na=False)
        results = df[mask]
        
        if len(results) > 0:
            cols = st.columns(3)
            for i, (_, row) in enumerate(results.head(9).iterrows()):
                with cols[i % 3]:
                    if row.get('image'):
                        st.image(row['image'], use_container_width=True)
                    st.caption(row.get('title', 'Untitled'))
        else:
            st.warning("No results found")

def show_recommendations(df):
    st.markdown("### ⭐ Recommendations")
    st.info("🔧 Recommendation system is under development. Please check back later.")

def show_analytics(df):
    st.markdown("### 📊 Analytics Dashboard")
    
    if df is not None and len(df) > 0:
        dashboard = Dashboard(df)
        stats = dashboard.get_stats()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Items", stats.get('total_items', 0))
        with col2:
            st.metric("Content Types", len(stats.get('content_types', {})))
        with col3:
            st.metric("Sources", len(stats.get('sources', {})))
        
        # Charts
        fig1 = dashboard.create_content_distribution_chart()
        if fig1:
            st.plotly_chart(fig1, use_container_width=True)
        
        fig2 = dashboard.create_popularity_chart(10)
        if fig2:
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No data available for analytics")

def show_profile():
    st.markdown("### 👤 Profile")
    st.info("🔧 Profile features are under development.")

def show_skills(df):
    st.markdown("### 🎯 Skills Learning")
    st.markdown("""
    ⚠️ **Premium Feature**
    
    Skills Learning is a premium feature of ContentRadar.
    
    For commercial licensing:
    - 📧 licensing@contentradar.com
    - 🌐 Visit our website for pricing
    
    **Features:**
    - Skill extraction from content
    - Personalized learning paths
    - Progress tracking
    - Skill analysis
    """)

if __name__ == "__main__":
    create_app()