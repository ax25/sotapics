
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from tools.eqsl_generator.eqsl_generator import generate_eqsls_from_activation

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_PATH / "data"
SESSIONS_FILE = BASE_PATH / "sessions.json"
CALLSIGNS_FILE = BASE_PATH / "callsigns.json"

def load_json_file(path):
    if Path(path).exists():
        with open(path) as f:
            return json.load(f)
    return {}

def save_json_file(path, data):
    with open(path, "w") as f:
        json.dump(data, f)

sessions = load_json_file(SESSIONS_FILE)
callsigns = load_json_file(CALLSIGNS_FILE)

def get_session_dir(callsign, ref):
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    dir_path = DATA_DIR / callsign / f"{ref.replace("/", "-")}_{date_str}"
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path

def get_summit_info(ref):
    try:
        parts = ref.strip().upper().split("/")
        if len(parts) != 2 or "-" not in parts[1]:
            return None

        association = parts[0]
        region = parts[1].split("-")[0]
        full_url = f"https://api2.sota.org.uk/api/regions/{association}/{region}"
        print("🔎 Consultando URL:", full_url)

        response = requests.get(full_url, timeout=10)
        print("📡 Código HTTP:", response.status_code)

        if response.status_code != 200:
            return None

        summits = response.json()
        summit = summits.get(ref.upper())

        if summit:
            name = summit.get("summitName", "Unknown")
            alt = summit.get("altM", "?")
            print("✅ Cima encontrada:", name, alt)
            return f"⛰️ {name} ({alt} m)"
        else:
            print("❌ Cima no encontrada en diccionario")
    except Exception as e:
        print("💥 Error en get_summit_info:", e)
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to SOTApics! First, register your callsign using /callsign YOURCALL.\n"
        "Then use /ref EA3/GI-002 to start uploading activation photos. Use /eqsl to generate eQSLs."
    )

async def callsign(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    args = context.args

    if not args:
        await update.message.reply_text("Usage: /callsign EA3GNU")
        return

    callsigns[user_id] = args[0].upper()
    save_json_file(CALLSIGNS_FILE, callsigns)

    await update.message.reply_text(f"Callsign set: {args[0].upper()} ✅")

async def ref(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    args = context.args

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
        reply = f"Reference set: {sota_ref} ✅"

    await update.message.reply_text(reply)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if user_id not in callsigns:
        await update.message.reply_text("Please register your callsign first using /callsign YOURCALL.")
        return

    if user_id not in sessions:
        await update.message.reply_text("Please start with /ref before sending photos.")
        return

    session = sessions[user_id]
    ref = session["ref"]
    callsign = session["callsign"]
    dir_path = get_session_dir(callsign, ref)

    photo = update.message.photo[-1]
    file = await photo.get_file()
    count = len(list(dir_path.glob("photo_*.jpg"))) + 1
    filename = dir_path / f"photo_{count}.jpg"
    await file.download_to_drive(filename)

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

    session = sessions[user_id]
    callsign = session["callsign"]
    sota_ref = session["ref"].replace("/", "-")
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    activation_path = DATA_DIR / callsign / f"{sota_ref}_{date_str}"
    output_dir = activation_path / "eqsls"

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

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("callsign", callsign))
    app.add_handler(CommandHandler("ref", ref))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(CommandHandler("eqsl", eqsl))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("SOTApics Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
