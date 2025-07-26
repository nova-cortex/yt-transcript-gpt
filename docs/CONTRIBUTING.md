# Contributing to YouTube Transcript GPT

Thank you for your interest in contributing to YouTube Transcript GPT! We welcome contributions from everyone and appreciate your help in making this AI-powered transcript analysis tool better for learners, educators, and content creators worldwide.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following:
- **Python 3.8+** installed on your system
- **Git** installed and configured
- **GitHub account** for contributing
- **Basic knowledge** of Python, Streamlit, and AI/ML concepts
- **Google Gemini API key** for testing AI features (free tier available)

### Project Overview

YouTube Transcript GPT is a Streamlit application that:
- Extracts transcripts from YouTube videos using multiple methods
- Generates AI-powered insights using Google's Gemini AI
- Provides interactive features for learning and content analysis
- Supports note-taking, search, and export functionality

### First Time Setup

1. **Fork the repository** on GitHub
2. **Clone your fork locally**:
   ```bash
   git clone https://github.com/your-username/yt-transcript-gpt.git
   cd yt-transcript-gpt
   ```
3. **Add the upstream repository**:
   ```bash
   git remote add upstream https://github.com/nova-cortex/yt-transcript-gpt.git
   ```
4. **Set up the development environment**:
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```
5. **Review the project structure**:
```
yt-transcript-gpt/
├── src/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # Main Streamlit application
│   │   ├── transcript_extractor.py  # YouTube transcript extraction
│   │   ├── gemini_ai.py         # Gemini AI integration
│   │   ├── ui.py               # User interface components
│   │   └── utils.py            # Utility functions
│   └── main.py                 # Application entry point
├── tests/
│   ├── test_gemini_ai.py
│   └── test_transcript_extractor.py
├── docs/                       # Documentation
├── assets/                     # Screenshots and media
└── requirements.txt            # Python dependencies
```

## How to Contribute

### Types of Contributions

We welcome several types of contributions:

- **🐛 Bug Fixes**: Fix issues in transcript extraction, AI processing, or UI
- **✨ New Features**: Add new AI analysis types, UI improvements, or functionality
- **📚 Documentation**: Improve guides, API documentation, or code comments
- **🧪 Testing**: Add unit tests, integration tests, or improve test coverage
- **🎨 UI/UX Improvements**: Enhance the Streamlit interface and user experience
- **⚡ Performance**: Optimize transcript processing, API calls, or memory usage
- **🔧 Infrastructure**: Improve CI/CD, deployment, or development setup
- **🌐 Accessibility**: Make the application more accessible to diverse users

### Before You Start

1. **Check existing issues** and pull requests to avoid duplicates
2. **For major changes**, open an issue first to discuss your proposal
3. **For AI feature changes**, ensure you have access to test with Gemini API
4. **Make sure your contribution** aligns with the project's educational goals

## Development Setup

### Local Development Environment

1. **Create a new branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   # or for bug fixes:
   git checkout -b fix/issue-description
   # or for documentation:
   git checkout -b docs/documentation-update
   ```

2. **Install development dependencies**:
   ```bash
   pip install -r requirements.txt
   # For development tools (if needed):
   pip install pytest black flake8 mypy
   ```

3. **Set up environment variables** (create `.env` file):
   ```bash
   # Optional: Set default API key for testing
   GEMINI_API_KEY=your_test_api_key_here
   ```

4. **Run the application locally**:
   ```bash
   streamlit run src/main.py
   ```

### Testing Your Changes

1. **Manual Testing**:
   - Test transcript extraction with various YouTube videos
   - Verify AI features work with your Gemini API key
   - Check UI responsiveness and functionality
   - Test edge cases (private videos, no captions, etc.)

2. **Automated Testing**:
   ```bash
   # Run all tests
   python -m pytest tests/
   
   # Run specific test file
   python -m pytest tests/test_transcript_extractor.py
   
   # Run with coverage
   python -m pytest tests/ --cov=src/app
   ```

3. **Code Quality Checks**:
   ```bash
   # Format code
   black src/
   
   # Check code style
   flake8 src/
   
   # Type checking (if applicable)
   mypy src/
   ```

## Coding Standards

### Python Code Standards

