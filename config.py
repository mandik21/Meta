from __future__ import print_function
import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
VISION_MODEL = os.getenv("VISION_MODEL", "gpt-4o")
MAX_KEYWORDS = 49
TITLE_MAX_CHARS = 70
DESCRIPTION_MAX_CHARS = 150
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".tiff"}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
