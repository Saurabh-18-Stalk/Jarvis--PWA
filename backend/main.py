import os, sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
DB = os.getenv("DATABASE_PATH", "jarvis.db")
TOKEN = os.getenv("JARVIS_TOKEN", "")
origins = [x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:5500").split(",") if x.strip()]
app = FastAPI(title="JARVIS API", version="2.1.0")
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False, allow_methods=["GET","POST","DELETE"], allow_headers=["Authorization","Content-Type"])

def connect():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with connect() as con:
        con.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, message TEXT NOT NULL, language TEXT NOT NULL, reply TEXT NOT NULL, created_at TEXT NOT NULL)")
        con.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, note TEXT NOT NULL, created_at TEXT NOT NULL)")
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

@app.get("/health")
def health():
    return {"status":"ok","service":"jarvis-api","version":"2.1.0"}

@app.post("/api/chat")
def chat(data: ChatIn, authorization: Optional[str] = Header(default=None)):
    auth(authorization)
    reply = "JARVIS backend is connected. Add your chosen AI provider integration on the server to enable generated answers."
    with connect() as con:
        con.execute("INSERT INTO messages(message,language,reply,created_at) VALUES(?,?,?,?)", (data.message,data.language,reply,datetime.now(timezone.utc).isoformat()))
    return {"reply":reply}

@app.get("/api/notes")
def list_notes(authorization: Optional[str] = Header(default=None)):
    auth(authorization)
    with connect() as con:
        rows = con.execute("SELECT id,note,created_at FROM notes ORDER BY id DESC LIMIT 100").fetchall()
    return {"notes":[dict(r) for r in rows]}

@app.post("/api/notes")
def add_note(data: NoteIn, authorization: Optional[str] = Header(default=None)):
    auth(authorization)
    with connect() as con:
        cur = con.execute("INSERT INTO notes(note,created_at) VALUES(?,?)", (data.note,datetime.now(timezone.utc).isoformat()))
        return {"id":cur.lastrowid,"note":data.note}

@app.delete("/api/notes/{note_id}")
def delete_note(note_id: int, authorization: Optional[str] = Header(default=None)):
    auth(authorization)
    with connect() as con:
        cur = con.execute("DELETE FROM notes WHERE id=?", (note_id,))
    if not cur.rowcount:
        raise HTTPException(404,"Note not found")
    return {"deleted":True}