#### General Guidelines
- Follow **PEP 8** style guidelines
- Use **meaningful variable and function names**
- Include **docstrings** for all modules, classes, and functions
- Keep functions **focused and single-purpose**
- Handle **exceptions gracefully** with user-friendly error messages

#### Specific to This Project
- **Streamlit components** should be in `ui.py`
- **API interactions** should include proper error handling
- **User input validation** should be thorough
- **Session state management** should be clean and organized

#### Code Examples

```python
# Good: Clear function with docstring
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
    ]
    # Implementation here...

# Good: Error handling with user feedback
try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return transcript
except Exception as e:
    st.error(f"YouTube Transcript API failed: {str(e)}")
    return None
```

### Documentation Standards

- **Docstrings**: Use Google-style docstrings for all functions
- **Comments**: Explain complex logic or business rules
- **README updates**: Update documentation for new features
- **Type hints**: Use type hints where appropriate

### UI/UX Standards

- **Consistent styling**: Follow existing CSS patterns in `ui.py`
- **User feedback**: Provide clear success/error messages
- **Loading states**: Use spinners for long operations
- **Responsive design**: Ensure components work on different screen sizes

## Testing Guidelines

### Writing Tests

1. **Unit Tests**: Test individual functions and methods
   ```python
   def test_extract_video_id():
       extractor = YouTubeTranscriptExtractor()
       video_id = extractor.extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
       assert video_id == "dQw4w9WgXcQ"
   ```

2. **Integration Tests**: Test component interactions
   ```python
   def test_gemini_ai_integration():
       gemini = GeminiAI("test_api_key")
       # Test with mock data
       assert gemini.is_configured() == True
   ```

3. **Edge Case Testing**: Test with various inputs
   - Invalid YouTube URLs
   - Videos without captions
   - Empty or very long transcripts
   - API failures and network issues

### Test Coverage

- Aim for **80%+ code coverage** for core functionality
- Focus on **critical paths**: transcript extraction, AI processing
- Include **error handling** scenarios in tests
- Test **user interface** components where possible

## Commit Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Commit Message Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

- `feat`: New feature (AI analysis, UI component, functionality)
- `fix`: Bug fix (transcript extraction, API issues, UI bugs)
- `docs`: Documentation changes (README, docstrings, guides)
- `style`: Code style changes (formatting, CSS, no logic changes)
- `refactor`: Code refactoring without changing functionality
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, CI/CD, config)
- `perf`: Performance improvements

### Scopes (Optional)

- `extractor`: YouTube transcript extraction functionality
- `ai`: Gemini AI integration and processing
- `ui`: User interface and Streamlit components
- `chat`: Chat functionality
- `notes`: Note-taking features
- `export`: Download and export functionality

### Examples

```
feat(ai): add flashcard generation feature using Gemini API

fix(extractor): handle videos with disabled captions gracefully

docs: update installation guide with Python version requirements

style(ui): improve transcript display formatting and spacing

refactor(ai): optimize API calls to reduce processing time

test(extractor): add unit tests for video ID extraction

chore: update dependencies to latest versions
```

## Pull Request Process

### Before Submitting

1. **Update your branch** with the latest changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run all tests** and ensure they pass:
   ```bash
   python -m pytest tests/
   ```

3. **Test manually** with the application running
4. **Update documentation** if you've added new features
5. **Check code formatting** and style compliance

### Submitting Your Pull Request

1. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a pull request** from your fork to the main repository

3. **Fill out the PR template** completely:
   - Clear description of changes
   - Screenshots for UI changes
   - Testing steps performed
   - Breaking changes (if any)

### Pull Request Checklist

- [ ] **Code follows** the project's coding standards
- [ ] **Tests added/updated** for new functionality
- [ ] **Documentation updated** (README, docstrings, etc.)
- [ ] **Manual testing** performed successfully
- [ ] **No breaking changes** (or clearly documented)
- [ ] **Screenshots included** for UI changes
- [ ] **Issue linked** (if applicable)

### Review Process

1. **Automated checks** must pass (CI/CD, tests)
2. **At least one maintainer review** required
3. **Address feedback** promptly and professionally
4. **Maintain clean commit history** (squash if requested)
5. **Final approval** from maintainer before merge

## Issue Guidelines

