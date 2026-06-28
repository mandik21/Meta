import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
VISION_MODEL = os.getenv("VISION_MODEL", "gpt-4o")
MAX_KEYWORDS = 49
TITLE_MAX_CHARS = 70
DESCRIPTION_MAX_CHARS = 150
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".tiff"}
IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
