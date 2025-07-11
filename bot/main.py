import os
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

SESSIONS_FILE = "sessions.json"
DATA_DIR = Path("data")

def load_sessions():
    if Path(SESSIONS_FILE).exists():
        with open(SESSIONS_FILE) as f:
            return json.load(f)
    return {}

def save_sessions(sessions):
    with open(SESSIONS_FILE, "w") as f:
        json.dump(sessions, f)

sessions = load_sessions()

def get_session_dir(user_id, callsign, ref):
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    dir_path = DATA_DIR / callsign / f"{ref.replace('/', '-')}_{date_str}"
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to SOTApics! Use /ref EA3/GI-002 to start uploading activation photos.")

async def ref(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args
    if not args:
        await update.message.reply_text("Usage: /ref EA3/GI-002")
        return

    sota_ref = args[0].upper()
    callsign = user.username or f"user{user.id}"
    sessions[str(user.id)] = {"ref": sota_ref, "callsign": callsign}
    save_sessions(sessions)

    await update.message.reply_text(f"Reference set: {sota_ref}. Now send me your activation photos!")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in sessions:
        await update.message.reply_text("Please start with /ref before sending photos.")
        return

    session = sessions[user_id]
    ref = session["ref"]
    callsign = session["callsign"]
    dir_path = get_session_dir(user_id, callsign, ref)

    photo = update.message.photo[-1]
    file = await photo.get_file()
    count = len(list(dir_path.glob("photo_*.jpg"))) + 1
    filename = dir_path / f"photo_{count}.jpg"
    await file.download_to_drive(filename)

    if update.message.caption:
        with open(dir_path / "captions.txt", "a") as f:
            f.write(f"{filename.name}: {update.message.caption}\n")

    await update.message.reply_text(f"📷 Photo {count} saved.")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    sessions.pop(user_id, None)
    save_sessions(sessions)
    await update.message.reply_text("Session cancelled.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ref", ref))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("SOTApics Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
