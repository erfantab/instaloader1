from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from downloader import download_instagram_post
import os

BOT_TOKEN = "7547538867:AAHPb5mk6amBNdqAvKEHlwr9VkUnG6VL96o"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لینک پست اینستاگرام رو بده تا دانلود کنم.")

async def handle_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "instagram.com/p/" in url:
        await update.message.reply_text("⏳ در حال دریافت پست...")
        path = download_instagram_post(url)
        if path:
            if path.endswith(".mp4"):
                await update.message.reply_video(video=open(path, 'rb'))
            else:
                await update.message.reply_photo(photo=open(path, 'rb'))
            os.remove(path)
        else:
            await update.message.reply_text("❌ مشکلی در دانلود پست پیش اومد.")

async def handle_group_tag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message and context.bot.username.lower() in update.message.text.lower():
        original = update.message.reply_to_message
        if original.text and "instagram.com/p/" in original.text:
            await update.message.reply_text("⏳ در حال دریافت از اینستاگرام...")
            path = download_instagram_post(original.text)
            if path:
                if path.endswith(".mp4"):
                    await update.message.reply_video(video=open(path, 'rb'))
                else:
                    await update.message.reply_photo(photo=open(path, 'rb'))
                os.remove(path)
            else:
                await update.message.reply_text("❌ نتونستم پست رو بگیرم.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, handle_private))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_group_tag))

    print("ربات اجرا شد ✅")
    app.run_polling()

if __name__ == "__main__":
    main()
