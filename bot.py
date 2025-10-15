from flask import Flask, request
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import random, asyncio

TOKEN = "8451634743:AAH7J4RtoICOcVqJ7VWbXZGwmjqqUtRzvRA"
MINI_APP_URL = "https://epic-calm-reports-d9f9cb01.base44.app"

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

# ---------- Handlers ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("🚀 ورود به Mini App", web_app=WebAppInfo(MINI_APP_URL))]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    msg = (
        "🌤 خوش اومدی به فضای آی‌تاب!\n"
        "من بات آموزشی و مدیریتی هوشمندت هستم 💡\n"
        "همه‌چیز در حالت Calm اجرا می‌شه."
    )
    await update.message.reply_text(msg, reply_markup=markup)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🧭 *راهنمای آی‌تاب‌بات*\n"
        "• /start — ورود و نمایش کلید Mini App\n"
        "• /about — توضیح فلسفه‌ی آی‌تاب و نقش من\n"
        "• هر پیام معمولی هم با حالت Calm جواب داده می‌شه ✨"
    )
    await update.message.reply_markdown(msg)

async def about_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🌿 درباره‌ی آی‌تاب:\n"
        "نماد خودمدیریتی و زیبایی در آموزش معلمانه.\n"
        "فرآیندهای آموزشی‌ت رو نرم و منظّم می‌کنم 💎"
    )
    await update.message.reply_text(msg)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    replies = [
        "✨ دریافت شد، فضای آرام حفظ شد.",
        "💎 noted در حافظه‌ی calm.",
        "📖 یادداشت ذخیره شد.",
        "🪶 حس نظم ازش اومد!",
    ]
    await update.message.reply_text(random.choice(replies))

# ---------- Register ----------
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_cmd))
application.add_handler(CommandHandler("about", about_cmd))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# ---------- Webhook Routes ----------
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    asyncio.run(application.process_update(update))
    return "OK"

@app.route("/", methods=["GET"])
def root():
    return "🌊 AiTabBot Flask Webhook — Python 3.13 compatible ✅"

if __name__ == "__main__":
    print("✅ AiTabBot starting with pure Flask webhook — no Updater, no Dispatcher")
    app.run(host="0.0.0.0", port=10000)
