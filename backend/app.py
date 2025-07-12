# backend/app.py
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, Form
from fastapi.staticfiles import StaticFiles
import json, datetime as dt

BASE = Path(__file__).resolve().parent
IMG_DIR = BASE / "static" / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")

# conexiones WebSocket por callsign
_rooms: dict[str, set[WebSocket]] = {}

@app.post("/api/photo")
async def api_photo(
        callsign: str = Form(...),
        ref: str = Form(...),
        file: UploadFile = Form(...)
):
    # guarda la foto
    folder = IMG_DIR / callsign
    folder.mkdir(parents=True, exist_ok=True)
    fname = f"{dt.datetime.utcnow().timestamp():.0f}{Path(file.filename).suffix}"
    path = folder / fname
    with path.open("wb") as f:
        f.write(await file.read())

    url = f"/static/images/{callsign}/{fname}"
    payload = {"callsign": callsign, "ref": ref, "url": url,
               "ts": dt.datetime.utcnow().isoformat()}

    # broadcast
    for ws in _rooms.get(callsign, set()):
        await ws.send_json(payload)

    # opcional: registrar en JSON plano
    (BASE / "photos.jsonl").write_text(json.dumps(payload) + "\n", append=True)
    return {"ok": True, "url": url}

@app.websocket("/ws/{callsign}")
async def ws_endpoint(ws: WebSocket, callsign: str):
    await ws.accept()
    _rooms.setdefault(callsign, set()).add(ws)
    try:
        while True:
            await ws.receive_text()          # keep-alive
    except WebSocketDisconnect:
        _rooms[callsign].discard(ws)
