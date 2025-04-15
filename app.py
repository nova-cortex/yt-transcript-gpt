import streamlit as st
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    NoTranscriptFound,
    TranscriptsDisabled
)
import re

def extract_video_id(url: str) -> str:
    url = url.strip()
    if 'shorts' in url:
        url = url.split('?')[0]
    patterns = [
        r"(?:v=)([^&]+)",
        r"youtu\.be/([^?&]+)",
        r"youtube\.com/shorts/([^?&]+)"
    ]
    for pat in patterns:
        match = re.search(pat, url)
        if match:
            return match.group(1)
    return url

def get_channel_and_video_details(video_id: str):
    return {
        "channel_id": "UCdABA6CLwAZ5ef_Qoqbl60w",  # placeholder
        "video_id": video_id
    }

def get_transcript_data(video_id: str, languages=None):
    try:
        if languages is None:
            return YouTubeTranscriptApi.get_transcript(video_id)
        else:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            t = transcript_list.find_transcript(languages)
            return t.fetch()
    except (NoTranscriptFound, TranscriptsDisabled):
        return None
    except:
        return None

def format_timestamp(seconds: float) -> str:
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"

def main():
    st.set_page_config(
        page_title="YouTube Transcript Extractor",
        layout="centered",
        initial_sidebar_state="auto",
    )
    
    # Unified CSS styling - all backgrounds set to #121212 to remove color blocks
    st.markdown("""
    <style>
    /* General body styling */
    body {
        background-color: #121212;
        color: #e0e0e0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Main container - same color as body, no box shadow */
    .main .block-container {
        max-width: 1100px;
        margin: auto;
        background-color: #121212;
        padding: 2rem;
        border-radius: 0;
    }
    /* Title and subtitle styling */
    .title-text {
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.2rem;
        color: #ffffff;
    }
    .subtitle-text {
        font-size: 1.2rem;
        font-weight: 500;
        text-align: center;
        margin-bottom: 2rem;
        color: #bbbbbb;
    }
    /* Button styling */
    .stButton > button {
        display: block;
        width: 100%;
        background-color: #007acc !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 1.2rem 1rem !important;
        font-size: 1.1rem !important;
        font-weight: 600;
        transition: background-color 0.3s ease;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #005fa3 !important;
    }
    /* Panels and transcript container - same color as body */
    .left-panel, .right-panel {
        background-color: #121212;
        padding: 1.5rem;
        border-radius: 0;
        height: 100%;
    }
    .video-panel iframe {
        width: 100%;
        border: none;
        border-radius: 8px;
    }
    .video-info {
        margin-top: 1rem;
        color: #cccccc;
        font-weight: 600;
    }
    .transcript-container {
        padding: 1rem;
        background-color: #121212;
        border-radius: 0;
        max-height: 500px;
        overflow-y: auto;
        margin-top: 1rem;
        font-weight: 500;
    }
    .transcript-line {
        margin-bottom: 0.5rem;
    }
    .timestamp {
        color: #007acc;
        font-weight: 700;
        margin-right: 0.7rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="title-text">YouTube Transcript Extractor</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-text">Convert a YouTube video to transcript, copy and download the generated transcript in one click.</div>', unsafe_allow_html=True)
    
    youtube_url = st.text_input(
        label="YouTube URL",
        label_visibility="collapsed",
        key="custom_input_url"
    )
    
    if st.button("Get Transcript"):
        if not youtube_url.strip():
            st.warning("Please enter a valid YouTube link.")
            return
        
        video_id = extract_video_id(youtube_url.strip())
        channel_video_details = get_channel_and_video_details(video_id)
        
        available_languages = []
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            for t in transcript_list:
                display_name = t.language
                if t.is_generated:
                    display_name += " (auto-generated)"
                available_languages.append((display_name, t.language_code))
        except:
            pass
        
        selected_language_code = None
        if available_languages:
            lang_display_names = [item[0] for item in available_languages]
            selected_display = st.selectbox(
                "Select Transcript Language:",
                lang_display_names,
                help="Pick the language you'd like"
            )
            for (dname, dcode) in available_languages:
                if dname == selected_display:
                    selected_language_code = dcode
                    break
        
        if selected_language_code:
            transcript_data = get_transcript_data(video_id, [selected_language_code])
        else:
            transcript_data = get_transcript_data(video_id, None)
        
        final_transcript = []
        if transcript_data:
            if isinstance(transcript_data[0], dict):
                final_transcript = transcript_data
            else:
                for snippet in transcript_data:
                    snippet_dict = {
                        "start": snippet.start,
                        "duration": snippet.duration,
                        "text": snippet.text
                    }
                    final_transcript.append(snippet_dict)
        
        if final_transcript:
            col_left, col_right = st.columns([1, 1])
            with col_left:
                st.markdown('<div class="left-panel">', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="video-panel">
                  <iframe height="220"
                    src="https://www.youtube.com/embed/{channel_video_details['video_id']}"
                    allowfullscreen>
                  </iframe>
                </div>
                <div class="video-info" style="margin-top:1rem;">
                  <p><b>Channel ID:</b> {channel_video_details["channel_id"]}</p>
                  <p><b>Video ID:</b> {channel_video_details["video_id"]}</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_right:
                st.markdown('<div class="right-panel">', unsafe_allow_html=True)
                st.markdown('<div class="transcript-container">', unsafe_allow_html=True)
                
                for line in final_transcript:
                    start_ts = format_timestamp(line["start"])
                    text_line = line["text"].strip()
                    st.markdown(
                        f'<div class="transcript-line"><span class="timestamp">{start_ts}</span>{text_line}</div>',
                        unsafe_allow_html=True
                    )
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("No transcript found or transcripts disabled.")

if __name__ == "__main__":
    main()
