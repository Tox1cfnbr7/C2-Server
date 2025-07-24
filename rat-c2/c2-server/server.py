# server.py
import asyncio
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Speicher für aktive Connections
clients = set()

@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    try:
        # Eingehende Nachrichten (Shell‑Output vom Agent)
        while True:
            data = await ws.receive_text()
            # Ausgabe im Server‑Terminal
            print(f"[Agent] {data}", end="")
            # Alternativ: Buffer für UI speichern
    except WebSocketDisconnect:
        clients.remove(ws)

async def send_command(cmd: str):
    """Broadcastet ein Kommando an alle verbundenen Agents."""
    dead = []
    for ws in clients:
        try:
            await ws.send_text(cmd)
        except:
            dead.append(ws)
    for ws in dead:
        clients.remove(ws)

if __name__ == "__main__":
    # Starte den Server (HTTP + WS) auf Port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
