# 🎬 yt-transcript-gpt

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen.svg)](STATUS.md)
[![Version: 1.0.0](https://img.shields.io/badge/Version-1.0.0-red.svg)](CHANGELOG.md)
![Language: Python](https://img.shields.io/badge/Language-Python-blue)

<div align="center">
  <img src="../assets/yt-transcript-gpt-banner.jpg" alt="Project Banner" width="100%">
</div>

<div align="center">
  <img src="https://readme-typing-svg.demolab.com/?lines=Streamlit+based+AI+transcript+extractor&font=Fira%20Code&pause=1000&color=F75C7E&center=true&vCenter=true&width=600&height=30&cursor=true">
</div>

---

## 🖼 Screenshot

<div align="center">
  <img src="../assets/screenshots/screenshot.png" alt="Web UI" />
  <p><em>Web UI</em></p>
</div>


---

## ✨ What’s New in v1.0.0

- 🎉 **Initial release** with core transcript extraction and AI modules  
- 🚀 Integrated both YouTube Transcript API and `yt-dlp` fallback  
- 🤖 Gemini AI features: summaries, key quotes, Q&A, study guides, flashcards, insights  
- 🔍 Interactive transcript viewer with search, copy, and notes  
- 💬 Chat interface to ask questions about the transcript  

---

## 🛠️ All Features

- **Transcript Extraction** via YouTube Transcript API or `yt-dlp`  
- **AI Analysis** through Google Gemini:  
  - Summaries  
  - Key Quotes  
  - Q&A sessions  
  - Study Guides  
  - Flashcards  
  - Highlighted Insights  
- **Interactive Viewer**: search, scrollable transcript, per-paragraph copy & notes  
- **Downloadable Content**: transcripts and AI-generated outputs (Markdown/plain text)  
- **Chat Mode**: ask questions about video content and get AI answers  
- **Configurable**: enable/disable libraries, set Gemini API key  

---

## 🗂️ Folder Structure

```
yt-transcript-gpt/
├── .devcontainer/
│   └── devcontainer.json
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── RELEASE_TEMPLATE.md
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── assets/
│   ├── screenshots/
│   │   └── screenshot.png
│   └── yt-transcript-gpt-banner.jpg
├── docs/
│   ├── CHANGELOG.md
│   ├── CODE_OF_CONDUCT.md
│   ├── CONTRIBUTING.md
│   ├── README.md
│   ├── SECURITY.md
│   ├── STATUS.md
│   └── USAGE.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── src/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── gemini_ai.py
│   │   ├── main.py
│   │   ├── transcript_extractor.py
│   │   ├── ui.py
│   │   └── utils.py
│   └── main.py
└── tests/
    ├── test_gemini_ai.py
    └── test_transcript_extractor.py

```

---

## 🕹 Usage

### Prerequisites

- GitHub

### Installation

```bash
# Clone the repository
git clone https://github.com/nova-cortex/yt-transcript-gpt.git
```

For more detailed documentation, see our [USAGE.md](USAGE.md)

---

## 🤝 Contributing

Please see our [Contributing Guide](CONTRIBUTING.md) for details.

---

### Code of Conduct

This project follows our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

---

## 📋 Roadmap

- [x] Chat interface
- [x] Gemini AI features
- [x] Integrated both YouTube Transcript API and `yt-dlp` fallback

See the [open issues](https://github.com/nova-cortex/yt-transcript-gpt/issues) for a full list of proposed features and known issues.

---

## 📝 Changelog

All notable changes to this project are documented in [CHANGELOG.md](CHANGELOG.md).

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

## 🙏 Acknowledgments

* **Streamlit** for rapid GUI development
* **YouTube Transcript API** & **yt-dlp** for transcript extraction
* **Google Gemini AI** (`google-generativeai`) for advanced analysis

---

## 📞 Support

- 📧 Email: ujjwalkrai@gmail.com
- 🐛 Issues: [Repo Issues](https://github.com/nova-cortex/yt-transcript-gpt/issues)
- 🔓 Security: [Repo Security](https://github.com/nova-cortex/yt-transcript-gpt/security)
- ⛏ Pull Request: [Repo Pull Request](https://github.com/nova-cortex/yt-transcript-gpt/pulls)
- 📖 Docs: [Repo Documentation](https://github.com/nova-cortex/yt-transcript-gpt/tree/main/docs)
- 📃 Changelog: [Repo Changelog](https://github.com/nova-cortex/yt-transcript-gpt/docs/CHANGELOG.md)
---

## 🔗 Connect

#### 📝 Writing & Blogging
[![Hashnode](https://img.shields.io/badge/Hashnode-2962FF?style=for-the-badge&logo=hashnode&logoColor=white)](https://ukr-projects.hashnode.dev/)
[![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/@ukrpurojekuto)

#### 💼 Professional
[![Website](https://img.shields.io/badge/Website-000000?style=for-the-badge&logo=About.me&logoColor=white)](https://ukr-projects.github.io/ukr-projects/)
[![ukr-projects](https://img.shields.io/badge/main-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ukr-projects)
[![cyberx-projects](https://img.shields.io/badge/cybersecurity-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/cyberx-projects)
[![contro-projects](https://img.shields.io/badge/frontend-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/contro-projects)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/u-k-r/ )
[![Main Channel](https://img.shields.io/badge/main-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@ujjwal-krai)

#### 🌐 Social
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://x.com/ukr_projects)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/ukr_projects)
[![Tech Channel](https://img.shields.io/badge/tech-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@ukr-projects)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/ukr_projects)
[![Reddit](https://img.shields.io/badge/Reddit-FF4500?style=for-the-badge&logo=reddit&logoColor=white)](https://www.reddit.com/user/mrujjwalkr)

---

<div align="center">
  Made with ❤️ by <a href="https://github.com/ukr-projects">ukr</a>
</div>

---
