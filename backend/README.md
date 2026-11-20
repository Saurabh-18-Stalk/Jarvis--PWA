# JARVIS API v2.3

FastAPI backend for the JARVIS PWA with server-side AI provider support.

## Supported AI providers

Set AI_PROVIDER to exactly one of:

- openrouter — default model openrouter/free. Free model availability and quotas: https://openrouter.ai/ and https://openrouter.ai/collections/free-models
- gemini — default model gemini-2.5-flash. Check availability and quotas: https://aistudio.google.com/ and https://ai.google.dev/gemini-api/docs/pricing
- groq — default model openai/gpt-oss-20b. Check availability and limits: https://console.groq.com/ and https://console.groq.com/docs/rate-limits

Free tiers, model availability, data policies and quotas can change; free access is not unlimited. Provider keys belong only in the private backend environment.

## Deploy

Use Python 3.10+ and an HTTPS host. Set these environment variables in the host dashboard:

- JARVIS_TOKEN: long random secret required for protected API routes.
- AI_PROVIDER: openrouter, gemini or groq.
- The matching OPENROUTER_API_KEY, GEMINI_API_KEY or GROQ_API_KEY.
- CORS_ORIGINS: exact origin of the hosted PWA, for example https://saurabh-18-stalk.github.io.
- DATABASE_PATH: SQLite file path on persistent storage, where supported.
- AI_MODEL: optional model override.

Do not upload a real .env file. GitHub Pages serves only static files and cannot run this Python API.

## Run locally on Windows

PowerShell, from this folder:

~~~powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env locally with your own token and provider key.
uvicorn main:app --host 127.0.0.1 --port 8000
~~~

Health check: GET /health. It reports selected provider and whether its key is configured, never the key itself. Protected routes require Authorization: Bearer <JARVIS_TOKEN>.

## API

- GET /health
- POST /api/chat — calls the selected provider and stores the exchange in SQLite.
- GET /api/notes, POST /api/notes, DELETE /api/notes/{note_id}

The current PWA stores notes locally on the device. Backend notes routes are available for future cross-device sync but are not yet wired into the PWA.

## Storage and privacy

SQLite on an ephemeral host filesystem can be lost after restart or redeploy. Configure persistent storage or migrate to a managed database before relying on long-term storage. Backend chat prompts and replies are stored in SQLite. Do not submit passwords, Aadhaar numbers, banking details or other sensitive information. Review the selected provider's current data-use policy.
