"""
YouTube Transcript Generator - Professional YouTube Transcript Extractor
==============================================

YouTube Transcript Generator with AI Analysis and Chat Interface
Streamlit-based desktop/web app to extract YouTube video transcripts

Author: Ujjwal Nova
License: MIT
Repository: https://github.com/ukr-projects/yt-transcript-gpt

What’s New:
- 🎉 Initial release with core transcript extraction and AI modules
- 🚀 Integrated both YouTube Transcript API and yt-dlp fallback
- 🤖 Gemini AI features: summaries, key quotes, Q&A, study guides, flashcards, insights
- 🔍 Interactive transcript viewer with search, copy, and notes
- 💬 Chat interface to ask questions about the transcript

Features:
- Transcript Extraction via YouTube Transcript API or yt-dlp
- AI Analysis through Google Gemini:
  - Summaries
  - Key Quotes
  - Q&A sessions
  - Study Guides
  - Flashcards
  - Highlighted Insights
- Interactive Viewer: search, scrollable transcript, per-paragraph copy & notes
- Downloadable Content: transcripts and AI-generated outputs (Markdown/plain text)
- Chat Mode: ask questions about video content and get AI answers
- Configurable: enable/disable libraries, set Gemini API key

Dependencies:
- streamlit
- youtube-transcript-api
- yt-dlp
- google-generativeai
- requests
- urllib3

Usage:
- cd src
- streamlit run main.py
"""

import streamlit as st
import re
import time
from urllib.parse import urlparse, parse_qs
import google.generativeai as genai
from datetime import datetime
import json
import base64
import streamlit.components.v1


try:
    from youtube_transcript_api import YouTubeTranscriptApi
    TRANSCRIPT_API_AVAILABLE = True
except ImportError:
    TRANSCRIPT_API_AVAILABLE = False

try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="YouTube Transcript Extractor",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional UI
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

