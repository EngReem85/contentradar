import streamlit as st
from datetime import datetime

def show_profile(user_manager):
    st.markdown("# 👤 My Profile")
    
    # User info
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://ui-avatars.com/api/?name=User&size=150", use_container_width=True)
    
    with col2:
        st.markdown(f"""
        ## User: {user_manager.user_id}
        
        **Member since:** {datetime.now().strftime("%B %Y")}
        
        **Total Ratings:** {len(user_manager.get_ratings())}
        
        **Watchlist:** {len(user_manager.get_watchlist())}
        """)
    
    st.divider()
    
    # Statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ratings = user_manager.get_ratings()
        if ratings:
            avg_rating = sum(r['rating'] for r in ratings.values()) / len(ratings)
            st.metric("⭐ Average Rating", f"{avg_rating:.1f}")
        else:
            st.metric("⭐ Average Rating", "N/A")
    
    with col2:
        watchlist = user_manager.get_watchlist()
        completed = sum(1 for w in watchlist.values() if w.get('status') == 'completed')
        st.metric("✅ Completed", completed)
    
    with col3:
        progress = user_manager.get_progress()
        if progress:
            avg_progress = sum(p.get('progress', 0) for p in progress.values()) / len(progress)
            st.metric("📊 Avg Progress", f"{avg_progress:.0f}%")
        else:
            st.metric("📊 Avg Progress", "N/A")
    
    st.divider()
    
    # Preferences
    st.markdown("### ⚙️ Preferences")
    preferences = user_manager.get_preferences()
    
    # Content types preference
    content_types = st.multiselect(
        "Preferred Content Types",
        ["movie", "series", "anime", "youtube", "podcast"],
        default=preferences.get('content_types', [])
    )
    
    # Genres preference
    genres = st.multiselect(
        "Preferred Genres",
        ["action", "comedy", "drama", "sci-fi", "fantasy", "romance", "thriller"],
        default=preferences.get('genres', [])
    )
    
    if st.button("💾 Save Preferences"):
        preferences['content_types'] = content_types
        preferences['genres'] = genres
        user_manager._save_json(user_manager.preferences_file, preferences)
        st.success("Preferences saved successfully!")