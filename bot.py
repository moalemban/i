# AiTabBot — Calm Webhook Edition 2025
# Author: Hossein Taherkenar (Tabdila / Farhangian University Kerman)
# Description: Pure Flask + Bot webhook (no Application, no Updater)
# Color theme: Calm Turquoise (#4ED1C9)

from flask import Flask, request
from telegram import Bot, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
import os
import random

# ───────────── Configuration ─────────────
TOKEN = "8451634743:AAH7J4RtoICOcVqJ7VWbXZGwmjqqUtRzvRA"    # fixed, stable bot token
MINI_APP_URL = "https://epic-calm-reports-d9f9cb01.base44.app"  # AiTab Mini App endpoint
PORT = int(os.getenv("PORT", 10000))

# ───────────── Flask App + Telegram Bot ─────────────
app = Flask(__name__)
bot = Bot(token=TOKEN)

@app.route(f"/{TOKEN}", methods=["POST"])
def receive_update():
    data = request.get_json(force=True)
    if not data or "message" not in data:
        return "ignored"

    msg = data["message"]
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")

    # ───────────── Commands ─────────────
    if text == "/start":
        keyboard = [[KeyboardButton("🚀 ورود به Mini App", web_app=WebAppInfo(MINI_APP_URL))]]
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        bot.send_message(
            chat_id=chat_id,
            text=(
                "🌤 خوش اومدی به فضای آی‌تاب!\n"
                "من بات آموزشی و مدیریتی هوشمندت هستم 💎\n"
                "همه‌چیز با حس آرامش و نظم اجرا می‌شه."
            ),
            reply_markup=markup,
        )

    elif text == "/help":
        bot.send_message(
            chat_id=chat_id,
            text=(
                "🧭 راهنمای آی‌تاب‌بات:\n"
                "• /start — ورود به Mini App\n"
                "• /about — معرفی و فلسفه آی‌تاب\n"
                "• هر پیام طبیعی با پاسخ Calm دریافت میشه ✨"
            ),
        )

    elif text == "/about":
        bot.send_message(
            chat_id=chat_id,
            text=(
                "🌿 آی‌تاب؛ زیباییِ خودمدیریتی معلمانه.\n"
                "طراحی‌شده برای فضایی منظم، آرام و هوشمند 💠"
            ),
        )

    else:
        bot.send_message(
            chat_id=chat_id,
            text=random.choice([
                "🪶 پیام دریافت شد با حس آرامش.",
                "📖 noted در سیستم Calm.",
                "✨ حفظ شد در دفتر آی‌تاب.",
                "💎 نظمش حس شد!"
            ]),
        )

    return "OK"

@app.route("/", methods=["GET"])
def home():
    return "🌊 AiTabBot Pure Webhook is running — Calm & Stable."

if __name__ == "__main__":
    print("✅ AiTabBot started successfully — Flask webhook mode")
    app.run(host="0.0.0.0", port=PORT)
