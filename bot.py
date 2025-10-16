# AiTabBot — Calm Webhook Edition 2025 (Revised)
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
# Bot instance is now globally available
bot = Bot(token=TOKEN) 

@app.route(f"/{TOKEN}", methods=["POST"])
def receive_update():
    # Safely get the JSON data from the request body
    try:
        data = request.get_json(force=True)
    except Exception:
        # If request body is not valid JSON, ignore
        return "ignored (invalid json)"

    # Safely get the message object from the update
    # Note: Telegram updates can be 'message', 'edited_message', 'callback_query', etc.
    msg = data.get("message")

    # If the update is not a standard message, gracefully ignore it
    if not msg:
        return "ignored (no message)"
    
    # Extract necessary information securely
    try:
        chat_id = msg["chat"]["id"]
        text = msg.get("text", "") # .get ensures that if 'text' key is missing, it defaults to ""
    except KeyError:
        # This handles cases where chat_id might be missing (highly unlikely for messages)
        return "ignored (missing chat info)"

    # ───────────── Commands ─────────────
    if text == "/start":
        keyboard = [[KeyboardButton("🚀 ورود به Mini App", web_app=WebAppInfo(MINI_APP_URL))]]
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        # Using bot.send_message
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

    # ───────────── General Text Response ─────────────
    elif text: # Only respond if the message has actual text
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
    # The default host for Railway/production environments should be '0.0.0.0'
    app.run(host="0.0.0.0", port=PORT)
