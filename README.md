# News App

Simple Flask app that fetches news from NewsAPI and optionally checks authenticity via GROQ AI.

Setup

1. Create a virtual environment and install dependencies:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

1. Copy `.env.example` to `.env` and set `NEWS_API_KEY` (required) and `GROQ_API_KEY` (optional).

2. Run the app in development:

```powershell
python web.py
```

Build a Windows .exe

1. Make sure your `.env` file is present in the project folder.

2. Run the build script:

```powershell
.\build_exe.ps1
```

1. After the build finishes, your executable will be at `dist\NewsApp.exe`.

2. Keep a copy of `.env` next to `NewsApp.exe` so the app can read your API keys after packaging.

Notes

- The packaged app starts a local Flask server and opens your browser automatically.
- If `GROQ_API_KEY` is missing, authenticity checks are disabled and the app will still work.
- Keep your API keys private and do not commit `.env` to source control.
