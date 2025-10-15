from flask import Flask, request
from telegram import Update, Bot, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio, random

TOKEN = "8451634743:AAH7J4RtoICOcVqJ7VWbXZGwmjqqUtRzvRA"
MINI_APP_URL = "https://epic-calm-reports-d9f9cb01.base44.app"
PORT = 10000

app = Flask(__name__)

# مرحله ساخت: Application ساخته می‌شود ولی Updater فوراً خنثی می‌گردد
application = Application.builder().token(TOKEN).build()
application.updater = None  # 💣 حذف Updater که در build ساخته شده
application.job_queue = None
application._running = True  # اجازه اجرای مستقیم بدون start()

# ---------- Handlers ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[KeyboardButton("🚀 ورود به Mini App", web_app=WebAppInfo(MINI_APP_URL))]]
    markup = ReplyKeyboardMarkup(kb, resize_keyboard=True)
    await update.message.reply_text(
        "🌤 خوش اومدی به فضای آی‌تاب!\n"
        "من بات آموزشی و مدیریتی هوشمندت هستم 💡\n"
        "همه چیز در حالت Calm اجرا می‌شه.",
        reply_markup=markup,
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🧭 *راهنمای آی‌تاب‌بات*\n"
        "• /start — ورود و نمایش کلید Mini App\n"
        "• /about — فلسفه آی‌تاب\n"
        "• هر پیام معمولی هم با حالت Calm جواب داده می‌شه ✨"
    )
    await update.message.reply_markdown(msg)

async def about_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌿 آی‌تاب: نماد خودمدیریتی و زیبایی در آموزش معلمانه.\n"
        "من فرآیندهای آموزشی‌ت رو نرم و آرام می‌کنم 💎"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice([
        "✨ دریافت شد، فضای آرام حفظ شد.",
        "💎 noted در حافظه‌ی Calm.",
        "📖 یادداشت ذخیره شد.",
        "🪶 حس نظم ازش اومد!",
    ]))

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_cmd))
application.add_handler(CommandHandler("about", about_cmd))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# ---------- Webhook ----------
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    asyncio.run(application.process_update(update))
    return "OK"

@app.route("/", methods=["GET"])
def home():
    return "🌊 AiTabBot Webhook-only — Python 3.13 stable ✅"

if __name__ == "__main__":
    print("✅ AiTabBot running with patched Application (no Updater init)")
    app.run(host="0.0.0.0", port=PORT)
