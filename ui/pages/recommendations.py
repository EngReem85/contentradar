import streamlit as st

def show_recommendations(df, recommender):
    st.markdown("# ⭐ Recommendations")
    
    if df is None:
        st.info("Please load data first")
        return
    
    st.markdown("### 🔍 Find Recommendations")
    
    query = st.text_input("What are you interested in?", placeholder="e.g., movies about space, comedy series...")
    
    if query:
        with st.spinner("Generating recommendations..."):
            # Use recommender
            results = recommender.search(query, top_k=20)
            
            if results:
                cols = st.columns(3)
                for i, item in enumerate(results):
                    with cols[i % 3]:
                        if item.get('image'):
                            st.image(item['image'], use_container_width=True)
                        st.caption(item.get('title', 'Untitled')[:50])
                        st.progress(min(1.0, item.get('similarity', 0)))
            else:
                st.warning("No recommendations found")