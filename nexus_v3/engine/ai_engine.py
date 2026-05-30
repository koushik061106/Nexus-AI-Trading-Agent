import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv

# Initialize logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    log.warning("GEMINI_API_KEY not found in environment.")

def call_ai(prompt: str) -> str:
    """
    Sends the prompt to Gemini Flash and returns the raw string response.
    Optimized for ultra-fast, JSON-based trading decisions.
    """
    if not API_KEY:
        log.error("Cannot call AI: GEMINI_API_KEY is missing.")
        return ""

    try:
        # Using 2.5-flash for rapid execution loops
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        log.error(f"Gemini Engine Error: {str(e)}")
        return ""