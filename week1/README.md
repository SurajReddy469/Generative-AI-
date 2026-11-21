# Week 1: Getting Started with Google Gemini API

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Google GenAI](https://img.shields.io/badge/Google%20GenAI-Gemini%20API-4285F4?style=flat&logo=google&logoColor=white)](https://ai.google.dev/)
[![Status](https://img.shields.io/badge/Status-Completed-success?style=flat)]()

## Aim
To set up the development environment, securely manage API credentials using `.env`, and generate text completions using the official Google GenAI SDK with the `gemini-3.5-flash-lite` model.

---

## Prerequisites & Credentials
- **Python 3.10+**
- **Google Gemini API Key**: Obtain a free API key from [Google AI Studio](https://aistudio.google.com/).

---

## Project Structure
```text
week1/
├── .env.example       # Template for required environment variables
├── .env               # Local API credentials (strictly git-ignored)
├── .gitignore         # Ignores sensitive environment files and caches
├── main.py            # Text generation script
├── requirements.txt   # Dependencies (google-genai, python-dotenv)
└── README.md          # Week 1 guide
```

---

## How to Run Week 1

### Step 1: Install Dependencies
From the repository root (or within `week1/`):
```powershell
pip install -r week1/requirements.txt
```

### Step 2: Configure Environment Variables
Create your local `.env` file from the provided `.env.example`:

**PowerShell (Windows):**
```powershell
Copy-Item week1\.env.example week1\.env
```

**Bash (Linux / macOS):**
```bash
cp week1/.env.example week1/.env
```

Open `week1/.env` and insert your Gemini API key:
```env
GEMINI_API_KEY=AIzaSy...your_actual_key_here...
```

### Step 3: Execute the Script

#### Option A: Run directly from Repository Root (Recommended)
```powershell
python week1/main.py
```

#### Option B: Run from inside `week1/`
```powershell
cd week1
python main.py
```

---

## Expected Output
```text
===================Week1 =====================

LLM Response:
Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think like humans and mimic their actions...
```

---

## Troubleshooting

| Issue | Cause | Fix |
| :--- | :--- | :--- |
| `ValueError: GEMINI_API_KEY is missing` | `.env` file does not exist or `GEMINI_API_KEY` is empty | Copy `.env.example` to `.env` in `week1/` and set your key. |
| `503 Service Unavailable` | Temporary server overload on large models | The script defaults to `gemini-3.5-flash-lite`, which is optimized for high availability and low latency. |
| `ModuleNotFoundError: No module named 'google'` | Dependencies not installed in active environment | Run `pip install -r requirements.txt` within your virtual environment (`.venv`). |
