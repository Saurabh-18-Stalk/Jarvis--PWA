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

## Recommended roadmap for a reliable JARVIS

Build and test these in order; do not enable risky automation before the core assistant is stable.

1. **Core reliability:** backend connection indicator, clear offline mode, request timeouts, retry action, readable error messages, and saved chat history.
2. **Voice experience:** push-to-talk by default, selectable English/Hindi/Marathi speech, stop-speaking control, and visible microphone status. Avoid always-on microphone listening.
3. **Private AI connection:** keep provider API keys only on the server; use HTTPS, a private JARVIS token, rate limits, and persistent database storage.
4. **Personal workspace:** user-selected file import, document summaries, generated-file export, searchable notes, and explicit confirmation before overwriting or deleting anything.
5. **Productivity integrations:** reminders and calendar/email connections through official OAuth integrations; ask for confirmation before sending or changing events.
6. **Creator tools:** YouTube research and script packages, captions, thumbnails briefs, and social post drafts. Publishing and messaging must require official APIs and final user approval.
7. **Developer tools:** code generation, explanation, test suggestions, and downloadable project files. Never execute generated code automatically.
8. **Release quality:** test on the target Android version and Windows, verify microphone/file permissions, provide an in-app diagnostics screen, and publish signed release builds with versioned update notes.

### Important capability boundaries

JARVIS can only access files that the user explicitly selects or grants through supported platform permissions. A web app cannot silently browse the whole phone or computer. Background wake-word listening, unrestricted device control, automatic social publishing, and arbitrary app control need separate native permissions, platform-specific integrations, and security reviews. Treat them as later, opt-in features—not promises of the current build.
