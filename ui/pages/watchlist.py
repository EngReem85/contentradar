import streamlit as st
from datetime import datetime

def show_watchlist(user_manager):
    st.markdown("# 📺 My Watchlist")
    
    # Get watchlist data
    watchlist = user_manager.get_watchlist()
    
    if not watchlist:
        st.info("📭 Your watchlist is empty. Start adding content you want to watch!")
        return
    
    # Filter options
    status_filter = st.selectbox(
        "Filter by status",
        ["All", "plan_to_watch", "watching", "completed", "on_hold"],
        format_func=lambda x: {
            "All": "All",
            "plan_to_watch": "📋 Plan to Watch",
            "watching": "▶️ Watching",
            "completed": "✅ Completed",
            "on_hold": "⏸️ On Hold"
        }.get(x, x)
    )
    
    # Display watchlist
    st.markdown("### Your Watchlist")
    
    for item_id, data in watchlist.items():
        if status_filter != "All" and data.get('status') != status_filter:
            continue
        
        # Get content details (you would fetch from your content DB)
        # For now, just display the ID and status
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            st.write(f"**{item_id}**")
            if data.get('notes'):
                st.caption(f"📝 {data['notes']}")
        
        with col2:
            status_emoji = {
                "plan_to_watch": "📋",
                "watching": "▶️",
                "completed": "✅",
                "on_hold": "⏸️"
            }.get(data.get('status', ''), "❓")
            st.write(f"{status_emoji} {data.get('status', 'Unknown')}")
        
        with col3:
            # Status update buttons
            status_options = ["plan_to_watch", "watching", "completed", "on_hold"]
            new_status = st.selectbox(
                "Update",
                status_options,
                index=status_options.index(data.get('status', 'plan_to_watch')),
                key=f"status_{item_id}",
                label_visibility="collapsed"
            )
            if new_status != data.get('status'):
                user_manager.update_status(item_id, new_status)
                st.rerun()
            
            if st.button("🗑️ Remove", key=f"remove_{item_id}"):
                user_manager.remove_from_watchlist(item_id)
                st.rerun()
        
        st.divider()