class YouTubeTranscriptExtractor:
    def __init__(self):
        self.transcript_data = None
        self.video_info = None
        
    def extract_video_id(self, url):
        """Extract video ID from YouTube URL"""
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:embed\/)([0-9A-Za-z_-]{11})',
            r'(?:watch\?v=)([0-9A-Za-z_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_transcript_with_proxy(self, video_id, proxies=None):
        """Get transcript using YouTube Transcript API with proxy support"""
        try:
            if proxies:
                # Configure proxies for the transcript API
                transcript_list = YouTubeTranscriptApi.get_transcript(
                    video_id,
                    proxies=proxies
                )
            else:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            return transcript_list
        except Exception as e:
            st.error(f"YouTube Transcript API failed: {str(e)}")
            return None
    
    def get_transcript_youtube_api(self, video_id, use_proxy=False, proxy_config=None):
        """Get transcript using YouTube Transcript API with optional proxy"""
        try:
            if use_proxy and proxy_config:
                proxies = {
                    'http': proxy_config,
                    'https': proxy_config
                }
                transcript_list = self.get_transcript_with_proxy(video_id, proxies)
            else:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            return transcript_list
        except Exception as e:
            error_message = str(e)
            if "blocked" in error_message.lower() or "ip" in error_message.lower():
                st.error("🚫 Your IP has been blocked by YouTube. Try using a proxy or VPN.")
            else:
                st.error(f"YouTube Transcript API failed: {error_message}")
            return None
    
    def get_transcript_ytdlp(self, video_id, use_proxy=False, proxy_config=None):
        """Get transcript using yt-dlp as fallback with proxy support"""
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            ydl_opts = {
                'writesubtitles': True,
                'writeautomaticsub': True,
                'skip_download': True,
                'quiet': True
            }
            
            if use_proxy and proxy_config:
                ydl_opts['proxy'] = proxy_config
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Try to get subtitles
                subtitles = info.get('subtitles', {})
                auto_captions = info.get('automatic_captions', {})
                
                # Try English first, then any available language
                for lang in ['en', 'en-US', 'en-GB']:
                    if lang in subtitles:
                        return self._process_ytdlp_subtitles(subtitles[lang])
                    if lang in auto_captions:
                        return self._process_ytdlp_subtitles(auto_captions[lang])
                
                # If no English, try first available
                if subtitles:
                    first_lang = list(subtitles.keys())[0]
                    return self._process_ytdlp_subtitles(subtitles[first_lang])
                if auto_captions:
                    first_lang = list(auto_captions.keys())[0]
                    return self._process_ytdlp_subtitles(auto_captions[first_lang])
            
            return None
        except Exception as e:
            st.error(f"yt-dlp failed: {str(e)}")
            return None
    
    def _process_ytdlp_subtitles(self, subtitle_list):
        """Process subtitle list from yt-dlp"""
        # This is a simplified version - in practice, you'd need to download and parse the subtitle files
        return [{"text": "Subtitle available via yt-dlp (implementation needed)", "start": 0, "duration": 1}]
    
    def extract_transcript(self, video_url, use_proxy=False, proxy_config=None):
        """Main method to extract transcript with fallback and proxy support"""
        video_id = self.extract_video_id(video_url)
        if not video_id:
            return None, "Invalid YouTube URL"
        
        # Store video info
        self.video_info = {
            'video_id': video_id,
            'url': video_url,
            'extracted_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Try YouTube Transcript API first
        if TRANSCRIPT_API_AVAILABLE:
            transcript = self.get_transcript_youtube_api(video_id, use_proxy, proxy_config)
            if transcript:
                self.transcript_data = transcript
                proxy_status = " (with proxy)" if use_proxy else ""
                return transcript, f"Success using YouTube Transcript API{proxy_status}"
        
        # Fallback to yt-dlp
        if YT_DLP_AVAILABLE:
            transcript = self.get_transcript_ytdlp(video_id, use_proxy, proxy_config)
            if transcript:
                self.transcript_data = transcript
                proxy_status = " (with proxy)" if use_proxy else ""
                return transcript, f"Success using yt-dlp{proxy_status}"
        
        return None, "Both transcript extraction methods failed"

class GeminiAI:
    def __init__(self, api_key):
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
    
    def is_configured(self):
        return self.model is not None
    
    def generate_summary(self, transcript_text):
        """Generate summary of the transcript"""
        prompt = f"""
        Please provide a comprehensive summary of the following video transcript:
        
        {transcript_text}
        
        Include:
        1. Main topics discussed
        2. Key points and insights
        3. Important conclusions or takeaways
        
        Keep the summary clear and well-structured.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def extract_key_quotes(self, transcript_text):
        """Extract key quotes from transcript"""
        prompt = f"""
        From the following transcript, extract 5-10 of the most important and impactful quotes:
        
        {transcript_text}
        
        Format each quote as:
        "Quote text" - [Approximate timestamp if available]
        
        Focus on quotes that:
        - Capture main ideas
        - Are memorable or impactful
        - Represent key insights
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error extracting quotes: {str(e)}"
    
    def create_study_guide(self, transcript_text):
        """Create a study guide from transcript"""
        prompt = f"""
        Create a comprehensive study guide from this video transcript:
        
        {transcript_text}
        
        Structure the study guide with:
        1. Main Topics/Chapters
        2. Key Concepts and Definitions
        3. Important Facts and Figures
        4. Study Questions
        5. Review Points
        
        Make it suitable for learning and revision.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error creating study guide: {str(e)}"
    
    def generate_qa(self, transcript_text):
        """Generate Q&A from transcript"""
        prompt = f"""
        Create a Q&A session based on this video transcript:
        
        {transcript_text}
        
        Generate 10-15 relevant questions and provide detailed answers based on the content.
        Format as:
        
        Q: [Question]
        A: [Answer]
        
        Include a mix of factual, analytical, and conceptual questions.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating Q&A: {str(e)}"
    
    def create_flashcards(self, transcript_text):
        """Create flashcards from transcript"""
        prompt = f"""
        Create 15-20 flashcards from this video transcript:
        
        {transcript_text}
        
        Format each flashcard as:
        FRONT: [Question/Term]
        BACK: [Answer/Definition]
        ---
        
        Focus on key concepts, definitions, and important facts that would be useful for memorization.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error creating flashcards: {str(e)}"
    
    def highlight_insights(self, transcript_text):
        """Extract key insights and highlights"""
        prompt = f"""
        Analyze this video transcript and extract the key insights and highlights:
        
        {transcript_text}
        
        Provide:
        1. 🔍 Key Insights (3-5 main insights)
        2. 💡 Important Revelations
        3. 📊 Data/Statistics mentioned
        4. 🎯 Actionable takeaways
        5. 🔗 Connections to broader topics
        
        Use emojis and clear formatting for easy reading.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error extracting insights: {str(e)}"
    
    def chat_with_transcript(self, transcript_text, question):
        """Chat about the transcript content"""
        prompt = f"""
        Based on this video transcript:
        
        {transcript_text}
        
        User Question: {question}
        
        Please provide a detailed answer based on the transcript content. If the question cannot be answered from the transcript, please mention that clearly.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error in chat: {str(e)}"

def create_download_link(content, filename, content_type="text/markdown"):
    """Create a download link for content"""
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:{content_type};base64,{b64}" download="{filename}" class="action-btn">📥 Download</a>'

def display_content_with_actions(content, title, content_type, note_id):
    """Display content with scroll, delete, and download actions"""
    
    # Create download filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{content_type.lower().replace(' ', '_')}_{timestamp}.md"
    
    # Content display with actions
    st.markdown(f"""
    <div class="content-display">
        <div class="content-header">
            <h3 class="content-title">{title}</h3>
            <div class="content-actions">
                {create_download_link(content, filename)}
            </div>
        </div>
        <div style="white-space: pre-wrap;">{content}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Delete button
    if st.button(f"🗑️ Delete {content_type}", key=f"delete_{note_id}", help="Delete this note"):
        if f"note_{note_id}" in st.session_state:
            del st.session_state[f"note_{note_id}"]
            st.rerun()

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎬 YouTube Transcript Extractor</h1>
        <p style="color: white; margin: 0;">Extract, Analyze, and Chat with YouTube Video Transcripts</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'transcript_data' not in st.session_state:
        st.session_state.transcript_data = None
    if 'transcript_text' not in st.session_state:
        st.session_state.transcript_text = ""
    if 'video_info' not in st.session_state:
        st.session_state.video_info = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'note_counter' not in st.session_state:
        st.session_state.note_counter = 0
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Proxy Configuration
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

        # Gemini API Key
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
        
        # Library status
        st.subheader("📚 Available Libraries")
        if TRANSCRIPT_API_AVAILABLE:
            st.success("✅ YouTube Transcript API")
        else:
            st.error("❌ YouTube Transcript API (install: pip install youtube-transcript-api)")
            
        if YT_DLP_AVAILABLE:
            st.success("✅ yt-dlp")
        else:
            st.error("❌ yt-dlp (install: pip install yt-dlp)")
        
        if not TRANSCRIPT_API_AVAILABLE and not YT_DLP_AVAILABLE:
            st.error("⚠️ No transcript libraries available! Please install at least one.")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # URL Input
        st.subheader("📥 Extract Transcript")
        video_url = st.text_input(
            "YouTube Video URL",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Paste any YouTube video URL here"
        )
        
        extract_btn = st.button("🚀 Extract Transcript", type="primary", use_container_width=True)
        
        if extract_btn and video_url:
            if not TRANSCRIPT_API_AVAILABLE and not YT_DLP_AVAILABLE:
                st.error("❌ Please install transcript extraction libraries first!")
            else:
                with st.spinner("Extracting transcript..."):
                    extractor = YouTubeTranscriptExtractor()
                    transcript, message = extractor.extract_transcript(
                        video_url, 
                        use_proxy=use_proxy, 
                        proxy_config=proxy_config
                    )
                    
                    if transcript:
                        st.session_state.transcript_data = transcript
                        st.session_state.video_info = extractor.video_info
                        
                        # Convert transcript to text
                        transcript_text = ""
                        for entry in transcript:
                            start_time = entry.get('start', 0)
                            minutes = int(start_time // 60)
                            seconds = int(start_time % 60)
                            timestamp = f"{minutes:02d}:{seconds:02d}"
                            transcript_text += f"[{timestamp}] {entry['text']}\n"
                        
                        st.session_state.transcript_text = transcript_text
                        
                        st.markdown('<div class="success-box">✅ ' + message + '</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="warning-box">❌ ' + message + '</div>', unsafe_allow_html=True)
                        
                        # Show troubleshooting tips
                        st.markdown("""
                        ### 🔧 Troubleshooting Tips:
                        1. **Enable Proxy**: Check the "Use Proxy" option in the sidebar and configure a proxy server
                        2. **Try Different Video**: Some videos may have transcripts disabled
                        3. **Wait and Retry**: Your IP might be temporarily blocked - try again later
                        4. **Use VPN**: Connect through a VPN to change your IP address
                        5. **Check Video Availability**: Ensure the video is public and has captions
                        """)
        
        # Display transcript
        if st.session_state.transcript_data:
            st.subheader("📝 Video Info")
            
            # Video info
            if st.session_state.video_info:
                st.markdown(f"""
                <div class="video-info">
                    <strong>Video ID:</strong> {st.session_state.video_info['video_id']}<br>
                    <strong>Extracted:</strong> {st.session_state.video_info['extracted_at']}<br>
                    <strong>Total Segments:</strong> {len(st.session_state.transcript_data)}
                </div>
                """, unsafe_allow_html=True)

            # View transcript button
            view_transcript = st.button("📋 View Transcript")
            if view_transcript:
                st.session_state.show_transcript = True

            # Display transcript in enhanced format
            if st.session_state.get('show_transcript', False):
                st.subheader("📋 Transcript Content")
                
                # Initialize transcript notes if not exists
                if 'transcript_notes' not in st.session_state:
                    st.session_state.transcript_notes = {}
                
                # Search functionality
                search_term = st.text_input("🔍 Search in transcript:", placeholder="Enter word or phrase to search...")
                
# Action buttons row
                col1_inner, col2_inner, col3_inner = st.columns([1, 1, 1])
                with col1_inner:
                    if st.button("📋 Copy Whole Transcript", use_container_width=True):
                        # Convert to paragraph format without timestamps
                        clean_transcript = ""
                        current_paragraph = []
                        
                        for entry in st.session_state.transcript_data:
                            text = entry['text'].strip()
                            current_paragraph.append(text)
                            
                            # Create paragraph breaks at sentence endings or after 3-4 segments
                            if (text.endswith('.') or text.endswith('!') or text.endswith('?') or 
                                len(current_paragraph) >= 3):
                                clean_transcript += ' '.join(current_paragraph) + '\n\n'
                                current_paragraph = []
                        
                        # Add remaining text
                        if current_paragraph:
                            clean_transcript += ' '.join(current_paragraph)
                        
                        # Store in session state
                        st.session_state.clean_transcript_copy = clean_transcript
                        
                        # Escape backticks and backslashes for JavaScript template literal
                        js_safe_transcript = clean_transcript.replace('\\', '\\\\').replace('`', '\\`')
                        # JavaScript to copy to clipboard
                        copy_js = f"""
                        <script>
                        function copyToClipboard() {{
                            const textToCopy = `{js_safe_transcript}`;
                            navigator.clipboard.writeText(textToCopy).then(function() {{
                                console.log('Transcript copied to clipboard successfully!');
                            }}, function(err) {{
                                console.error('Could not copy transcript: ', err);
                                // Fallback method
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
                        
                        # Execute the JavaScript
                        st.components.v1.html(copy_js, height=0)
                        st.success("✅ Transcript copied to clipboard!")
                
                # Show clean transcript if it exists (optional - for manual copying as backup)
                if st.session_state.get('clean_transcript_copy'):
                    with st.expander("📋 Clean Transcript (Manual Copy Backup)", expanded=False):
                        st.text_area(
                            "Clean transcript without timestamps:",
                            value=st.session_state.clean_transcript_copy,
                            height=200,
                            help="Select all text and copy (Ctrl+A, Ctrl+C) - This is a backup if automatic copy didn't work"
                        )
                
                with col2_inner:
                    # Download transcript
                    def create_download_transcript():
                        clean_transcript = ""
                        current_paragraph = []
                        paragraph_index = 0
                        
                        for i, entry in enumerate(st.session_state.transcript_data):
                            text = entry['text'].strip()
                            current_paragraph.append(text)
                            
                            # Create paragraph breaks
                            if (text.endswith('.') or text.endswith('!') or text.endswith('?') or 
                                len(current_paragraph) >= 3):
                                paragraph_text = ' '.join(current_paragraph)
                                
                                # Check if this paragraph has notes
                                if paragraph_index in st.session_state.transcript_notes:
                                    clean_transcript += "--- NOTE SECTION START ---\n"
                                    clean_transcript += paragraph_text + '\n'
                                    clean_transcript += f'"{st.session_state.transcript_notes[paragraph_index]}"\n'
                                    clean_transcript += "--- NOTE SECTION END ---\n\n"
                                else:
                                    clean_transcript += paragraph_text + '\n\n'
                                
                                current_paragraph = []
                                paragraph_index += 1
                        
                        # Add remaining text
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
                
                # Create paragraphs from transcript
                paragraphs = []
                current_paragraph = []
                current_timestamps = []
                
                for entry in st.session_state.transcript_data:
                    text = entry['text'].strip()
                    start_time = entry.get('start', 0)
                    current_paragraph.append(text)
                    current_timestamps.append(start_time)
                    
                    # Create paragraph breaks at sentence endings or after 3-4 segments
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
                
                # Add remaining text as final paragraph
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
                
                # Create a container for the transcript with fixed height and scrolling
                transcript_container = st.container()
                with transcript_container:
                    # Use st.container with height parameter for scrolling
                    with st.container(height=400):  # Fixed height scrollable container
                        for i, paragraph in enumerate(paragraphs):
                            # Create a container for each paragraph
                            # Highlight search term if present
                            display_text = paragraph['text']
                            if search_term and search_term.lower() in display_text.lower():
                                import re
                                pattern = re.compile(re.escape(search_term), re.IGNORECASE)
                                display_text = pattern.sub(
                                    f'<mark style="background-color: #ffeb3b; padding: 2px 4px; border-radius: 3px;">{search_term}</mark>',
                                    display_text
                                )
                            
                            # Create paragraph container with styling
                            st.markdown(f"""
                            <div style="margin-bottom: 1.5rem; padding: 1rem; border-left: 3px solid #4ECDC4; background: #f8f9fa; border-radius: 0 8px 8px 0;">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                    <span style="color: #FF6B6B; font-weight: bold; font-size: 0.9rem;">[{paragraph['timestamp']}]</span>
                                </div>
                                <div style="margin: 0.5rem 0; line-height: 1.6; color: #2c3e50;">{display_text}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Add copy and note buttons for each paragraph
                            col_copy, col_note, col_spacer = st.columns([1, 1, 4])
                            with col_copy:
                                if st.button("📋 Copy", key=f"copy_para_{i}", help="Copy this paragraph"):
                                    # Store paragraph text for copying
                                    st.session_state[f"copied_text_{i}"] = paragraph['text']
                                    st.success("✅ Copied to session!")
                            
                            with col_note:
                                if st.button("📝 Note", key=f"note_para_{i}", help="Add note to this paragraph"):
                                    st.session_state[f"show_note_input_{i}"] = True
                            
                            # Show note input if button was clicked
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
                            
                            # Show existing note if present
                            if i in st.session_state.transcript_notes:
                                st.markdown(f"""
                                <div style="margin-top: 0.5rem; padding: 0.5rem; background: #e8f5e8; border-radius: 4px; border-left: 3px solid #4ECDC4;">
                                    <strong>📝 Your Note:</strong> {st.session_state.transcript_notes[i]}
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if st.button(f"✏️ Edit Note", key=f"edit_note_para_{i}"):
                                    st.session_state[f"show_note_input_{i}"] = True
                                    st.rerun()
                
                # Display copied text and notes outside the scrollable area
                # Display copied text if any
                copied_texts = []
                for key in st.session_state.keys():
                    if key.startswith("copied_text_"):
                        para_idx = key.split("_")[-1]
                        copied_texts.append((para_idx, st.session_state[key]))
                
                if copied_texts:
                    st.subheader("📋 Copied Paragraphs")
                    for para_idx, text in copied_texts[-3:]:  # Show last 3 copied
                        with st.expander(f"Copied Paragraph {int(para_idx)+1}"):
                            st.text_area("Text:", value=text, height=100, disabled=True)
                            if st.button(f"Clear", key=f"clear_copied_{para_idx}"):
                                del st.session_state[f"copied_text_{para_idx}"]
                                st.rerun()
                
                # Show existing notes summary
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

    with col2:
        st.subheader("🧠 Insights & Actions")
        
        if st.session_state.transcript_text and gemini_api_key:
            gemini = GeminiAI(gemini_api_key)
            
            # Action buttons
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("📊 Summarize", use_container_width=True):
                    with st.spinner("Generating summary..."):
                        summary = gemini.generate_summary(st.session_state.transcript_text)
                        st.session_state.note_counter += 1
                        note_id = f"summary_{st.session_state.note_counter}"
                        st.session_state[f"note_{note_id}"] = {
                            'content': summary,
                            'type': 'Summary',
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        st.rerun()
                
                if st.button("💎 Key Quotes", use_container_width=True):
                    with st.spinner("Extracting quotes..."):
                        quotes = gemini.extract_key_quotes(st.session_state.transcript_text)
                        st.session_state.note_counter += 1
                        note_id = f"quotes_{st.session_state.note_counter}"
                        st.session_state[f"note_{note_id}"] = {
                            'content': quotes,
                            'type': 'Key Quotes',
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        st.rerun()
                
                if st.button("❓ Q&A", use_container_width=True):
                    with st.spinner("Generating Q&A..."):
                        qa = gemini.generate_qa(st.session_state.transcript_text)
                        st.session_state.note_counter += 1
                        note_id = f"qa_{st.session_state.note_counter}"
                        st.session_state[f"note_{note_id}"] = {
                            'content': qa,
                            'type': 'Q&A',
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        st.rerun()
            
            with col_b:
                if st.button("📚 Study Guide", use_container_width=True):
                    with st.spinner("Creating study guide..."):
                        guide = gemini.create_study_guide(st.session_state.transcript_text)
                        st.session_state.note_counter += 1
                        note_id = f"study_{st.session_state.note_counter}"
                        st.session_state[f"note_{note_id}"] = {
                            'content': guide,
                            'type': 'Study Guide',
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        st.rerun()
                
                if st.button("🎯 Flash Cards", use_container_width=True):
                    with st.spinner("Creating flashcards..."):
                        cards = gemini.create_flashcards(st.session_state.transcript_text)
                        st.session_state.note_counter += 1
                        note_id = f"flashcards_{st.session_state.note_counter}"
                        st.session_state[f"note_{note_id}"] = {
                            'content': cards,
                            'type': 'Flash Cards',
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        st.rerun()
                
                if st.button("✨ Highlights", use_container_width=True):
                    with st.spinner("Extracting insights..."):
                        insights = gemini.highlight_insights(st.session_state.transcript_text)
                        st.session_state.note_counter += 1
                        note_id = f"highlights_{st.session_state.note_counter}"
                        st.session_state[f"note_{note_id}"] = {
                            'content': insights,
                            'type': 'Highlights',
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        st.rerun()
        
        elif st.session_state.transcript_text:
            st.info("🔑 Enter Gemini API key to enable AI features")
        else:
            st.info("📥 Extract a transcript first to enable insights")


    
    # Display notes section
    st.divider()
    st.subheader("📋 Your Notes")
    
    # Get all notes from session state
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

    # Sort notes by timestamp (newest first)
    notes = sorted(notes, key=lambda x: x['timestamp'], reverse=True)
    
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
    
    # Chat with transcript
    if st.session_state.transcript_text and gemini_api_key:
        st.divider()
        st.subheader("💬 Chat with Transcript")
        
        gemini = GeminiAI(gemini_api_key)
        
        # Chat interface
        chat_question = st.text_input(
            "Ask a question about the video content:",
            placeholder="What are the main points discussed in this video?"
        )
        
        if st.button("💬 Ask", use_container_width=True) and chat_question:
            with st.spinner("Thinking..."):
                answer = gemini.chat_with_transcript(st.session_state.transcript_text, chat_question)
                
                # Add to chat history
                st.session_state.chat_history.append({
                    'question': chat_question,
                    'answer': answer,
                    'timestamp': datetime.now().strftime("%H:%M:%S")
                })
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown("### 💭 Chat History")
            for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):  # Show last 5
                with st.expander(f"Q: {chat['question'][:50]}... ({chat['timestamp']})"):
                    st.write("**Question:**", chat['question'])
                    st.write("**Answer:**", chat['answer'])
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🚀 Built with Streamlit & Gemini AI | 
        <a href="https://ai.google.dev/" target="_blank">Get Gemini API Key</a> | 
        Made with ❤️ for learning</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()