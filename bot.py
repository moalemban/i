from flask import Flask, request
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import telegram.ext.updater

# --- PATCH ناسازگاری پایتون ۳.۱۳ با python-telegram-bot v20.6 ---
# این خط جلوی AttributeError مربوط به Updater را می‌گیرد
try:
    if not hasattr(telegram.ext.updater.Updater, "_Updater__polling_cleanup_cb"):
        telegram.ext.updater.Updater._Updater__polling_cleanup_cb = None
except Exception as e:
    print("Patch Updater applied:", e)

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
