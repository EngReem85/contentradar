import streamlit as st

def show_search(df):
    st.markdown("# 🔍 Search Content")
    
    query = st.text_input("Search for content...", placeholder="e.g., action movies, leadership, anime...")
    
    if query and df is not None:
        st.markdown("### Results")
        
        # Search in title and description
        mask = df['title'].str.contains(query, case=False, na=False) | \
               df['description'].str.contains(query, case=False, na=False)
        results = df[mask]
        
        if len(results) > 0:
            cols = st.columns(3)
            for i, (_, row) in enumerate(results.head(9).iterrows()):
                with cols[i % 3]:
                    if row.get('image'):
                        st.image(row['image'], use_container_width=True)
                    st.caption(row.get('title', 'Untitled')[:50])
        else:
            st.warning("No results found")