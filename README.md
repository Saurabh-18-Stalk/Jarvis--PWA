# JARVIS PWA v2.3

Local-first Progressive Web App for Android and Windows/desktop browsers, with an optional private FastAPI backend for general AI conversations.

## Included
- Responsive futuristic interface and installable PWA.
- English, Hindi and Marathi locale selection.
- Device-local notes and conversation history.
- Local time/date/help/note commands.
- Browser speech recognition where supported and speech synthesis replies.
- Backend health test in Settings.
- Optional FastAPI + SQLite backend with server-side OpenRouter, Gemini and Groq support.
- Service-worker app-shell caching for offline access.
- Chat export to JSON.

Live site: https://saurabh-18-stalk.github.io/Jarvis--PWA/

## Backend
See backend/README.md. GitHub Pages hosts static files only. Deploy the backend separately over HTTPS. Set JARVIS_TOKEN, AI_PROVIDER, the selected provider key, exact CORS_ORIGINS and a persistent DATABASE_PATH in the hosting dashboard. Enter only the backend URL and JARVIS bearer token in the PWA Settings. Never commit provider keys or place them in frontend code.

## Run backend on Windows
Use Python 3.10+. In PowerShell from the backend folder:
~~~powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env locally; never commit the real file.
uvicorn main:app --host 127.0.0.1 --port 8000
~~~

## Offline and voice limits
After first load, cached app shell and local commands can work offline. AI chat needs internet and a reachable backend. Browser speech recognition support and language availability vary and may require an online speech service. Speech synthesis voices vary by device. A PWA cannot continuously listen in the background or provide a reliable always-on wake word.

## Not yet included
A native wake-word service, fully offline speech-to-text model, Windows system automation, screen/computer vision understanding, and autonomous multi-step desktop actions are not part of this PWA release. These require a separately installed Windows companion with explicit approvals and additional testing.

## Privacy
Browser notes and history are not encrypted. The backend stores prompts and replies in SQLite. Do not store passwords, Aadhaar numbers or banking details. The backend bearer token is stored in this browser's local storage; avoid shared devices. Use HTTPS and a strong token.
