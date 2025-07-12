import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import os
import json
import time
import requests
from datetime import datetime
from dotenv import load_dotenv
from typing import Optional        # ← compatible con Python ≤ 3.9

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from tools.eqsl_generator.eqsl_generator import generate_eqsls_from_activation


# ──────────────────────────────────────────
# Configuración general
# ──────────────────────────────────────────
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

BASE_PATH   = Path(__file__).resolve().parent.parent
DATA_DIR    = BASE_PATH / "data"
DATA_DIR.mkdir(exist_ok=True)

SESSIONS_FILE = BASE_PATH / "sessions.json"
CALLSIGNS_FILE = BASE_PATH / "callsigns.json"
CACHE_FILE     = DATA_DIR / "summits_cache.json"   # caché SOTA

CACHE_TTL = 3600   # 1 hora (s -> segundos)


# ──────────────────────────────────────────
# Utilidades JSON sencillas
# ──────────────────────────────────────────
def load_json_file(path: Path):
    if path.exists():
        with open(path) as f:
            try:
                return json.load(f)
            except Exception:
                pass
    return {}

def save_json_file(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f)


sessions  = load_json_file(SESSIONS_FILE)
callsigns = load_json_file(CALLSIGNS_FILE)
cache     = load_json_file(CACHE_FILE)


# ──────────────────────────────────────────
# Directorio de sesión (por referencia y fecha)
# ──────────────────────────────────────────
def get_session_dir(callsign: str, ref: str) -> Path:
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    dir_path = DATA_DIR / callsign / f"{ref.replace('/', '-')}_{date_str}"
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


# ──────────────────────────────────────────
# Descarga (con caché) y búsqueda de cimas
# ──────────────────────────────────────────
def _fetch_region(association: str, region: str) -> dict:
    """Descarga la lista de cimas de una región y la devuelve como dict mapeado por summitCode."""
    full_url = f"https://api2.sota.org.uk/api/regions/{association}/{region}"
    print("🔎 Consultando URL:", full_url)

    r = requests.get(full_url, timeout=10)
    print("📡 Código HTTP:", r.status_code)
    r.raise_for_status()

    data = r.json()               # estructura original
    summits = {s["summitCode"].upper(): s for s in data.get("summits", [])}
    return {
        "timestamp": time.time(),
        "summits":   summits,
    }


def get_summit_info(ref: str) -> Optional[str]:
    """
    Devuelve string con nombre y altitud de la cima
    o None si no existe. Usa caché de 1 hora.
    """
    try:
        parts = ref.strip().upper().split("/")
        if len(parts) != 2 or "-" not in parts[1]:
            return None

        association = parts[0]             # EA3
        region      = parts[1].split("-")[0]   # GI
        region_key  = f"{association}/{region}"

        # ─── Caché ──────────────────────────
        region_cache = cache.get(region_key)
        if (
            region_cache is None
            or (time.time() - region_cache.get("timestamp", 0)) > CACHE_TTL
        ):
            try:
                region_cache = _fetch_region(association, region)
                cache[region_key] = region_cache
                save_json_file(CACHE_FILE, cache)
                print("💾 Región cacheada:", region_key)
            except Exception as e:
                print("⚠️  Fallo al actualizar caché:", e)
                # si teníamos datos viejos los usamos; si no, devolvemos None
                if region_cache is None:
                    return None

        summit_dict = region_cache["summits"]
        summit = summit_dict.get(ref.upper())

        if summit:
            name = summit.get("name") or summit.get("summitName", "Unknown")
            alt  = summit.get("altM", "?")
            print("✅ Cima encontrada:", name, alt)
            return f"⛰️ {name} ({alt} m)"
        else:
            print("❌ Cima no encontrada en diccionario")
            return None

    except Exception as e:
        print("💥 Error en get_summit_info:", e)
        return None


# ──────────────────────────────────────────
# Handlers Telegram
# ──────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to SOTApics! First, register your callsign using /callsign YOURCALL.\n"
        "Then use /ref EA3/GI-002 to start uploading activation photos. Use /eqsl to generate eQSLs."
    )


