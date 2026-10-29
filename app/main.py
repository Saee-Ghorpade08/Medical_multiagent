from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.schemas import AskRequest, AskResponse
from app.agents.team import ask_healthcare_team

app = FastAPI(
    title="Medical Healthcare Multi-Agent Assistant",
    description="Educational multi-agent healthcare assistant for GenAI & ML DevOps coursework.",
    version="1.0.0",
)

ROOT = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(ROOT / "static")), name="static")


@app.get("/", response_class=HTMLResponse)
def home():
    return (ROOT / "static" / "index.html").read_text(encoding="utf-8")


@app.get("/health")
def health():
    return {"status": "ok", "service": "medical-healthcare-assistant"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    try:
        answer = ask_healthcare_team(request.question)
        return AskResponse(answer=answer)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Agent request failed: {exc}") from exc
