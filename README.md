# 📡 SOTApics

**SOTApics** is a lightweight system for Summits on the Air (SOTA) activators to create an embeddable HTML widget that showcases their latest activations with summit data, photos, and personal notes.

Ideal for embedding in QRZ pages, club websites, or personal blogs.

---

## 🧭 Overview

SOTApics combines:

- ✅ Official SOTA activation logs (via the SOTA API)
- 📷 User-submitted photos and captions via Telegram
- 💡 A responsive iframe widget for easy embedding

---

## ⚙️ How it Works

1. **Activate normally** and upload your log to the [SOTA Database](https://www.sotadata.org.uk).
2. **Send `/ref` and your photos** to the `@SOTApicsBot` on Telegram:

   ```
   /ref EA3/GI-002
   [send photos]
   ```

3. The system links your photos and comments with the activation metadata.
4. Embed your public widget using an iframe like this:

   ```html
   <iframe src="https://sotapics.example.net/widget/EA3ABC" width="100%" height="300" frameborder="0"></iframe>
   ```

---

## 🔧 Project Structure

```
sotapics/
├── bot/           # Telegram bot (photo upload and ref commands)
├── api/           # Backend API (FastAPI, serves JSON + HTML)
├── widget/        # Static frontend (JS/HTML iframe widget)
├── data/          # Photo and session storage (ignored in git)
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 📦 Installation

### Requirements

- Python 3.11+
- Docker & Docker Compose (optional but recommended)
- A Telegram bot token ([create one](https://t.me/BotFather))

### Run locally

```bash
git clone https://github.com/ax25/sotapics.git
cd sotapics
cp .env.example .env
# Edit your Telegram token inside .env
cd bot
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

## 🚀 Deployment

SOTApics is designed to run smoothly on a Raspberry Pi, small VPS, or even local server.

Use the included `docker-compose.yml` to deploy the full stack:
- Telegram bot
- API backend
- Static photo serving
- Reverse proxy with HTTPS (e.g. Caddy or nginx)

---

## 🛠 Roadmap

- [x] Receive `/ref` and photos via Telegram
- [x] Store activation metadata and media locally
- [ ] Generate JSON for latest activation per callsign
- [ ] Render HTML iframe widget
- [ ] Support captions, summit info, and QSO stats
- [ ] Cloud-based storage (optional)

---

## 🤝 Contributing

Contributions welcome! Whether you're a SOTA activator, a radio club developer, or just curious, feel free to open issues, fork, or suggest features.

---

## 📜 License

MIT License © 2025 [Alberto Padilla]

---

## 📬 Contact

Questions? Suggestions? Reach me via [@SOTApicsBot](https://t.me/SOTApicsBot) on Telegram or open an issue here.
