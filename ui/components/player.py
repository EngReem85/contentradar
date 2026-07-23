import streamlit as st

def video_player(url, title="Video Player"):
    """Embed video player"""
    
    st.markdown(f"""
    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; background: #000; border-radius: 10px;">
        <iframe 
            src="{url}" 
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
        ></iframe>
    </div>
    """, unsafe_allow_html=True)

def audio_player(url, title="Audio Player"):
    """Embed audio player"""
    
    st.audio(url, format='audio/mpeg')

def content_player(content_type, url, title="Player"):
    """Generic content player"""
    
    if content_type in ['youtube', 'video']:
        video_player(url, title)
    elif content_type == 'audio':
        audio_player(url, title)
    else:
        st.info(f"ℹ️ Player not available for {content_type} content")