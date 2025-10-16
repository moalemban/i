# ------------------------------
# AiTabBot — Minimal Telegram Bot (Polling Mode)
# Author: Hossein Taherkenar
# ------------------------------

from telegram import (
    Update,
    WebAppInfo,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
import asyncio

BOT_TOKEN = "8451634743:AAH7J4RtoICOcVqJ7VWbXZGwmjqqUtRzvRA"
AITAB_URL = "https://epic-calm-reports-d9f9cb01.base44.app"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or user.username or "کاربر"

    reply_keyboard = [
        [KeyboardButton("🩵 باز کردن آی‌تاب", web_app=WebAppInfo(url=AITAB_URL))]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    text = (
        f"👋 سلام {name}!\n"
        "به آی‌تاب خوش آمدی 💎\n\n"
        "روی دکمه آبی کنار نوار تایپ یا دکمه‌ی زیر بزن تا فرم گزارش‌کار روزانه باز شود."
    )
    await update.message.reply_text(text, reply_markup=markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📘 راهنمای ربات آی‌تاب:\n"
        "۱. دستور /start را بزن تا دکمه‌ی وب‌اپ فعال شود.\n"
        "۲. روی دکمه‌ی آبی کنار نوار تایپ بزن تا فرم باز شود.\n"
        "۳. اجرای ربات به‌صورت لوکال (polling)."
    )


if __name__ == "__main__":
    # ⚙️ اصلاح حلقه رویدادها برای ویندوز
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    print("✅ AiTabBot در حالت Polling اجرا شد ...")
    app.run_polling()
