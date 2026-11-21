import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import errors

# Load .env from the same directory as this file
load_dotenv(Path(__file__).parent / ".env", override=True)
api_key = os.getenv("GEMINI_API_KEY")

if not api_key or "your_" in api_key.lower():
    print("\n[ERROR] GEMINI_API_KEY is missing or unconfigured.")
    print("Please open 'week1/.env' and paste your Gemini API key from https://aistudio.google.com/apikey.\n")
    sys.exit(1)

try:
    client = genai.Client(api_key=api_key)

    # Using gemini-3.5-flash-lite for fast, reliable response
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="What is Artificial Intelligence? Explain in simple words.",
    )

    print("=================== Week 1 =====================")
    print("\nLLM Response:")
    print(response.text)

except errors.ClientError as e:
    if "401" in str(e) or "UNAUTHENTICATED" in str(e):
        print("\n" + "=" * 60)
        print("[ERROR 401: UNAUTHENTICATED - Invalid or Expired API Key]")
        print("=" * 60)
        print("Google Generative AI rejected your API key:")
        print(f"Reason: {e.message if hasattr(e, 'message') else e}")
        print("\nHow to fix:")
        print("1. Go to https://aistudio.google.com/apikey")
        print("2. Generate a new API key.")
        print("3. Paste it in 'week1/.env':")
        print("   GEMINI_API_KEY=...")
        print("=" * 60 + "\n")
        sys.exit(1)
    else:
        raise
