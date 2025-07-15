"""
Transcript Extractor Module.

This module provides the `YouTubeTranscriptExtractor` class, which is responsible
for extracting video transcripts from YouTube using the youtube-transcript-api
with a fallback to yt-dlp. It includes functionality for video ID extraction,
proxy support, and handling of different transcript sources.
"""

import streamlit as st
import re
from datetime import datetime

# Check for the availability of the youtube_transcript_api library
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    TRANSCRIPT_API_AVAILABLE = True
except ImportError:
    TRANSCRIPT_API_AVAILABLE = False

# Check for the availability of the yt-dlp library
try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False

class YouTubeTranscriptExtractor:
    """
    A class to extract YouTube video transcripts.
    
    This class handles the extraction of transcripts using different methods,
    manages video information, and supports the use of proxies.
    """
    def __init__(self):
        """
        Initializes the YouTubeTranscriptExtractor with empty transcript data and video info.
        """
        self.transcript_data = None
        self.video_info = None
        
    def extract_video_id(self, url):
        """
        Extracts the video ID from a given YouTube URL.
        
        Args:
            url (str): The URL of the YouTube video.
            
        Returns:
            str: The extracted video ID, or None if not found.
        """
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
        """
        Retrieves a transcript using the YouTube Transcript API with proxy support.
        
        Args:
            video_id (str): The ID of the YouTube video.
            proxies (dict, optional): A dictionary of proxy settings. Defaults to None.
            
        Returns:
            list: A list of transcript segments, or None on failure.
        """
        try:
            if proxies:
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
        """
        Retrieves a transcript using the YouTube Transcript API, with an option for a proxy.
        
        Args:
            video_id (str): The ID of the YouTube video.
            use_proxy (bool, optional): Whether to use a proxy. Defaults to False.
            proxy_config (str, optional): The proxy configuration string. Defaults to None.
            
        Returns:
            list: A list of transcript segments, or None on failure.
        """
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
        """
        Retrieves a transcript using yt-dlp as a fallback, with proxy support.
        
        Args:
            video_id (str): The ID of the YouTube video.
            use_proxy (bool, optional): Whether to use a proxy. Defaults to False.
            proxy_config (str, optional): The proxy configuration string. Defaults to None.
            
        Returns:
            list: A list of transcript segments, or None on failure.
        """
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
                
                subtitles = info.get('subtitles', {})
                auto_captions = info.get('automatic_captions', {})
                
                # Prioritize English subtitles, then any other available language
                for lang in ['en', 'en-US', 'en-GB']:
                    if lang in subtitles:
                        return self._process_ytdlp_subtitles(subtitles[lang])
                    if lang in auto_captions:
                        return self._process_ytdlp_subtitles(auto_captions[lang])
                
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
        """
        Processes the subtitle list obtained from yt-dlp.
        
        Note: This is a placeholder and needs to be implemented to parse the actual
              subtitle file format provided by yt-dlp.
              
        Args:
            subtitle_list (list): The list of subtitles from yt-dlp.
            
        Returns:
            list: A simplified list of transcript segments.
        """
        return [{"text": "Subtitle available via yt-dlp (implementation needed)", "start": 0, "duration": 1}]
    
    def extract_transcript(self, video_url, use_proxy=False, proxy_config=None):
        """
        Main method to extract a transcript, trying the API first and falling back to yt-dlp.
        
        Args:
            video_url (str): The URL of the YouTube video.
            use_proxy (bool, optional): Whether to use a proxy. Defaults to False.
            proxy_config (str, optional): The proxy configuration string. Defaults to None.
            
        Returns:
            tuple: A tuple containing the transcript (list) and a status message (str).
        """
        video_id = self.extract_video_id(video_url)
        if not video_id:
            return None, "Invalid YouTube URL"
        
        # Store video information
        self.video_info = {
            'video_id': video_id,
            'url': video_url,
            'extracted_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Attempt to get transcript using the YouTube Transcript API
        if TRANSCRIPT_API_AVAILABLE:
            transcript = self.get_transcript_youtube_api(video_id, use_proxy, proxy_config)
            if transcript:
                self.transcript_data = transcript
                proxy_status = " (with proxy)" if use_proxy else ""
                return transcript, f"Success using YouTube Transcript API{proxy_status}"
        
        # Fallback to yt-dlp if the API fails or is unavailable
        if YT_DLP_AVAILABLE:
            transcript = self.get_transcript_ytdlp(video_id, use_proxy, proxy_config)
            if transcript:
                self.transcript_data = transcript
                proxy_status = " (with proxy)" if use_proxy else ""
                return transcript, f"Success using yt-dlp{proxy_status}"
        
        return None, "Both transcript extraction methods failed"
