# Contributing to DiscordRecords

Thank you for your interest in contributing to DiscordRecords! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected behavior vs actual behavior
- Your environment (OS, Python version, etc.)
- Console error messages (if any)

### Suggesting Features

Feature suggestions are welcome! Please create an issue with:
- Clear description of the feature
- Use case/motivation
- Potential implementation approach (if you have ideas)

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your fork (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

## 💻 Development Setup

1. Clone your fork:
```bash
git clone https://github.com/yourusername/DiscordRecords.git
cd DiscordRecords
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Setup your `.env` file for testing

## 📝 Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Comment complex logic
- Keep functions focused and modular

Example:
```python
def calculate_duration(seconds: int) -> str:
    """
    Convert seconds to MM:SS format
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted string like "3:45"
    """
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"
```

## 🧪 Testing

Before submitting a PR:
- Test all affected commands in Discord
- Verify error handling works
- Check console for warnings/errors
- Test with and without optional features (Spotify, AI)

## 📁 Project Structure

```
DiscordRecords/
├── bot.py                    # Main entry point
├── music/                    # Music playback logic
│   └── player.py
├── services/                 # External API integrations
│   ├── spotify_service.py
│   └── youtube_service.py
├── ai/                       # AI/NLP processing
│   └── language_processor.py
└── utils.py                  # Utility functions
```

## 🎯 Areas for Contribution

We especially welcome contributions in these areas:

### High Priority
- 🐛 Bug fixes
- 📚 Documentation improvements
- 🧪 Test coverage
- ♿ Accessibility improvements

### Features
- 🎵 Additional music sources
- 🔊 Audio effects/filters
- 📊 Queue visualization improvements
- 🤖 Enhanced AI understanding
- 🌐 Internationalization

### Code Quality
- ⚡ Performance optimizations
- 🧹 Code refactoring
- 🔒 Security improvements
- 📝 Type hints

## 🚫 What NOT to Do

- Don't include API keys or tokens in commits
- Don't make breaking changes without discussion
- Don't add dependencies without justification
- Don't ignore existing code style
- Don't submit untested code

## 📜 Commit Message Guidelines

Use clear, descriptive commit messages:

```
✅ Good:
- "Add playlist shuffle feature"
- "Fix volume control bug in player.py"
- "Improve Spotify error handling"

❌ Bad:
- "fix stuff"
- "update"
- "asdfasdf"
```

## 🔍 Code Review Process

1. Maintainer reviews your PR
2. Feedback may be provided
3. Make requested changes
4. PR is approved and merged
5. You're awesome! 🎉

## 📞 Questions?

- Open an issue for questions
- Tag it with `question` label
- We'll respond as soon as possible

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

All contributors will be recognized in the project. Thank you for making DiscordRecords better!

---

**Happy coding! 🎵**
