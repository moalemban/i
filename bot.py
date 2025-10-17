from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import platform

# ---- پیکربندی ربات ----
BOT_TOKEN = "8451634743:AAH7J4RtoICOcVqJ7VWbXZGwmjqqUtRzvRA"
WEBAPP_URL = "https://epic-calm-reports-d9f9cb01.base44.app"

# ---- دستور شروع ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.first_name

    # دکمه شیشه‌ای برای باز کردن مینی‌اپ
    inline_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("باز کردن آی‌تاب 🩵", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])

    # دکمه آبی کنار نوار تایپ برای باز کردن مستقیم وب‌اپ
    reply_keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton(باز کردن آی تاک 🩵", web_app=WebAppInfo(url=WEBAPP_URL))]],
        resize_keyboard=True
    )

    await update.message.reply_text(
        f"سلام {user_name} 👋\nبه آی‌تاک خوش اومدی.\nاز دکمه‌ی زیر برای آغاز گزارش روزانه‌ت استفاده کن:",
        reply_markup=inline_keyboard
    )

    await update.message.reply_text(
        "یا از دکمه‌ی آبی پایین برای ورود مستقیم به مینی‌اپ استفاده کن:",
        reply_markup=reply_keyboard
    )

# ---- اجرای ربات ----
if __name__ == "__main__":
    # در ویندوز گاهی نیاز به EventLoopPolicy متفاوت داریم، ولی در لینوکس Railway حذفش می‌کنیم
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
