import streamlit as st

def content_card(item, width="100%"):
    """Display a content card"""
    st.markdown(f"""
    <div style="border: 1px solid #ddd; border-radius: 10px; padding: 10px; margin: 5px; width: {width};">
        <img src="{item.get('image', '')}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 5px;">
        <h4 style="margin: 10px 0; font-size: 16px;">{item.get('title', 'Untitled')}</h4>
        <p style="font-size: 12px; color: #666;">{item.get('content_type', '')} | {item.get('source', '')}</p>
        <p style="font-size: 12px; margin: 5px 0;">⭐ {item.get('popularity', 0):.1f}</p>
    </div>
    """, unsafe_allow_html=True)