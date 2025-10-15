from flask import Flask, request
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import telegram.ext.updater

# Patch برای دور زدن خطای AttributeError در پایتون 3.13
if not hasattr(telegram.ext.updater.Updater, "_Updater__polling_cleanup_cb"):
    telegram.ext.updater.Updater._Updater__polling_cleanup_cb = None

# -----------------------------
TOKEN = os.getenv("BOT_TOKEN")
MINI_APP_URL = "https://epic-calm-reports-d9f9cb01.base44.app"

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()


# ======= COMMAND HANDLERS =======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("🔹 باز کردن Mini App", web_app=WebAppInfo(MINI_APP_URL))]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("سلام 👋 من آی‌تاب‌بات هستم.\nروی دکمه پایین کلیک کن:", reply_markup=reply_markup)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"پیام دریافت شد: {update.message.text}")


application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


# ======= WEBHOOK / FLASK ROUTES =======
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "OK"

@app.route("/", methods=["GET"])
def index():
    return "AiTabBot Webhook Active ✅"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
