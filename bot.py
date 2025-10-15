from flask import Flask, request
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import telegram.ext

# --- PATCH ناسازگاری پایتون ۳.۱۳ با کلاس Updater در PTB v20.6 ---
try:
    UpdaterClass = getattr(telegram.ext, "Updater", None)
    if UpdaterClass and not hasattr(UpdaterClass, "_Updater__polling_cleanup_cb"):
        setattr(UpdaterClass, "_Updater__polling_cleanup_cb", None)
        print("✅ Patch for Python 3.13 applied successfully")
except Exception as e:
    print("⚠️ Patch not applied:", e)

# ------------------------------------------------------------------

TOKEN = os.getenv("BOT_TOKEN")
MINI_APP_URL = "https://epic-calm-reports-d9f9cb01.base44.app"

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()


# ---- HANDLERS ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("🔹 باز کردن Mini App", web_app=WebAppInfo(MINI_APP_URL))]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("سلام 👋 من آی‌تاب‌بات هستم.\nروی دکمه پایین کلیک کن:", reply_markup=markup)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"پیام دریافت شد: {update.message.text}")


application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


# ---- FLASK WEBHOOK ----
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    if update:
        application.update_queue.put(update)
    return "OK"

@app.route("/", methods=["GET"])
def index():
    return "AiTabBot Webhook Active ✅"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
