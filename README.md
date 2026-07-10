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

Deploy the Flask app

This repository is ready to deploy on Render from GitHub.

1. Push the latest code to GitHub.
2. In Render, create a new `Web Service` from this repository.
3. Render will detect `render.yaml` and use:
   - build command: `pip install -r requirements.txt`
   - start command: `gunicorn wsgi:app`
4. Add these environment variables in Render:
   - `NEWS_API_KEY` required
   - `GROQ_API_KEY` optional
5. After deploy, Render will give you a public HTTPS URL such as `https://your-news-app.onrender.com`.

Use the Android app on any network

Once the Flask app is hosted, open the Android app and set the server URL to your public Render URL, for example:

```text
https://your-news-app.onrender.com/
```

That URL will work from any network because the backend is no longer running only on your local Wi-Fi.

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
