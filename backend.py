from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import sqlite3
import os

app = FastAPI(title="Camarão Seco - Lead Capture API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[""https://www.voacamarao.com",
    "https://voacamarao.com", "https://vaocamarao.github.io", "https://voacamarao.vercel.app",
    "http://localhost:5500", # Para testes locais no seu PC
    "http://127.0.0.1:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.join(os.path.dirname(__file__), "leads.db")


class LeadIn(BaseModel):
    nome: str = Field(..., min_length=2, max_length=120)
    empresa: str = Field(..., min_length=2, max_length=200)
    estimativa: str = Field(..., pattern=r"^(10kg|50kg|100kg\+)$")


class LeadOut(LeadIn):
    id: int
    criado_em: str


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE IF NOT EXISTS leads ("
        "  id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "  nome TEXT NOT NULL,"
        "  empresa TEXT NOT NULL,"
        "  estimativa TEXT NOT NULL,"
        "  criado_em TEXT NOT NULL"
        ")"
    )
    return conn


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/lead", response_model=LeadOut, status_code=201)
def create_lead(lead: LeadIn):
    conn = get_connection()
    try:
        now = datetime.now(timezone.utc).isoformat()
        cursor = conn.execute(
            "INSERT INTO leads (nome, empresa, estimativa, criado_em) VALUES (?, ?, ?, ?)",
            (lead.nome, lead.empresa, lead.estimativa, now),
        )
        conn.commit()
        return LeadOut(
            id=cursor.lastrowid,
            nome=lead.nome,
            empresa=lead.empresa,
            estimativa=lead.estimativa,
            criado_em=now,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        conn.close()


@app.get("/api/leads", response_model=list[LeadOut])
def list_leads():
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM leads ORDER BY criado_em DESC").fetchall()
        return [
            LeadOut(id=r["id"], nome=r["nome"], empresa=r["empresa"],
                    estimativa=r["estimativa"], criado_em=r["criado_em"])
            for r in rows
        ]
    finally:
        conn.close()
