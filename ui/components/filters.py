import streamlit as st

def filter_sidebar(df):
    """Create filter sidebar"""
    with st.sidebar:
        st.markdown("### 🔍 Filters")
        
        # Content type filter
        content_types = st.multiselect(
            "Content Type",
            options=sorted(df['content_type'].unique()) if df is not None else [],
            default=[]
        )
        
        # Source filter
        sources = st.multiselect(
            "Source",
            options=sorted(df['source'].unique()) if df is not None else [],
            default=[]
        )
        
        # Popularity range
        if df is not None and 'popularity' in df.columns:
            min_pop, max_pop = float(df['popularity'].min()), float(df['popularity'].max())
            pop_range = st.slider(
                "Popularity Range",
                min_value=min_pop,
                max_value=max_pop,
                value=(min_pop, max_pop)
            )
        else:
            pop_range = (0, 100)
        
        return {
            'content_types': content_types,
            'sources': sources,
            'popularity_range': pop_range
        }