"""
UI module for the YouTube Transcript Extractor.

This module contains functions for rendering the user interface components
of the Streamlit application, including custom CSS, headers, sidebars,
and the main content display areas for transcripts, notes, and chat.
"""

import streamlit as st
from datetime import datetime
from .utils import create_download_link, display_content_with_actions
from .gemini_ai import GeminiAI

def custom_css():
    """
    Applies custom CSS to the Streamlit application for a professional look and feel.
    """
    st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
            padding: 2rem;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .main-header h1 {
            color: white;
            margin: 0;
            font-size: 2.5rem;
            font-weight: bold;
        }
        
        .feature-card {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid #FF6B6B;
            margin: 1rem 0;
        }
        
        .transcript-container {
            background: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 1.5rem;
            max-height: 400px;
            overflow-y: auto;
            margin: 1rem 0;
            color: #2c3e50;
    }
        
        .content-display {
            background: #f8f9fa;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 1.5rem;
            max-height: 500px;
            overflow-y: auto;
            margin: 1rem 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #2c3e50;    
        }
        
        .content-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #4ECDC4;
        }
        
        .content-title {
            font-size: 1.2rem;
            font-weight: bold;
            color: #2c3e50;
            margin: 0;
        }
        
        .content-actions {
            display: flex;
            gap: 0.5rem;
        }
        
        .action-btn {
            background: #4ECDC4;
            color: white;
            border: none;
            padding: 0.3rem 0.8rem;
            border-radius: 4px;
            font-size: 0.8rem;
            cursor: pointer;
            text-decoration: none;
        }
        
        .action-btn:hover {
            background: #44A08D;
        }
        
        .delete-btn {
            background: #e74c3c;
        }
        
        .delete-btn:hover {
            background: #c0392b;
        }
        
        .timestamp {
            color: #FF6B6B;
            font-weight: bold;
            font-size: 0.9rem;
        }
        
        .transcript-text {
            margin: 0.5rem 0;
            line-height: 1.6;
        }
        
        .insight-card {
            background: linear-gradient(145deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        
        .action-button {
            background: linear-gradient(90deg, #4ECDC4, #44A08D);
            color: white;
            border: none;
            padding: 0.8rem 1.5rem;
            border-radius: 5px;
            cursor: pointer;
            margin: 0.5rem;
            font-weight: bold;
        }
        
        .video-info {
            background: #f1f3f4;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            color: #2c3e50;    
        }
        
        .warning-box {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .success-box {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .notes-section {
            background: #2c3e50;
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        .note-item {
            background: #34495e;
            padding: 1rem;
            border-radius: 6px;
            margin: 0.5rem 0;
            border-left: 4px solid #4ECDC4;
        }
        
        .note-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }
        
        .note-type {
            background: #4ECDC4;
            color: white;
            padding: 0.2rem 0.5rem;
            border-radius: 3px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        
        .note-timestamp {
            color: #bdc3c7;
            font-size: 0.8rem;
        }
    </style>
    """, unsafe_allow_html=True)

def main_header():
    """
    Displays the main header of the application.
    """
    st.markdown("""
    <div class="main-header">
        <h1>🎬 YouTube Transcript Extractor</h1>
        <p style="color: white; margin: 0;">Extract, Analyze, and Chat with YouTube Video Transcripts</p>
    </div>
    """, unsafe_allow_html=True)

def sidebar():
    """
    Renders the sidebar with configuration options for proxy settings and API keys.
    
    Returns:
        tuple: A tuple containing use_proxy (bool), proxy_config (str), and 
               gemini_api_key (str).
    """
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        st.subheader("🔒 Proxy Settings")
        use_proxy = st.checkbox("Use Proxy", help="Enable if you're getting IP blocked errors")
        
        proxy_config = None
        if use_proxy:
            proxy_type = st.selectbox("Proxy Type", ["HTTP", "HTTPS", "SOCKS5"])
            proxy_host = st.text_input("Proxy Host", placeholder="proxy.example.com")
            proxy_port = st.text_input("Proxy Port", placeholder="8080")
            proxy_user = st.text_input("Username (optional)", placeholder="username")
            proxy_pass = st.text_input("Password (optional)", type="password", placeholder="password")
            
            if proxy_host and proxy_port:
                if proxy_user and proxy_pass:
                    proxy_config = f"{proxy_type.lower()}://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"
                else:
                    proxy_config = f"{proxy_type.lower()}://{proxy_host}:{proxy_port}"
                st.success("✅ Proxy configured")
            elif use_proxy:
                st.warning("⚠️ Please enter proxy host and port")

        # Gemini API Key input
        gemini_api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Get your free API key from https://ai.google.dev/"
        )
        
        if gemini_api_key:
            st.success("✅ Gemini API configured")
        else:
            st.warning("⚠️ Enter Gemini API key to enable AI features")
        
        st.divider()
        
        # Display status of available libraries
        st.subheader("📚 Available Libraries")
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            st.success("✅ YouTube Transcript API")
        except ImportError:
            st.error("❌ YouTube Transcript API (install: pip install youtube-transcript-api)")
            
        try:
            import yt_dlp
            st.success("✅ yt-dlp")
        except ImportError:
            st.error("❌ yt-dlp (install: pip install yt-dlp)")

    return use_proxy, proxy_config, gemini_api_key

def display_transcript():
    """
    Displays the extracted transcript and related information, including video details,
    search functionality, and an interactive transcript viewer with options to copy,
    download, and add notes.
    """
    st.subheader("📝 Video Info")
    
    # Display video information if available
    if st.session_state.video_info:
        st.markdown(f"""
        <div class="video-info">
            <strong>Video ID:</strong> {st.session_state.video_info['video_id']}<br>
            <strong>Extracted:</strong> {st.session_state.video_info['extracted_at']}<br>
            <strong>Total Segments:</strong> {len(st.session_state.transcript_data)}
        </div>
        """, unsafe_allow_html=True)

    # Button to show/hide the transcript
    view_transcript = st.button("📋 View Transcript")
    if view_transcript:
        st.session_state.show_transcript = True

    # Display the transcript content if the user chooses to view it
    if st.session_state.get('show_transcript', False):
        st.subheader("📋 Transcript Content")
        
        if 'transcript_notes' not in st.session_state:
            st.session_state.transcript_notes = {}
        
        search_term = st.text_input("🔍 Search in transcript:", placeholder="Enter word or phrase to search...")
        
        # Action buttons for the whole transcript
        col1_inner, col2_inner, col3_inner = st.columns([1, 1, 1])
        with col1_inner:
            if st.button("📋 Copy Whole Transcript", use_container_width=True):
                # Logic to copy the entire transcript to the clipboard
                clean_transcript = ""
                current_paragraph = []
                
                for entry in st.session_state.transcript_data:
                    text = entry['text'].strip()
                    current_paragraph.append(text)
                    
                    if (text.endswith('.') or text.endswith('!') or text.endswith('?') or 
                        len(current_paragraph) >= 3):
                        clean_transcript += ' '.join(current_paragraph) + '\n\n'
                        current_paragraph = []
                
                if current_paragraph:
                    clean_transcript += ' '.join(current_paragraph)
                
                st.session_state.clean_transcript_copy = clean_transcript
                
                js_safe_transcript = clean_transcript.replace('\\', '\\\\').replace('`', '\\`')
                copy_js = f"""
                <script>
                function copyToClipboard() {{
                    const textToCopy = `{js_safe_transcript}`;
                    navigator.clipboard.writeText(textToCopy).then(function() {{
                        console.log('Transcript copied to clipboard successfully!');
                    }}, function(err) {{
                        console.error('Could not copy transcript: ', err);
                        const textArea = document.createElement("textarea");
                        textArea.value = textToCopy;
                        document.body.appendChild(textArea);
                        textArea.focus();
                        textArea.select();
                        try {{
                            const successful = document.execCommand('copy');
                            if (successful) {{
                                console.log('Transcript copied using fallback method!');
                            }}
                        }} catch (err) {{
                            console.error('Fallback copy failed: ', err);
                        }}
                        document.body.removeChild(textArea);
                    }});
                }}
                copyToClipboard();
                </script>
                """
                
                st.components.v1.html(copy_js, height=0)
                st.success("✅ Transcript copied to clipboard!")
        
        if st.session_state.get('clean_transcript_copy'):
            with st.expander("📋 Clean Transcript (Manual Copy Backup)", expanded=False):
                st.text_area(
                    "Clean transcript without timestamps:",
                    value=st.session_state.clean_transcript_copy,
                    height=200,
                    help="Select all text and copy (Ctrl+A, Ctrl+C) - This is a backup if automatic copy didn't work"
                )
        
        with col2_inner:
            # Logic to download the transcript as a text file
            def create_download_transcript():
                clean_transcript = ""
                current_paragraph = []
                paragraph_index = 0
                
                for i, entry in enumerate(st.session_state.transcript_data):
                    text = entry['text'].strip()
                    current_paragraph.append(text)
                    
                    if (text.endswith('.') or text.endswith('!') or text.endswith('?') or 
                        len(current_paragraph) >= 3):
                        paragraph_text = ' '.join(current_paragraph)
                        
                        if paragraph_index in st.session_state.transcript_notes:
                            clean_transcript += "--- NOTE SECTION START ---\n"
                            clean_transcript += paragraph_text + '\n'
                            clean_transcript += f'"{st.session_state.transcript_notes[paragraph_index]}"\n'
                            clean_transcript += "--- NOTE SECTION END ---\n\n"
                        else:
                            clean_transcript += paragraph_text + '\n\n'
                        
                        current_paragraph = []
                        paragraph_index += 1
                
                if current_paragraph:
                    paragraph_text = ' '.join(current_paragraph)
                    if paragraph_index in st.session_state.transcript_notes:
                        clean_transcript += "--- NOTE SECTION START ---\n"
                        clean_transcript += paragraph_text + '\n'
                        clean_transcript += f'"{st.session_state.transcript_notes[paragraph_index]}"\n'
                        clean_transcript += "--- NOTE SECTION END ---\n"
                    else:
                        clean_transcript += paragraph_text
                
                return clean_transcript
            
            transcript_content = create_download_transcript()
            st.download_button(
                "📥 Download Transcript",
                data=transcript_content,
                file_name=f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col3_inner:
            if st.button("⬇️ Hide Transcript", use_container_width=True):
                st.session_state.show_transcript = False
                st.rerun()
        
        # Process and display the transcript in paragraphs
        paragraphs = []
        current_paragraph = []
        current_timestamps = []
        
        for entry in st.session_state.transcript_data:
            text = entry['text'].strip()
            start_time = entry.get('start', 0)
            current_paragraph.append(text)
            current_timestamps.append(start_time)
            
            if (text.endswith('.') or text.endswith('!') or text.endswith('?') or 
                len(current_paragraph) >= 3):
                paragraph_text = ' '.join(current_paragraph)
                start_timestamp = current_timestamps[0]
                minutes = int(start_timestamp // 60)
                seconds = int(start_timestamp % 60)
                timestamp_str = f"{minutes:02d}:{seconds:02d}"
                
                paragraphs.append({
                    'text': paragraph_text,
                    'timestamp': timestamp_str,
                    'start_time': start_timestamp
                })
                current_paragraph = []
                current_timestamps = []
        
        if current_paragraph:
            paragraph_text = ' '.join(current_paragraph)
            start_timestamp = current_timestamps[0] if current_timestamps else 0
            minutes = int(start_timestamp // 60)
            seconds = int(start_timestamp % 60)
            timestamp_str = f"{minutes:02d}:{seconds:02d}"
            
            paragraphs.append({
                'text': paragraph_text,
                'timestamp': timestamp_str,
                'start_time': start_timestamp
            })
        
        # Scrollable container for the transcript
        transcript_container = st.container()
        with transcript_container:
            with st.container(height=400):
                for i, paragraph in enumerate(paragraphs):
                    # Highlight search term if found
                    display_text = paragraph['text']
                    if search_term and search_term.lower() in display_text.lower():
                        import re
                        pattern = re.compile(re.escape(search_term), re.IGNORECASE)
                        display_text = pattern.sub(
                            f'<mark style="background-color: #ffeb3b; padding: 2px 4px; border-radius: 3px;">{search_term}</mark>',
                            display_text
                        )
                    
                    # Display each paragraph with timestamp and actions
                    st.markdown(f"""
                    <div style="margin-bottom: 1.5rem; padding: 1rem; border-left: 3px solid #4ECDC4; background: #f8f9fa; border-radius: 0 8px 8px 0;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <span style="color: #FF6B6B; font-weight: bold; font-size: 0.9rem;">[{paragraph['timestamp']}]</span>
                        </div>
                        <div style="margin: 0.5rem 0; line-height: 1.6; color: #2c3e50;">{display_text}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Buttons for copying and adding notes to each paragraph
                    col_copy, col_note, col_spacer = st.columns([1, 1, 4])
                    with col_copy:
                        if st.button("📋 Copy", key=f"copy_para_{i}", help="Copy this paragraph"):
                            st.session_state[f"copied_text_{i}"] = paragraph['text']
                            st.success("✅ Copied to session!")
                    
                    with col_note:
                        if st.button("📝 Note", key=f"note_para_{i}", help="Add note to this paragraph"):
                            st.session_state[f"show_note_input_{i}"] = True
                    
                    # Input area for adding/editing notes
                    if st.session_state.get(f"show_note_input_{i}", False):
                        note_input = st.text_area(
                            f"Add note for paragraph {i+1}:",
                            key=f"note_input_para_{i}",
                            height=80
                        )
                        
                        col_save, col_cancel = st.columns([1, 1])
                        with col_save:
                            if st.button("💾 Save Note", key=f"save_note_para_{i}"):
                                if note_input.strip():
                                    st.session_state.transcript_notes[i] = note_input.strip()
                                    st.session_state[f"show_note_input_{i}"] = False
                                    st.success(f"✅ Note saved for paragraph {i+1}")
                                    st.rerun()
                        
                        with col_cancel:
                            if st.button("❌ Cancel", key=f"cancel_note_para_{i}"):
                                st.session_state[f"show_note_input_{i}"] = False
                                st.rerun()
                    
                    # Display existing note for the paragraph
                    if i in st.session_state.transcript_notes:
                        st.markdown(f"""
                        <div style="margin-top: 0.5rem; padding: 0.5rem; background: #e8f5e8; border-radius: 4px; border-left: 3px solid #4ECDC4;">
                            <strong>📝 Your Note:</strong> {st.session_state.transcript_notes[i]}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"✏️ Edit Note", key=f"edit_note_para_{i}"):
                            st.session_state[f"show_note_input_{i}"] = True
                            st.rerun()
        
        # Display recently copied paragraphs
        copied_texts = []
        for key in st.session_state.keys():
            if key.startswith("copied_text_"):
                para_idx = key.split("_")[-1]
                copied_texts.append((para_idx, st.session_state[key]))
        
        if copied_texts:
            st.subheader("📋 Copied Paragraphs")
            for para_idx, text in copied_texts[-3:]:
                with st.expander(f"Copied Paragraph {int(para_idx)+1}"):
                    st.text_area("Text:", value=text, height=100, disabled=True)
                    if st.button(f"Clear", key=f"clear_copied_{para_idx}"):
                        del st.session_state[f"copied_text_{para_idx}"]
                        st.rerun()
        
        # Display a summary of all notes
        if st.session_state.transcript_notes:
            st.subheader("📝 Notes Summary")
            for para_idx, note in st.session_state.transcript_notes.items():
                if para_idx < len(paragraphs):
                    with st.expander(f"Note for Paragraph {para_idx + 1} [{paragraphs[para_idx]['timestamp']}]"):
                        st.write("**Paragraph:**", paragraphs[para_idx]['text'][:100] + "...")
                        st.write("**Note:**", note)
                        if st.button(f"🗑️ Delete Note", key=f"delete_note_summary_{para_idx}"):
                            del st.session_state.transcript_notes[para_idx]
                            st.rerun()

def display_notes():
    """
    Displays the section for user-generated notes, such as summaries, quotes, etc.
    """
    st.divider()
    st.subheader("📋 Your Notes")
    
    # Retrieve and sort notes from session state
    notes = [] 
    for key, value in st.session_state.items():
        if key.startswith('note_') and isinstance(value, dict):
            note_id = key.replace('note_', '')
            notes.append({
                'id': note_id,
                'content': value['content'],
                'type': value['type'],
                'timestamp': value['timestamp']
            })

    notes = sorted(notes, key=lambda x: x['timestamp'], reverse=True)
    
    # Display each note in an expander
    if notes:
        for note in notes:
            with st.expander(f"📝 {note['type']} - {note['timestamp']}", expanded=False):
                display_content_with_actions(
                    note['content'], 
                    note['type'], 
                    note['type'], 
                    note['id']
                )
    else:
        st.info("No notes yet. Generate summaries, quotes, or other insights to see them here!")

def display_chat(gemini_api_key):
    """
    Displays the chat interface for interacting with the transcript content.
    
    Args:
        gemini_api_key (str): The API key for the Gemini AI model.
    """
    st.divider()
    st.subheader("💬 Chat with Transcript")
    
    gemini = GeminiAI(gemini_api_key)
    
    # Input for user's question
    chat_question = st.text_input(
        "Ask a question about the video content:",
        placeholder="What are the main points discussed in this video?"
    )
    
    # Handle chat submission
    if st.button("💬 Ask", use_container_width=True) and chat_question:
        with st.spinner("Thinking..."):
            answer = gemini.chat_with_transcript(st.session_state.transcript_text, chat_question)
            
            st.session_state.chat_history.append({
                'question': chat_question,
                'answer': answer,
                'timestamp': datetime.now().strftime("%H:%M:%S")
            })
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### 💭 Chat History")
        for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):
            with st.expander(f"Q: {chat['question'][:50]}... ({chat['timestamp']})"):
                st.write("**Question:**", chat['question'])
                st.write("**Answer:**", chat['answer'])
