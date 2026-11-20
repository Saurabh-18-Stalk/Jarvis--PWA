# JARVIS AI Personal Assistant

JARVIS is a local-first web/PWA assistant with an optional private AI backend and a separate Flutter companion for Android and Windows.

## Live Chrome / Android website
https://saurabh-18-stalk.github.io/Jarvis--PWA/

Open this URL in Chrome. On Android, use Chrome menu → **Install app** or **Add to Home screen**. If the install prompt does not appear, confirm the site has loaded over HTTPS, reload it once, then use the Chrome menu option.

## Web app features
- Responsive mobile and desktop interface with PWA/offline app-shell caching.
- English, Hindi and Marathi locale selection.
- Browser voice input and spoken replies where supported by Chrome/device speech services.
- Local time/date/help commands, notes, chat history and JSON export.
- Explicitly selected text/code files (up to 100 KB each, 80 KB total context) can be sent to the configured AI backend for analysis.
- AI chat, code assistance, YouTube planning and social post drafts when the backend is configured.
- Backend health check and locally stored connection settings.

## Native companion
The Flutter source is in [native_app](./native_app). It targets Android and Windows with voice input/output, backend chat, user-selected file picking and saving generated replies. See [native app instructions](./native_app/README.md).

## Backend setup (required for general AI)
GitHub Pages hosts static files only; it cannot run the Python API. Deploy [backend](./backend) separately to an HTTPS host. Configure these environment variables in the host dashboard:
- `JARVIS_TOKEN`: a long random private access token.
- `AI_PROVIDER`: `openrouter`, `groq` or `gemini`.
- The matching provider API key: `OPENROUTER_API_KEY`, `GROQ_API_KEY` or `GEMINI_API_KEY`.
- `CORS_ORIGINS`: include `https://saurabh-18-stalk.github.io` and any additional exact web origins you use.
- `DATABASE_PATH`: use a persistent disk path if the host supports one.

Then enter only the backend HTTPS URL and JARVIS token in JARVIS Settings. Never put provider keys or the bearer token in GitHub source code. The backend stores submitted prompts and replies in SQLite; configure persistent storage if you need data to survive redeployments.

## Safe-use boundaries
- JARVIS reads only files you explicitly select. A browser app cannot silently scan all files on a phone or computer.
- Code is generated as text and is not automatically executed.
- YouTube uploads, social publishing, DMs, account changes and purchases are not enabled. Real account actions require official APIs, OAuth permissions, quotas and an explicit confirmation step.
- Background always-on microphone/wake-word listening, full offline speech recognition, unrestricted device control and autonomous desktop actions are not included.
- Review generated code and drafts before using or publishing them.

## Local backend development
See [backend/README.md](./backend/README.md). GitHub Pages is not a backend host. Do not commit real `.env` files or API keys.
