# Usage Guide - YouTube Transcript GPT

A comprehensive guide on how to use YouTube Transcript GPT to extract, analyze, and interact with YouTube video transcripts using AI-powered insights.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Features Overview](#features-overview)
- [Step-by-Step Usage](#step-by-step-usage)
- [AI-Powered Features](#ai-powered-features)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)
- [Tips and Best Practices](#tips-and-best-practices)
- [API Configuration](#api-configuration)
- [Proxy Configuration](#proxy-configuration)

## Overview

YouTube Transcript GPT is a powerful Streamlit application that allows you to:

- **Extract transcripts** from YouTube videos automatically
- **Generate AI-powered insights** including summaries, key quotes, study guides, Q&A sessions, and flashcards
- **Interactive chat** with video content using Google's Gemini AI
- **Note-taking system** with timestamps and searchable content
- **Export functionality** for all generated content
- **Proxy support** for bypassing regional restrictions

## Quick Start

### Method 1: Run Locally

```bash
# Clone the repository
git clone https://github.com/nova-cortex/yt-transcript-gpt.git
cd yt-transcript-gpt

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run src/main.py
```

### Method 2: Using Python Module

```bash
# After installation, run as a module
python src/main.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Installation

### Prerequisites

- Python 3.8 or higher
- Internet connection for API calls
- Google Gemini API key (free tier available)

### Required Dependencies

```bash
pip install streamlit
pip install youtube-transcript-api
pip install yt-dlp
pip install google-generativeai
```

Or install all at once:

```bash
pip install -r requirements.txt
```

### Verify Installation

After installation, check that all required libraries are available:

1. Start the application
2. Check the sidebar "📚 Available Libraries" section
3. Both "YouTube Transcript API" and "yt-dlp" should show ✅

## Configuration

### 1. Gemini API Key Setup

1. **Get your API key**:
   - Visit [Google AI Studio](https://ai.google.dev/)
   - Create an account or sign in
   - Generate a new API key (free tier available)

2. **Configure in the app**:
   - Open the application
   - In the sidebar, paste your API key in the "Gemini API Key" field
   - Look for the ✅ confirmation message

### 2. Proxy Configuration (Optional)

If you encounter IP blocking or regional restrictions:

1. **Enable proxy** in the sidebar
2. **Configure proxy settings**:
   - Proxy Type: HTTP, HTTPS, or SOCKS5
   - Proxy Host: Your proxy server address
   - Proxy Port: Port number
   - Username/Password: If required by your proxy

## Features Overview

### Core Features

| Feature | Description | Requirements |
|---------|-------------|--------------|
| 🎬 **Transcript Extraction** | Extract transcripts from any YouTube video | None |
| 📊 **AI Summaries** | Generate comprehensive video summaries | Gemini API |
| 💎 **Key Quotes** | Extract impactful quotes with timestamps | Gemini API |
| 📚 **Study Guides** | Create structured learning materials | Gemini API |
| ❓ **Q&A Generation** | Generate questions and answers | Gemini API |
| 🎯 **Flashcards** | Create memorization cards | Gemini API |
| ✨ **Highlights** | Extract key insights and revelations | Gemini API |
| 💬 **Chat Interface** | Ask questions about video content | Gemini API |
| 📝 **Note Taking** | Add personal notes to transcript segments | None |
| 🔍 **Search** | Search within transcript content | None |
| 📥 **Export** | Download transcripts and AI-generated content | None |

## Step-by-Step Usage

### 1. Extract a Transcript

1. **Launch the application** using `streamlit run src/main.py`
2. **Paste YouTube URL** in the "YouTube Video URL" field
   ```
   Examples:
   https://www.youtube.com/watch?v=VIDEO_ID
   https://youtu.be/VIDEO_ID
   https://youtube.com/watch?v=VIDEO_ID&t=120s
   ```
3. **Click "🚀 Extract Transcript"**
4. **Wait for processing** - you'll see a spinner and then a success message

### 2. View and Interact with Transcript

1. **Click "📋 View Transcript"** to expand the transcript viewer
2. **Search functionality**: Use the search box to find specific terms
3. **Paragraph-based display**: Content is organized into readable paragraphs
4. **Timestamp navigation**: Each paragraph shows its video timestamp

### 3. Copy and Download Content

#### Copy Individual Paragraphs
- Click "📋 Copy" next to any paragraph
- Content is copied to your session for easy access

#### Copy Entire Transcript
- Click "📋 Copy Whole Transcript" 
- Clean, formatted transcript is copied to clipboard

#### Download Transcript
- Click "📥 Download Transcript"
- Includes your notes if any have been added
- Saved as a timestamped .txt file

### 4. Add Personal Notes

1. **Click "📝 Note"** next to any paragraph
2. **Type your note** in the text area
3. **Click "💾 Save Note"** to save
4. **View notes summary** at the bottom of the transcript section

## AI-Powered Features

### Prerequisites
- Gemini API key configured in sidebar
- Extracted transcript available

### Available AI Features

#### 📊 Summarize
- **Purpose**: Generate comprehensive video summaries
- **Content**: Main topics, key points, important conclusions
- **Use case**: Quick understanding of long videos

#### 💎 Key Quotes
- **Purpose**: Extract 5-10 most impactful quotes
- **Format**: "Quote text" - [Timestamp]
- **Use case**: Social media sharing, presentations

#### 📚 Study Guide
- **Purpose**: Create structured learning materials
- **Content**: Main topics, key concepts, definitions, study questions
- **Use case**: Academic learning, skill development

#### ❓ Q&A
- **Purpose**: Generate comprehensive question-answer pairs
- **Content**: 10-15 questions with detailed answers
- **Use case**: Self-testing, interview preparation

#### 🎯 Flash Cards
- **Purpose**: Create memorization cards
- **Format**: FRONT: Question/Term, BACK: Answer/Definition
- **Content**: 15-20 flashcards per video
- **Use case**: Vocabulary building, concept memorization

#### ✨ Highlights
- **Purpose**: Extract key insights and actionable takeaways
- **Content**: Key insights, revelations, data/statistics, actionable items
- **Format**: Organized with emojis and clear formatting
- **Use case**: Business insights, personal development

### Using AI Features

1. **Ensure API key is configured** (✅ in sidebar)
2. **Extract a transcript first**
3. **Click any AI feature button** in the right column
4. **Wait for processing** (usually 10-30 seconds)
5. **View generated content** in the "Your Notes" section
6. **Download or copy** the generated content

## Advanced Features

### Interactive Chat

1. **Navigate to "💬 Chat with Transcript" section**
2. **Type your question** about the video content
   ```
   Example questions:
   - "What are the main arguments presented?"
   - "Can you explain the technical concepts mentioned?"
   - "What actionable advice is given?"
   ```
3. **Click "💬 Ask"** to get AI-powered answers
4. **View chat history** for previous Q&A sessions

### Search and Navigation

#### Transcript Search
- **Use the search box** in the transcript section
- **Terms are highlighted** in yellow for easy identification
- **Case-insensitive** search functionality

#### Note Management
- **View all notes** in the "📋 Your Notes" section
- **Expand/collapse** individual notes
- **Delete notes** using the 🗑️ button
- **Download individual notes** as markdown files

### Content Export Options

#### Individual Content Export
- Each AI-generated content has a "📥 Download" button
- Files are saved as markdown (.md) format
- Filenames include content type and timestamp

#### Bulk Export
- Transcript with notes can be downloaded as single file
- Notes are clearly marked in the exported content
- Preserves formatting and structure

## Troubleshooting

### Common Issues and Solutions

#### ❌ "Invalid YouTube URL"
**Cause**: URL format not recognized
**Solution**: 
- Use full YouTube URLs: `https://www.youtube.com/watch?v=VIDEO_ID`
- Avoid shortened URLs or URLs with extra parameters

#### ❌ "Both transcript extraction methods failed"
**Possible causes**: IP blocking, no captions available, private video
**Solutions**:
1. **Enable proxy** in sidebar settings
2. **Try different video** - some videos don't have captions
3. **Check video availability** - ensure video is public
4. **Wait and retry** - temporary IP restrictions
5. **Use VPN** to change your IP address

#### ❌ "YouTube Transcript API failed"
**Solutions**:
1. **Enable proxy configuration**:
   - Check "Use Proxy" in sidebar
   - Configure proxy server details
   - Test with different proxy servers

2. **Verify video has captions**:
   - Manual captions work best
   - Auto-generated captions are also supported
   - Some videos may not have any captions

#### ⚠️ AI Features Not Working
**Check these items**:
- ✅ Gemini API key is entered in sidebar
- ✅ Transcript has been extracted successfully
- ✅ Internet connection is stable
- ✅ API key has remaining quota

#### 🐌 Slow Performance
**Optimization tips**:
- Process shorter videos first
- Close unnecessary browser tabs
- Ensure stable internet connection
- Use latest version of Streamlit

### Error Messages Guide

| Error Message | Meaning | Solution |
|---------------|---------|----------|
| "Your IP has been blocked" | YouTube has temporarily blocked your IP | Enable proxy or use VPN |
| "Error generating summary" | Gemini API call failed | Check API key and internet connection |
| "No subtitles available" | Video doesn't have captions | Try a different video |
| "Invalid video ID" | Could not extract video ID from URL | Check URL format |

## Tips and Best Practices

### Optimal Video Selection
- **Educational content** works best for AI features
- **Videos with manual captions** provide better accuracy
- **English content** produces best AI results
- **10-60 minute videos** are ideal for processing time

### Maximizing AI Features
- **Be specific with chat questions** for better answers
- **Use study guides for learning** complex topics
- **Export flashcards to external apps** like Anki
- **Combine multiple AI features** for comprehensive analysis

### Note-Taking Strategy
- **Add notes during transcript review** for context
- **Use consistent formatting** in your notes
- **Export regularly** to avoid losing work
- **Organize notes by topic** using clear descriptions

### Performance Optimization
- **Process videos sequentially** rather than in parallel
- **Clear chat history** periodically to free memory
- **Download content regularly** and clear notes
- **Use shorter videos** for testing new features

## API Configuration

### Gemini API Setup

1. **Visit Google AI Studio**: https://ai.google.dev/
2. **Create account** or sign in with Google
3. **Generate API key**:
   - Click "Get API key"
   - Create new project or use existing
   - Copy the generated key
4. **Configure in app**:
   - Paste key in sidebar "Gemini API Key" field
   - Confirm ✅ "Gemini API configured" message

### API Usage Limits

- **Free tier**: Generous limits for personal use
- **Rate limits**: Built-in handling for API rate limits
- **Quota monitoring**: Check usage in Google AI Studio
- **Error handling**: Automatic retry for temporary failures

## Proxy Configuration

### When to Use Proxy

- 🚫 IP blocked by YouTube
- 🌍 Regional content restrictions
- 🏢 Corporate firewall blocking YouTube
- 📡 Network-level restrictions

### Proxy Setup Steps

1. **Obtain proxy server details**:
   - Host address (e.g., proxy.example.com)
   - Port number (e.g., 8080)
   - Authentication credentials (if required)

2. **Configure in application**:
   - Check "Use Proxy" in sidebar
   - Select proxy type (HTTP/HTTPS/SOCKS5)
   - Enter host and port
   - Add credentials if required

3. **Test configuration**:
   - Try extracting a transcript
   - Look for "Success using [method] (with proxy)" message

### Proxy Providers

**Free options**:
- Public proxy lists (reliability varies)
- Browser-based proxies

**Paid options** (recommended):
- Commercial proxy services
- VPN services with proxy support
- Cloud-based proxy solutions

---

### 📞 Support

- **📧 Email**: [ujjwalkrai@gmail.com](mailto:ujjwalkrai@gmail.com)
- **🐛 Issues**: [Repository Issues](https://github.com/nova-cortex/yt-transcript-gpt/issues)
- **🔓 Security**: [Repository Security](https://github.com/nova-cortex/yt-transcript-gpt/security)
- **⛏ Pull Requests**: [Repository Pull Requests](https://github.com/nova-cortex/yt-transcript-gpt/pulls)
- **📖 Documentation**: [Repository Documentation](https://github.com/nova-cortex/yt-transcript-gpt/tree/main/docs)

## Contributing

Want to improve YouTube Transcript GPT? Check out our [Contributing Guidelines](CONTRIBUTING.md) to get started!

---

**Made with ❤️ for learners and content creators**

*Transform any YouTube video into a comprehensive learning resource with AI-powered insights and interactive features.*