### Before Creating an Issue

1. **Search existing issues** to avoid duplicates
2. **Check the FAQ** and documentation
3. **Test with latest version** to confirm the issue persists
4. **Gather relevant information** (error messages, screenshots, etc.)

### Bug Reports

Include the following information:

- **Environment**:
  - Python version
  - Operating system
  - Browser (for UI issues)
  - Streamlit version

- **Bug Description**: Clear, concise description
- **Steps to Reproduce**: Detailed reproduction steps
- **Expected vs Actual Behavior**: What should happen vs what happens
- **Error Messages**: Full error messages or logs
- **Screenshots**: Visual evidence of the issue
- **Sample Data**: YouTube URL that causes the issue (if applicable)

### Feature Requests

When requesting a feature:

- **Feature Description**: Clear description of the proposed feature
- **Use Case**: Real-world scenario where this would be useful
- **Proposed Implementation**: Your ideas for how it could work
- **Examples**: Similar features in other applications
- **Priority**: How important is this feature to you/users?

### AI/ML Related Issues

For AI functionality issues:

- **Model Version**: Which Gemini model is being used
- **API Key Status**: Is the API key valid and has quota?
- **Input Data**: Type and size of transcript being processed
- **Expected Output**: What kind of analysis was expected
- **Actual Output**: What the AI actually generated

## Community

### Getting Help

If you need help or have questions:
- **💬 GitHub Discussions**: For general questions and ideas
- **🐛 GitHub Issues**: For bug reports and feature requests
- **📧 Email**: For sensitive issues or direct contact
- **📖 Documentation**: Check existing docs and usage guides

### Communication Guidelines

- **Be respectful** and constructive in all interactions
- **Provide context** when asking questions or reporting issues
- **Follow up** on your issues and pull requests
- **Help others** when you can share knowledge or experience

### Recognition

All contributors are recognized in our documentation and commit history. We maintain a contributors section to acknowledge everyone who helps improve the project.

### Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:
- **Use inclusive language** in code, comments, and discussions
- **Be respectful** of different viewpoints and experiences
- **Focus on collaboration** and constructive feedback
- **Report issues** if you experience or witness unacceptable behavior

## Development Workflow

### Typical Development Cycle

1. **Choose an issue** or propose a new feature
2. **Create a branch** for your work
3. **Develop and test** your changes locally
4. **Write/update tests** for your changes
5. **Update documentation** as needed
6. **Submit a pull request** with clear description
7. **Respond to feedback** during code review
8. **Celebrate** when your contribution is merged! 🎉

### Useful Commands Reference

```bash
# Setup and Development
git clone https://github.com/your-username/yt-transcript-gpt.git
cd yt-transcript-gpt
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Testing
streamlit run src/main.py                    # Run application
python -m pytest tests/                      # Run all tests
python -m pytest tests/ --cov=src/app      # Run with coverage

# Code Quality
black src/                                   # Format code
flake8 src/                                 # Check style
python -m pytest tests/ -v                 # Verbose test output

# Git Workflow
git checkout -b feature/new-feature
git add .
git commit -m "feat: add new feature description"
git push origin feature/new-feature
```

---

## 📞 Support

- **📧 Email**: For direct contact and sensitive issues
- **🐛 Issues**: [GitHub Issues](https://github.com/nova-cortex/yt-transcript-gpt/issues)
- **🔓 Security**: [Security Policy](https://github.com/nova-cortex/yt-transcript-gpt/security)
- **⛏ Pull Requests**: [GitHub Pull Requests](https://github.com/nova-cortex/yt-transcript-gpt/pulls)
- **📖 Documentation**: [Project Documentation](https://github.com/nova-cortex/yt-transcript-gpt/tree/main/docs)

### External Resources

- **Streamlit Documentation**: https://docs.streamlit.io/
- **Google Gemini AI**: https://ai.google.dev/
- **YouTube Transcript API**: https://github.com/jdepoix/youtube-transcript-api
- **yt-dlp Documentation**: https://github.com/yt-dlp/yt-dlp

Thank you for contributing to YouTube Transcript GPT! Together, we're making AI-powered learning more accessible to everyone. Your contributions help students, educators, and content creators get more value from YouTube videos. 🚀📚✨