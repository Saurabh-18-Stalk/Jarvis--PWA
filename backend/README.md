# JARVIS API starter
Run locally with Python 3.10+:
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env and set a long random JARVIS_TOKEN
uvicorn main:app --reload --port 8000
```
Health check: `GET /health`. Protected endpoints require `Authorization: Bearer <JARVIS_TOKEN>`. Configure `CORS_ORIGINS` to your exact deployed site origin. Use HTTPS in production and a persistent disk for SQLite. Do not commit your real .env file. The chat endpoint is deliberately a placeholder and does not call an AI model.
