from flask import Flask, request
from telegram import Bot, Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters
import random

TOKEN = "8451634743:AAH7J4RtoICOcVqJ7VWbXZGwmjqqUtRzvRA"
MINI_APP_URL = "https://epic-calm-reports-d9f9cb01.base44.app"

app = Flask(__name__)
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, workers=4, use_context=True)

# ---------------- Handlers ----------------
async def start(update, context):
    keyboard = [[KeyboardButton("🚀 ورود به Mini App", web_app=WebAppInfo(MINI_APP_URL))]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    msg = (
        "🌤 خوش اومدی به فضای آی‌تاب!\n"
        "من بات آموزشی و مدیریتی هوشمندت هستم 💡\n"
        "همه‌چیز در حالت Calm اجرا می‌شه."
    )
    await update.message.reply_text(msg, reply_markup=markup)

async def help_cmd(update, context):
    msg = (
        "🧭 *راهنمای آی‌تاب‌بات*\n"
        "• /start — ورود و نمایش کلید Mini App\n"
        "• /about — توضیح فلسفه‌ی آی‌تاب و نقش من\n"
        "• هر پیام معمولی هم با حالت Calm جواب داده می‌شه ✨"
    )
    await update.message.reply_markdown(msg)

async def about_cmd(update, context):
    msg = (
        "🌿 درباره‌ی آی‌تاب:\n"
        "نماد خودمدیریتی و زیبایی در آموزش معلمانه.\n"
        "فرآیندهای آموزشی‌ت رو نرم و منظّم می‌کنم 💎"
    )
    await update.message.reply_text(msg)

async def echo(update, context):
    replies = [
        "✨ دریافت شد، فضای آرام حفظ شد.",
        "💎 noted در حافظه‌ی calm.",
        "📖 یادداشت ذخیره شد.",
        "🪶 حس نظم ازش اومد!",
    ]
    await update.message.reply_text(random.choice(replies))
# ---------------- Register Handlers ----------------
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_cmd))
dispatcher.add_handler(CommandHandler("about", about_cmd))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# ---------------- Webhook Routes ----------------
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_update = request.get_json(force=True)
    update = Update.de_json(json_update, bot)
    dispatcher.process_update(update)
    return "OK"

@app.route("/", methods=["GET"])
def home():
    return "🌊 AiTabBot running on Python 3.13+ — calm & stable ✅"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
