import streamlit as st

def show_home(df):
    st.markdown("# 🏠 Home")
    st.markdown("Welcome to ContentRadar!")
    
    if df is not None:
        st.markdown("### 📊 Quick Stats")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Content", len(df))
        with col2:
            types = df['content_type'].value_counts()
            st.metric("Content Types", len(types))
        with col3:
            if 'popularity' in df.columns:
                st.metric("Avg Popularity", f"{df['popularity'].mean():.1f}")
        
        st.markdown("### 🔥 Popular Content")
        if 'popularity' in df.columns:
            popular = df.nlargest(10, 'popularity')
            for _, row in popular.iterrows():
                st.write(f"- {row.get('title', 'Untitled')}")
    else:
        st.info("No data loaded. Please run collection first.")