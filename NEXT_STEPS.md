# JARVIS v2.3 deployment checklist

1. Wait for GitHub Pages deployment and open the published URL.
2. Install the PWA from Android Chrome or a desktop browser.
3. Test local time/date, notes, delete, chat history, export, offline reload and microphone permissions.
4. Test Hindi and Marathi speech on the actual device; browser support varies.
5. Deploy backend/ on a Python 3.10+ HTTPS host.
6. Set private JARVIS_TOKEN, AI_PROVIDER, selected provider key, exact CORS_ORIGINS and persistent DATABASE_PATH.
7. Open /health and verify status and ai_configured.
8. In JARVIS Settings, enter backend URL and matching JARVIS token; Save and Test backend.

GitHub Pages is static hosting and cannot run FastAPI. AI keys stay on the backend host. SQLite needs persistent storage or data may be lost after host restarts. AI chat needs internet. Wake word, fully offline speech recognition, Windows automation and screen understanding remain future Windows companion work.
