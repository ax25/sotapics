# SOTApics 📡🏔️

SOTApics is an **all‑in‑one workflow** for SOTA (Summits on the Air) activators:

* **Telegram Bot** (Python) – collects photos, generates eQSLs and publishes them instantly.
* **React Front‑end** (Vite) – shows your profile, photo feed and activation cards in real time.
* **Self‑hosted server** (Raspberry Pi) – stores media locally and serves the web UI; no external services required.

---

## 1 · Features

| Module | Description |
|--------|-------------|
| **bot/** | `main.py` – Telegram bot.<br>• Commands `/callsign`, `/ref`, `/eqsl`, `/cancel`.<br>• Photo upload (`qsl` caption ⇒ QSL photo, `profile` caption ⇒ avatar).<br>• Queries the SOTA API with a 1 h cache. |
| **tools/eqsl_generator/** | Creates eQSL PDF/PNG files from activation data and photos. |
| **frontend/** | Vite + React app. Compact activation cards with photo carousel, points, QSO count, etc. |
| **data/** | Folder structure `data/<CALL>/<REF>_YYYY‑MM‑DD/` (photos, captions, eQSLs…). |
| **.github/** | (Optional) CI workflows for linting and building. |

---

## 2 · Architecture

```text
Raspberry Pi
├── bot/          (Python 3.10 virtualenv)
│   └── main.py   ← Telegram polling/webhook
├── frontend/     (Node 18+)
│   ├── src/
│   └── dist/     ← static build served by Apache/Nginx
└── data/         ← local media & generated eQSLs
```

The bot writes photos straight into `data/`; the front‑end reads them (dev) or Apache serves them after `npm run build` (prod).

---

## 3 · Quick Setup

```bash
# 1 – Clone
git clone https://github.com/ax25/sotapics.git
cd sotapics

# 2 – Backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3 – Front‑end
cd frontend
npm install        # installs Vite & deps
cd ..

# 4 – Environment variables
cp .env.example .env   # NEVER commit your real .env
nano .env              # BOT_TOKEN=<YOUR_TELEGRAM_BOT_TOKEN>

# 5 – Run
python bot/main.py          # Telegram bot
cd frontend && npm run dev  # React dev server (http://localhost:5173)
```

**Production build**

```bash
cd frontend
npm run build               # generates /dist
# Copy or symlink dist/ to /var/www/html/sotapics (Apache/Nginx)
```

---

## 4 · Bot Commands

| Command | Example | Effect |
|---------|---------|--------|
| `/start` | – | Quick help |
| `/callsign EA3GNU` | | Registers your callsign |
| `/ref EA3/GI‑002` | | Starts an activation session |
| *send photo* | optional caption | Saves the photo; caption **qsl** ⇒ marks QSL photo, caption **profile** ⇒ updates avatar |
| `/eqsl` | | Generates and returns eQSLs |
| `/cancel` | | Ends current session |

---

## 5 · Environment Variables & Secrets

| Variable | Purpose |
|----------|---------|
| `BOT_TOKEN` | Telegram Bot token |

`.gitignore` already excludes `.env`, `venv/`, `frontend/node_modules/`, etc.

---

## 6 · SOTA API Cache (TTL 1 h)

`get_summit_info()` fetches summit data from `https://api2.sota.org.uk` and stores it in `data/sota_cache.json` for one hour.  
If a reference is not found the bot replies **“Error: SOTA reference not found”**.

---

## 7 · Contributing

1. Fork & `git clone`  
2. Create a feature branch: `git checkout -b feat/my-improvement`  
3. Make sure `pytest` and `npm test` pass  
4. Open a pull request

---

## 8 · License

MIT © 2025 [ax25](https://github.com/ax25) – Happy SOTA activating! 🏞️📻
