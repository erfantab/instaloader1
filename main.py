import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import instaloader

TOKEN = "7547538867:AAHPb5mk6amBNdqAvKEHlwr9VkUnG6VL96o"  # توکن شما
PORT = 8443  # پورت استاندارد وبهوک
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # اینو تو رندر به صورت متغیر محیطی ست کن، مثل: https://yourservice.onrender.com/7547538867:AAHPb5mk6amBNdqAvKEHlwr9VkUnG6VL96o

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من بات دانلودر اینستاگرام هستم.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text and "instagram.com" in text:
        # اینجا میتونی دانلود ویدیو رو با instaloader پیاده کنی (برای ساده‌سازی الان فقط پیام می‌فرستیم)
        await update.message.reply_text("در حال دانلود پست اینستا... (الان دانلود پیاده نشده)")
    else:
        await update.message.reply_text("لطفا لینک اینستاگرام بفرستید.")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
