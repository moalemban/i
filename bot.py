from flask import Flask, request
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import telegram.ext
import random

# --- Custom Updater Patch Class ---
try:
    from telegram.ext import Updater as OriginalUpdater
    class PatchedUpdater(OriginalUpdater):
        def __init__(self, *args, **kwargs):
            # bypass problematic __polling_cleanup_cb assignment
            super().__init__(*args, **kwargs)
            # manually add safe placeholder (non-private)
            self.polling_cleanup_cb = None
    telegram.ext.Updater = PatchedUpdater
    print("✅ Deep Patch applied: Updater replaced with PatchedUpdater for Python ≥3.13")
except Exception as e:
    print("⚠️ Updater patch failed:", e)
# -----------------------------------------------------------

TOKEN = "8451634743:AAH7J4RtoICOcVqJ7VWbXZGwmjqqUtRzvRA"
MINI_APP_URL = "https://epic-calm-reports-d9f9cb01.base44.app"

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

# =============== AiTab Handlers ===============
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🌤 خوش اومدی به فضای آی‌تاب!\n"
        "من بات آموزشی و مدیریتی هوشمندت هستم 💡\n"
        "همه چی در حالت Calm اجرا می‌شه."
    )
    keyboard = [[KeyboardButton("🚀 ورود به Mini App", web_app=WebAppInfo(MINI_APP_URL))]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(msg, reply_markup=markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🧠 *راهنمای آی‌تاب‌بات*\n"
        "• /start ‑ ورود و نمایش کلید Mini App\n"
        "• /about ‑ توضیح فلسفه‌ی آی‌تاب و نقش من\n"
        "• هر پیام عادی هم با حالت Calm پاسخ داده می‌شه ✨"
    )
    await update.message.reply_markdown(text)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🌿 درباره‌ی آی‌تاب:\n"
        "آی‌تاب نمادی از خودمدیریتی و زیبایی در آموزش معلمانه‌ست.\n"
        "من طراحی شدم تا فرآیندهای آموزشی و گزارش‌گیریت رو نرم، سریع و شفاف کنم 💎"
    )
    await update.message.reply_text(text)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    replies = [
        "⚡ پیام عالی، حس نظم ازش میاد!",
        "🍃 دریافت شد، فضای آرام حفظ شد.",
        "💎 یادداشت ذخیره شد در حافظه‌ی calm.",
        "📖 چه جالب، الهام‌گیرنده بود!",
        "🪶 registered — ذهنم روشن‌تر شد!"
    ]
    await update.message.reply_text(random.choice(replies))

# register handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("about", about_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# =============== Webhook Flask ===============
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    if update:
        application.update_queue.put(update)
    return "OK"

@app.route("/", methods=["GET"])
def root():
    return "🌊 AiTabBot Python 3.13‑compatible — Calm mode running ✅"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
