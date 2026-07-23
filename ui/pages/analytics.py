import streamlit as st
from src.analytics.dashboard import Dashboard

def show_analytics(df):
    st.markdown("# 📊 Analytics")
    
    if df is None:
        st.info("No data available")
        return
    
    dashboard = Dashboard(df)
    stats = dashboard.get_stats()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Items", stats['total_items'])
    with col2:
        st.metric("Content Types", len(stats['content_types']))
    with col3:
        st.metric("Sources", len(stats['sources']))
    
    # Charts
    fig1 = dashboard.create_content_distribution_chart()
    if fig1:
        st.plotly_chart(fig1, use_container_width=True)
    
    fig2 = dashboard.create_popularity_chart()
    if fig2:
        st.plotly_chart(fig2, use_container_width=True)