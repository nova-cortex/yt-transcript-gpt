"""
yt-transcript-gpt - Professional YouTube Transcript Extractor
==============================================

yt-transcript-gpt with AI Analysis and Chat Interface
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

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import main

if __name__ == "__main__":
    main()
