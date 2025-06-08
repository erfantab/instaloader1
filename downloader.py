import instaloader
import os
import re
import uuid

DOWNLOAD_DIR = "downloads"

# ایجاد پوشه اگر وجود نداشت
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_instagram_post(url: str):
    shortcode_match = re.search(r"instagram\.com/p/([a-zA-Z0-9_-]+)", url)
    if not shortcode_match:
        return None

    shortcode = shortcode_match.group(1)
    filename = f"download_{uuid.uuid4().hex[:8]}"

    loader = instaloader.Instaloader(
        download_videos=True,
        download_video_thumbnails=False,
        save_metadata=False,
        download_comments=False,
        post_metadata_txt_pattern='',
        filename_pattern=filename
    )

    try:
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, target=DOWNLOAD_DIR)

        for ext in ['.mp4', '.jpg']:
            file_path = os.path.join(DOWNLOAD_DIR, f"{filename}{ext}")
            if os.path.exists(file_path):
                return file_path
    except Exception as e:
        print(f"Download error: {e}")
    return None
