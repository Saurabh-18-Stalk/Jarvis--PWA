# JARVIS API v2.2

FastAPI backend for JARVIS PWA with server-side AI provider support.

## Supported AI providers

Set `AI_PROVIDER` to exactly one of:

- `openrouter` — default model `openrouter/free`; free model availability and free-plan request caps: https://openrouter.ai/ and https://openrouter.ai/collections/free-models
- `gemini` — default model `gemini-2.5-flash`; check model availability and free-tier quotas: https://aistudio.google.com/ and https://ai.google.dev/gemini-api/docs/pricing
- `groq` — default model `openai/gpt-oss-20b`; check current model availability and account limits: https://console.groq.com/ and https://console.groq.com/docs/rate-limits

Free tiers, model availability, data policies, and quotas can change. A free tier is not unlimited. Provider keys belong only in the private backend environment, never in frontend JavaScript, GitHub, or the JARVIS Settings screen.

## Deploy

Use Python 3.10+ and a host that supports a persistent disk if you want SQLite data to survive restarts.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env with JARVIS_TOKEN, AI_PROVIDER and the selected provider key
uvicorn main:app --host 0.0.0.0 --port 8000
```

For production, deploy behind HTTPS, set a strong random `JARVIS_TOKEN`, set `CORS_ORIGINS` to the exact JARVIS Pages origin, and configure `DATABASE_PATH` on persistent storage. Configure environment variables in the hosting dashboard; do not upload a real `.env` file.

Health check: `GET /health` (reports whether the selected provider key is configured, never the key itself). Protected chat and notes endpoints require `Authorization: Bearer <JARVIS_TOKEN>`.

## API

- `POST /api/chat` — calls the selected AI provider and saves the exchange to SQLite.
- `GET /api/notes`, `POST /api/notes`, `DELETE /api/notes/{note_id}` — backend notes API.

GitHub Pages hosts only the static PWA; it does not run this Python API. The current PWA keeps local notes and local time/date commands on-device. General AI chat requires this backend to be separately deployed and configured in the app Settings.

## Privacy and safety

The backend stores submitted prompts and AI replies in its SQLite database. Do not send passwords, Aadhaar numbers, banking details, or other sensitive information. Review each provider's current data-use policy before sending personal data.
