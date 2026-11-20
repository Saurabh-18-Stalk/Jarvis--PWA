import json
import os
import sqlite3
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Optional
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
DB = os.getenv("DATABASE_PATH", "jarvis.db")
TOKEN = os.getenv("JARVIS_TOKEN", "")
AI_PROVIDER = os.getenv("AI_PROVIDER", "openrouter").strip().lower()
AI_MODEL = os.getenv("AI_MODEL", "").strip()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
CORS_ORIGINS = [x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:5500").split(",") if x.strip()]

app = FastAPI(title="JARVIS API", version="2.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

def connect():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    Path(DB).parent.mkdir(parents=True, exist_ok=True) if os.path.dirname(DB) else None
    with connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL, language TEXT NOT NULL,
            reply TEXT NOT NULL, created_at TEXT NOT NULL
        )""")
        con.execute("""CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note TEXT NOT NULL, created_at TEXT NOT NULL
        )""")

init_db()

def auth(authorization: Optional[str]):
    if not TOKEN:
        raise HTTPException(503, "Backend token is not configured")
    if authorization != f"Bearer {TOKEN}":
        raise HTTPException(401, "Invalid or missing bearer token")

class ChatIn(BaseModel):
    message: str = Field(min_length=1, max_length=8000)
    language: str = Field(default="en-IN", max_length=16)

class NoteIn(BaseModel):
    note: str = Field(min_length=1, max_length=4000)

def post_json(url: str, payload: dict, headers: dict) -> dict:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={**headers, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        # Do not return provider response bodies; they may contain sensitive diagnostics.
        if exc.code == 429:
            raise HTTPException(429, "AI provider rate limit reached. Try again later or switch provider.")
        if exc.code in (401, 403):
            raise HTTPException(502, "AI provider rejected its API key. Check the server environment settings.")
        raise HTTPException(502, f"AI provider request failed (HTTP {exc.code}).")
    except (urllib.error.URLError, TimeoutError):
        raise HTTPException(502, "Could not reach the AI provider. Try again shortly.")
    except (ValueError, KeyError, IndexError, TypeError):
        raise HTTPException(502, "AI provider returned an unreadable response.")

def generate_openai_compatible(provider: str, api_key: str, base_url: str, default_model: str, message: str, language: str) -> str:
    if not api_key:
        raise HTTPException(503, f"{provider} API key is not configured on the backend.")
    model = AI_MODEL or default_model
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": f"You are JARVIS, a helpful personal assistant. Reply in the user's selected language when practical: {language}. Be clear and concise."},
            {"role": "user", "content": message},
        ],
        "temperature": 0.7,
        "max_tokens": 900,
    }
    headers = {"Authorization": f"Bearer {api_key}"}
    if provider == "OpenRouter":
        headers["HTTP-Referer"] = os.getenv("PUBLIC_APP_URL", "https://saurabh-18-stalk.github.io/Jarvis--PWA/")
        headers["X-Title"] = "JARVIS PWA"
    data = post_json(base_url, payload, headers)
    return data["choices"][0]["message"]["content"].strip()

def generate_gemini(message: str, language: str) -> str:
    if not GEMINI_API_KEY:
        raise HTTPException(503, "Gemini API key is not configured on the backend.")
    model = AI_MODEL or "gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "system_instruction": {"parts": [{"text": f"You are JARVIS, a helpful personal assistant. Reply in the user's selected language when practical: {language}. Be clear and concise."}]},
        "contents": [{"role": "user", "parts": [{"text": message}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 900},
    }
    data = post_json(url, payload, {})
    return "".join(part.get("text", "") for part in data["candidates"][0]["content"]["parts"]).strip()

def generate_reply(message: str, language: str) -> str:
    if AI_PROVIDER == "openrouter":
        return generate_openai_compatible("OpenRouter", OPENROUTER_API_KEY, "https://openrouter.ai/api/v1/chat/completions", "openrouter/free", message, language)
    if AI_PROVIDER == "groq":
        return generate_openai_compatible("Groq", GROQ_API_KEY, "https://api.groq.com/openai/v1/chat/completions", "openai/gpt-oss-20b", message, language)
    if AI_PROVIDER == "gemini":
        return generate_gemini(message, language)
    raise HTTPException(503, "Unsupported AI_PROVIDER. Choose openrouter, groq, or gemini.")

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "jarvis-api",
        "version": "2.2.0",
        "ai_provider": AI_PROVIDER,
        "ai_configured": bool(
            (AI_PROVIDER == "openrouter" and OPENROUTER_API_KEY)
            or (AI_PROVIDER == "groq" and GROQ_API_KEY)
            or (AI_PROVIDER == "gemini" and GEMINI_API_KEY)
        ),
    }

@app.post("/api/chat")
def chat(data: ChatIn, authorization: Optional[str] = Header(default=None)):
    auth(authorization)
    reply = generate_reply(data.message, data.language)
    with connect() as con:
        con.execute(
            "INSERT INTO messages(message,language,reply,created_at) VALUES(?,?,?,?)",
            (data.message, data.language, reply, datetime.now(timezone.utc).isoformat()),
        )
    return {"reply": reply, "provider": AI_PROVIDER}

@app.get("/api/notes")
def list_notes(authorization: Optional[str] = Header(default=None)):
    auth(authorization)
    with connect() as con:
        rows = con.execute("SELECT id,note,created_at FROM notes ORDER BY id DESC LIMIT 100").fetchall()
    return {"notes": [dict(r) for r in rows]}

@app.post("/api/notes")
def add_note(data: NoteIn, authorization: Optional[str] = Header(default=None)):
    auth(authorization)
    with connect() as con:
        cur = con.execute(
            "INSERT INTO notes(note,created_at) VALUES(?,?)",
            (data.note, datetime.now(timezone.utc).isoformat()),
        )
        return {"id": cur.lastrowid, "note": data.note}

@app.delete("/api/notes/{note_id}")
def delete_note(note_id: int, authorization: Optional[str] = Header(default=None)):
    auth(authorization)
    with connect() as con:
        cur = con.execute("DELETE FROM notes WHERE id=?", (note_id,))
    if not cur.rowcount:
        raise HTTPException(404, "Note not found")
    return {"deleted": True}
