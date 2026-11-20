# JARVIS PWA v2.1
A local-first Progressive Web App starter for Android and desktop browsers.

## Included
- Futuristic responsive interface and PWA install support.
- English, Hindi and Marathi language selection.
- Local time/date/help commands and device-local notes.
- Browser speech recognition where supported, plus speech synthesis.
- Conversation history and notes stored in browser localStorage.
- Optional secured FastAPI backend connection.
- Service-worker app-shell caching.

## Deploy
This repository is hosted with GitHub Pages. Commit the site files to the repository root and enable Pages from the `main` branch / root folder. A feature branch does not update the live site until its pull request is merged.

## Backend
GitHub Pages only serves static files. It cannot run the Python API. See [backend/README.md](backend/README.md). Never put model-provider API keys in this repository or in frontend JavaScript.

## Limitations
This is a starter, not a fully integrated AI service. The included backend stores chat text and notes in SQLite and returns a setup reply for chat until a model provider is integrated server-side. Browser speech recognition may require an online browser service. A PWA cannot continuously listen in the background or provide a wake word. Local browser data is not encrypted; do not save passwords, Aadhaar, banking details or sensitive information.
