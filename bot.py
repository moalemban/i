from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from flask import Flask, request
from dotenv import load_dotenv
import os

# بارگذاری .env برای Railway یا توسعه محلی
load_dotenv()
TOKEN = os.getenv("TOKEN")

app_flask = Flask(__name__)  # برای تست محلی (Webhook یا health check)

@app_flask.route("/")
def home():
    return "AiTab Railway Bot Running 🩵"

# تابع اصلی برای فرمان /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    webapp_url = "https://epic-calm-reports-d9f9cb01.base44.app"

    # دکمه دائمی کنار کادر تایپ
    reply_keyboard = [[KeyboardButton("باز کردن آی‌تاب 🩵", web_app={"url": webapp_url})]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    # دکمه درون‌پیامی (Inline)
    inline_button = InlineKeyboardButton("ورود به آی‌تاب 🩵", web_app={"url": webapp_url})
    inline_markup = InlineKeyboardMarkup([[inline_button]])

    await update.message.reply_text("خوش آمدی به آی‌تاب 🎯", reply_markup=markup)
    await update.message.reply_text("برای ورود به اپ هوشمند، روی دکمه‌ی زیر بزن:", reply_markup=inline_markup)

# ساخت اپلیکیشن ربات
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

# اجرای مستقیم به‌صورت polling (برای تست یا Railway بدون SSL)
if __name__ == "__main__":
    print("Bot starting... 🧠")
    app.run_polling()
