"""
This module provides the `YouTubeTranscriptExtractor` class, which is responsible
for extracting video transcripts from YouTube using the youtube-transcript-api
with a fallback to yt-dlp. It includes functionality for video ID extraction,
proxy support, and handling of different transcript sources.
"""

import streamlit as st
import re
import json
import tempfile
import os
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
            r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
            r"(?:embed\/)([0-9A-Za-z_-]{11})",
            r"(?:watch\?v=)([0-9A-Za-z_-]{11})",
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
                    video_id, proxies=proxies
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
                proxies = {"http": proxy_config, "https": proxy_config}
                transcript_list = self.get_transcript_with_proxy(video_id, proxies)
            else:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            return transcript_list
        except Exception as e:
            error_message = str(e)
            if "blocked" in error_message.lower() or "ip" in error_message.lower():
                st.error(
                    "🚫 Your IP has been blocked by YouTube. Try using a proxy or VPN."
                )
            else:
                st.error(f"YouTube Transcript API failed: {error_message}")
            return None

    def _parse_vtt_content(self, vtt_content):
        """
        Parses VTT (WebVTT) subtitle content and converts it to transcript format.

        Args:
            vtt_content (str): The raw VTT content as a string.

        Returns:
            list: A list of transcript segments with text, start time, and duration.
        """
        transcript = []
        lines = vtt_content.split("\n")

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Skip empty lines and WEBVTT headers
            if (
                not line
                or line.startswith("WEBVTT")
                or line.startswith("Kind:")
                or line.startswith("Language:")
            ):
                i += 1
                continue

            # Look for timestamp lines (format: 00:00:00.000 --> 00:00:00.000)
            if "-->" in line:
                try:
                    # Parse timestamp
                    timestamp_parts = line.split(" --> ")
                    if len(timestamp_parts) == 2:
                        start_time = self._parse_timestamp(timestamp_parts[0])
                        end_time = self._parse_timestamp(timestamp_parts[1])
                        duration = end_time - start_time

                        # Get the text content (next non-empty lines)
                        text_lines = []
                        i += 1
                        while i < len(lines) and lines[i].strip():
                            text_line = lines[i].strip()
                            # Remove HTML tags and formatting
                            text_line = re.sub(r"<[^>]+>", "", text_line)
                            if text_line:
                                text_lines.append(text_line)
                            i += 1

                        if text_lines:
                            text = " ".join(text_lines)
                            transcript.append(
                                {
                                    "text": text,
                                    "start": start_time,
                                    "duration": duration,
                                }
                            )
                except Exception as e:
                    # Skip malformed timestamp lines
                    pass

            i += 1

        return transcript

    def _parse_srt_content(self, srt_content):
        """
        Parses SRT subtitle content and converts it to transcript format.

        Args:
            srt_content (str): The raw SRT content as a string.

        Returns:
            list: A list of transcript segments with text, start time, and duration.
        """
        transcript = []
        blocks = srt_content.strip().split("\n\n")

        for block in blocks:
            lines = block.strip().split("\n")
            if len(lines) >= 3:
                try:
                    # Skip sequence number (first line)
                    # Parse timestamp (second line)
                    timestamp_line = lines[1]
                    if "-->" in timestamp_line:
                        timestamp_parts = timestamp_line.split(" --> ")
                        if len(timestamp_parts) == 2:
                            start_time = self._parse_srt_timestamp(timestamp_parts[0])
                            end_time = self._parse_srt_timestamp(timestamp_parts[1])
                            duration = end_time - start_time

                            # Get text content (remaining lines)
                            text_lines = lines[2:]
                            text = " ".join(
                                line.strip() for line in text_lines if line.strip()
                            )
                            # Remove HTML tags
                            text = re.sub(r"<[^>]+>", "", text)

                            if text:
                                transcript.append(
                                    {
                                        "text": text,
                                        "start": start_time,
                                        "duration": duration,
                                    }
                                )
                except Exception as e:
                    # Skip malformed blocks
                    continue

        return transcript

    def _parse_timestamp(self, timestamp_str):
        """
        Parses a VTT timestamp string (HH:MM:SS.mmm) to seconds.

        Args:
            timestamp_str (str): The timestamp string to parse.

        Returns:
            float: The timestamp in seconds.
        """
        try:
            # Remove any extra whitespace
            timestamp_str = timestamp_str.strip()

            # Handle different timestamp formats
            if "." in timestamp_str:
                time_part, ms_part = timestamp_str.rsplit(".", 1)
                milliseconds = float("0." + ms_part)
            else:
                time_part = timestamp_str
                milliseconds = 0.0

            # Parse HH:MM:SS
            time_components = time_part.split(":")
            if len(time_components) == 3:
                hours, minutes, seconds = map(int, time_components)
                total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds
                return total_seconds
            elif len(time_components) == 2:
                minutes, seconds = map(int, time_components)
                total_seconds = minutes * 60 + seconds + milliseconds
                return total_seconds
        except Exception:
            return 0.0

        return 0.0

    def _parse_srt_timestamp(self, timestamp_str):
        """
        Parses an SRT timestamp string (HH:MM:SS,mmm) to seconds.

        Args:
            timestamp_str (str): The timestamp string to parse.

        Returns:
            float: The timestamp in seconds.
        """
        try:
            timestamp_str = timestamp_str.strip()

            # SRT uses comma for milliseconds
            if "," in timestamp_str:
                time_part, ms_part = timestamp_str.rsplit(",", 1)
                milliseconds = float("0." + ms_part)
            else:
                time_part = timestamp_str
                milliseconds = 0.0

            # Parse HH:MM:SS
            time_components = time_part.split(":")
            if len(time_components) == 3:
                hours, minutes, seconds = map(int, time_components)
                total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds
                return total_seconds
        except Exception:
            return 0.0

        return 0.0

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

            # Create a temporary directory for subtitle files
            with tempfile.TemporaryDirectory() as temp_dir:
                ydl_opts = {
                    "writesubtitles": True,
                    "writeautomaticsub": True,
                    "skip_download": True,
                    "quiet": True,
                    "no_warnings": True,
                    "subtitleslangs": ["en", "en-US", "en-GB"],
                    "subtitlesformat": "vtt/srt/best",
                    "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
                }

                if use_proxy and proxy_config:
                    ydl_opts["proxy"] = proxy_config

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Extract info without downloading video
                    info = ydl.extract_info(url, download=False)

                    # Store video info
                    self.video_info = {
                        "video_id": video_id,
                        "url": url,
                        "title": info.get("title", "Unknown Title"),
                        "duration": info.get("duration", 0),
                        "extracted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }

                    # Try to download subtitles
                    ydl.download([url])

                    # Look for subtitle files in the temp directory
                    subtitle_files = []
                    for file in os.listdir(temp_dir):
                        if file.endswith((".vtt", ".srt")):
                            subtitle_files.append(os.path.join(temp_dir, file))

                    # Process the first available subtitle file
                    for subtitle_file in subtitle_files:
                        try:
                            with open(subtitle_file, "r", encoding="utf-8") as f:
                                content = f.read()

                            if subtitle_file.endswith(".vtt"):
                                transcript = self._parse_vtt_content(content)
                            elif subtitle_file.endswith(".srt"):
                                transcript = self._parse_srt_content(content)
                            else:
                                continue

                            if transcript:
                                return transcript

                        except Exception as e:
                            st.warning(
                                f"Failed to process subtitle file {subtitle_file}: {str(e)}"
                            )
                            continue

                    # If no subtitle files were found, try to get them from the info dict
                    subtitles = info.get("subtitles", {})
                    auto_captions = info.get("automatic_captions", {})

                    # Try to find English subtitles
                    for lang in ["en", "en-US", "en-GB"]:
                        if lang in subtitles:
                            return self._download_and_parse_subtitle(
                                subtitles[lang], use_proxy, proxy_config
                            )
                        if lang in auto_captions:
                            return self._download_and_parse_subtitle(
                                auto_captions[lang], use_proxy, proxy_config
                            )

                    # Try any available language
                    if subtitles:
                        first_lang = list(subtitles.keys())[0]
                        return self._download_and_parse_subtitle(
                            subtitles[first_lang], use_proxy, proxy_config
                        )
                    if auto_captions:
                        first_lang = list(auto_captions.keys())[0]
                        return self._download_and_parse_subtitle(
                            auto_captions[first_lang], use_proxy, proxy_config
                        )

            return None

        except Exception as e:
            st.error(f"yt-dlp failed: {str(e)}")
            return None

    def _download_and_parse_subtitle(
        self, subtitle_formats, use_proxy=False, proxy_config=None
    ):
        """
        Downloads and parses subtitle content from yt-dlp subtitle format info.

        Args:
            subtitle_formats (list): List of subtitle format dictionaries from yt-dlp.
            use_proxy (bool, optional): Whether to use a proxy. Defaults to False.
            proxy_config (str, optional): The proxy configuration string. Defaults to None.

        Returns:
            list: A list of transcript segments, or None on failure.
        """
        import urllib.request
        import urllib.error

        # Try different formats in order of preference
        preferred_formats = ["vtt", "srv3", "srv2", "srv1", "srt"]

        for format_pref in preferred_formats:
            for subtitle_format in subtitle_formats:
                if subtitle_format.get("ext") == format_pref:
                    try:
                        subtitle_url = subtitle_format.get("url")
                        if not subtitle_url:
                            continue

                        # Set up request with proxy if needed
                        if use_proxy and proxy_config:
                            proxy_handler = urllib.request.ProxyHandler(
                                {"http": proxy_config, "https": proxy_config}
                            )
                            opener = urllib.request.build_opener(proxy_handler)
                            urllib.request.install_opener(opener)

                        # Download subtitle content
                        with urllib.request.urlopen(
                            subtitle_url, timeout=30
                        ) as response:
                            content = response.read().decode("utf-8")

                        # Parse based on format
                        if format_pref in ["vtt", "srv3", "srv2", "srv1"]:
                            transcript = self._parse_vtt_content(content)
                        elif format_pref == "srt":
                            transcript = self._parse_srt_content(content)
                        else:
                            continue

                        if transcript:
                            return transcript

                    except Exception as e:
                        st.warning(
                            f"Failed to download subtitle format {format_pref}: {str(e)}"
                        )
                        continue

        return None

    def _process_ytdlp_subtitles(self, subtitle_list):
        """
        Legacy method - now replaced by proper subtitle parsing methods.
        Kept for backward compatibility.

        Args:
            subtitle_list (list): The list of subtitles from yt-dlp.

        Returns:
            list: A simplified list of transcript segments.
        """
        # This method is now deprecated and replaced by proper parsing
        return self._download_and_parse_subtitle(subtitle_list)

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

        # Store basic video information
        self.video_info = {
            "video_id": video_id,
            "url": video_url,
            "extracted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        # Attempt to get transcript using the YouTube Transcript API
        if TRANSCRIPT_API_AVAILABLE:
            transcript = self.get_transcript_youtube_api(
                video_id, use_proxy, proxy_config
            )
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
