"""
This file contains the main logic for the Streamlit application, including
the overall layout, user interaction, and coordination between different
modules such as UI, transcript extraction, and AI processing.
"""

import streamlit as st
from .ui import (
    custom_css,
    main_header,
    sidebar,
    display_transcript,
    display_notes,
    display_chat,
)
from .transcript_extractor import YouTubeTranscriptExtractor
from .gemini_ai import GeminiAI
from datetime import datetime


def main():
    """
    Main function to run the Streamlit application.

    This function sets up the page configuration, initializes the session state,
    and orchestrates the display of UI components and the application's logic.
    """
    # Page configuration
    st.set_page_config(
        page_title="YouTube Transcript Extractor",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Apply custom CSS and display the main header
    custom_css()
    main_header()

    # Initialize session state variables if they don't exist
    if "transcript_data" not in st.session_state:
        st.session_state.transcript_data = None
    if "transcript_text" not in st.session_state:
        st.session_state.transcript_text = ""
    if "video_info" not in st.session_state:
        st.session_state.video_info = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "note_counter" not in st.session_state:
        st.session_state.note_counter = 0

    # Display the sidebar and get configuration settings
    use_proxy, proxy_config, gemini_api_key = sidebar()

    # Main layout with two columns
    col1, col2 = st.columns([2, 1])

    # Left column for transcript extraction and display
    with col1:
        st.subheader("📥 Extract Transcript")
        video_url = st.text_input(
            "YouTube Video URL",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Paste any YouTube video URL here",
        )

        extract_btn = st.button(
            "🚀 Extract Transcript", type="primary", use_container_width=True
        )

        # Handle transcript extraction when the button is clicked
        if extract_btn and video_url:
            with st.spinner("Extracting transcript..."):
                extractor = YouTubeTranscriptExtractor()
                transcript, message = extractor.extract_transcript(
                    video_url, use_proxy=use_proxy, proxy_config=proxy_config
                )

                if transcript:
                    st.session_state.transcript_data = transcript
                    st.session_state.video_info = extractor.video_info

                    # Convert transcript to a formatted text string
                    transcript_text = ""
                    for entry in transcript:
                        start_time = entry.get("start", 0)
                        minutes = int(start_time // 60)
                        seconds = int(start_time % 60)
                        timestamp = f"{minutes:02d}:{seconds:02d}"
                        transcript_text += f"[{timestamp}] {entry['text']}\n"

                    st.session_state.transcript_text = transcript_text
                    st.markdown(
                        f'<div class="success-box">✅ {message}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    # Display error message and troubleshooting tips if extraction fails
                    st.markdown(
                        f'<div class="warning-box">❌ {message}</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        """
                    ### 🔧 Troubleshooting Tips:
                    1. **Enable Proxy**: Check the "Use Proxy" option in the sidebar and configure a proxy server
                    2. **Try Different Video**: Some videos may have transcripts disabled
                    3. **Wait and Retry**: Your IP might be temporarily blocked - try again later
                    4. **Use VPN**: Connect through a VPN to change your IP address
                    5. **Check Video Availability**: Ensure the video is public and has captions
                    """
                    )

        # Display the transcript if it has been extracted
        if st.session_state.transcript_data:
            display_transcript()

    # Right column for AI-powered insights and actions
    with col2:
        st.subheader("🧠 Insights & Actions")
        if st.session_state.transcript_text and gemini_api_key:
            gemini = GeminiAI(gemini_api_key)

            # Action buttons for generating AI content
            col_a, col_b = st.columns(2)

            with col_a:
                if st.button("📊 Summarize", use_container_width=True):
                    with st.spinner("Generating summary..."):
                        summary = gemini.generate_summary(
                            st.session_state.transcript_text
                        )
                        st.session_state.note_counter += 1
                        note_id = f"summary_{st.session_state.note_counter}"
                        st.session_state[f"note_{note_id}"] = {
                            "content": summary,
                            "type": "Summary",
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        }
                        st.rerun()

                if st.button("💎 Key Quotes", use_container_width=True):
                    with st.spinner("Extracting quotes..."):
                        quotes = gemini.extract_key_quotes(
                            st.session_state.transcript_text
                        )
                        st.session_state.note_counter += 1
                        note_id = f"quotes_{st.session_state.note_counter}"
                        st.session_state[f"note_{note_id}"] = {
                            "content": quotes,
                            "type": "Key Quotes",
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        }
                        st.rerun()

                if st.button("❓ Q&A", use_container_width=True):
                    with st.spinner("Generating Q&A..."):
                        qa = gemini.generate_qa(st.session_state.transcript_text)
                        st.session_state.note_counter += 1
                        note_id = f"qa_{st.session_state.note_counter}"
                        st.session_state[f"note_{note_id}"] = {
                            "content": qa,
                            "type": "Q&A",
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        }
                        st.rerun()

            with col_b:
                if st.button("📚 Study Guide", use_container_width=True):
                    with st.spinner("Creating study guide..."):
                        guide = gemini.create_study_guide(
                            st.session_state.transcript_text
                        )
                        st.session_state.note_counter += 1
                        note_id = f"study_{st.session_state.note_counter}"
                        st.session_state[f"note_{note_id}"] = {
                            "content": guide,
                            "type": "Study Guide",
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        }
                        st.rerun()

                if st.button("🎯 Flash Cards", use_container_width=True):
                    with st.spinner("Creating flashcards..."):
                        cards = gemini.create_flashcards(
                            st.session_state.transcript_text
                        )
                        st.session_state.note_counter += 1
                        note_id = f"flashcards_{st.session_state.note_counter}"
                        st.session_state[f"note_{note_id}"] = {
                            "content": cards,
                            "type": "Flash Cards",
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        }
                        st.rerun()

                if st.button("✨ Highlights", use_container_width=True):
                    with st.spinner("Extracting insights..."):
                        insights = gemini.highlight_insights(
                            st.session_state.transcript_text
                        )
                        st.session_state.note_counter += 1
                        note_id = f"highlights_{st.session_state.note_counter}"
                        st.session_state[f"note_{note_id}"] = {
                            "content": insights,
                            "type": "Highlights",
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        }
                        st.rerun()

        elif st.session_state.transcript_text:
            st.info("🔑 Enter Gemini API key to enable AI features")
        else:
            st.info("📥 Extract a transcript first to enable insights")

    # Display the notes and chat sections
    display_notes()
    if gemini_api_key:
        display_chat(gemini_api_key)

    # Footer
    st.divider()
    st.markdown(
        """
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🚀 Built with Streamlit & Gemini AI | 
        <a href="https://ai.google.dev/" target="_blank">Get Gemini API Key</a> | 
        Made with ❤️ for learning</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