async def callsign(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user    = update.effective_user
    user_id = str(user.id)
    args    = context.args

    if not args:
        await update.message.reply_text("Usage: /callsign EA3GNU")
        return

    callsigns[user_id] = args[0].upper()
    save_json_file(CALLSIGNS_FILE, callsigns)

    await update.message.reply_text(f"Callsign set: {args[0].upper()} ✅")


async def ref(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    args    = context.args

    if user_id not in callsigns:
        await update.message.reply_text("Please register your callsign first using /callsign YOURCALL.")
        return
    if not args:
        await update.message.reply_text("Usage: /ref EA3/GI-002")
        return

    sota_ref = args[0].upper()
    callsign = callsigns[user_id]
    sessions[user_id] = {"ref": sota_ref, "callsign": callsign}
    save_json_file(SESSIONS_FILE, sessions)

    summit_info = get_summit_info(sota_ref)
    if summit_info:
        reply = f"Reference set: {sota_ref} ✅ {summit_info}"
    else:
        reply = f"Error: Referencia SOTA no encontrada ❌"

    await update.message.reply_text(reply)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if user_id not in callsigns:
        await update.message.reply_text("Please register your callsign first using /callsign YOURCALL.")
        return
    if user_id not in sessions:
        await update.message.reply_text("Please start with /ref before sending photos.")
        return

    session   = sessions[user_id]
    ref       = session["ref"]
    callsign  = session["callsign"]
    dir_path  = get_session_dir(callsign, ref)

    # última foto de mayor resolución
    photo = update.message.photo[-1]
    file  = await photo.get_file()

    count = len(list(dir_path.glob("photo_*.jpg"))) + 1
    filename = dir_path / f"photo_{count}.jpg"
    await file.download_to_drive(filename)

    # dentro de handle_photo() después de guardar la imagen
    files = {"file": open(filename, "rb")}
    data  = {"callsign": callsign, "ref": ref}
    requests.post("http://127.0.0.1:8000/api/photo",
                  data=data, files=files, timeout=5)


    # caption & foto QSL
    if update.message.caption:
        with open(dir_path / "captions.txt", "a") as f:
            f.write(f"{filename.name}: {update.message.caption}\n")

        if update.message.caption.strip().lower() == "qsl":
            with open(dir_path / "qsl_photo.txt", "w") as f:
                f.write(filename.name)

    await update.message.reply_text(f"📷 Photo {count} saved.")


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    sessions.pop(user_id, None)
    save_json_file(SESSIONS_FILE, sessions)
    await update.message.reply_text("Session cancelled.")


async def eqsl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if user_id not in sessions:
        await update.message.reply_text("You must first set a reference with /ref.")
        return

    session     = sessions[user_id]
    callsign    = session["callsign"]
    sota_ref    = session["ref"].replace("/", "-")
    date_str    = datetime.utcnow().strftime("%Y-%m-%d")
    activation_path = DATA_DIR / callsign / f"{sota_ref}_{date_str}"
    output_dir      = activation_path / "eqsls"

    try:
        eqsls = generate_eqsls_from_activation(activation_path, callsign, output_dir)
        if not eqsls:
            await update.message.reply_text("No eQSLs were generated.")
            return

        await update.message.reply_text(f"📨 Generated {len(eqsls)} eQSLs:")
        for eqsl_path in eqsls:
            await update.message.reply_photo(photo=open(eqsl_path, "rb"))

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error generating eQSLs: {str(e)}")


# ──────────────────────────────────────────
# Lanzador
# ──────────────────────────────────────────
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start",    start))
    app.add_handler(CommandHandler("callsign", callsign))
    app.add_handler(CommandHandler("ref",      ref))
    app.add_handler(CommandHandler("cancel",   cancel))
    app.add_handler(CommandHandler("eqsl",     eqsl))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("SOTApics Bot is running…")
    app.run_polling()


if __name__ == "__main__":
    main()
