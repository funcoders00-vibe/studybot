import os
import sys

# Ensure backend root directory is in sys.path so 'src' can be imported cleanly on Vercel
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.main import app

# Explicit top-level entrypoints statically recognized by Vercel's Python builder
application = app
handler = app