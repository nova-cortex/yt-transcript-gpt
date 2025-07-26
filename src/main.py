"""
Project: yt-transcript-gpt
Author: ukr
License: MIT
Repository: https://github.com/nova-cortex/yt-transcript-gpt
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import main

if __name__ == "__main__":
    main()
