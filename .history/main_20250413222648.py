import base64
import requests
import io
from PIL import Image
from dotenv import load_env
import os
import logging

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


if not GROQ_API_KEY:
    raise ValueError("GROQ API is not set in .env")