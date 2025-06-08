import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
import instaloader
import tempfile
import re

BOT_TOKEN = "7547538867:AAHPb5mk6amBNdqAvKEHlwr9VkUnG6VL96o"
PORT = int(os.environ.get("PORT", "8080"))
WEBHOOK_URL = "https://your-render-service.onrender.com"  # حتما آدرس واقعی رو بذار

logging.basicConfig(level=logging.INFO)
loader = instaloader.Instaloader(save_metadata=False, post_metadata_txt_pattern='')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لینک پست اینستاگرام رو بفرست تا برات دانلود کنم.")

def extract_shortcode(url: str):
    match = re.search(r"instagram\.com\/(p|reel|tv)\/([a-zA-Z0-9_-]+)", url)
    return match.group(2) if match else None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    shortcode = extract_shortcode(text)

    if not shortcode:
        await update.message.reply_text("لطفاً لینک معتبر اینستاگرام بفرست.")
        return

    await update.message.reply_text("درحال دانلود... ⏳")

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            loader.dirname_pattern = tmpdir
            post = instaloader.Post.from_shortcode(loader.context, shortcode)
            loader.download_post(post, target="downloaded")

            for file in os.listdir(tmpdir + "/downloaded"):
                if file.endswith((".mp4", ".jpg", ".jpeg", ".png")):
                    filepath = os.path.join(tmpdir, "downloaded", file)
                    with open(filepath, "rb") as f:
                        if file.endswith(".mp4"):
                            await update.message.reply_video(video=f)
                        else:
                            await update.message.reply_photo(photo=f)
                    break
    except Exception as e:
        logging.error(e)
        await update.message.reply_text("خطا در دانلود. مطمئن شو لینک درسته یا عمومی باشه.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}"
    )
