# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import os
import requests
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from Audify import app

def download_website(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return f"⚠️ Failed to download source code. Status code: {response.status_code}"
    except Exception as e:
        return f"❌ An error occurred: {str(e)}"

@app.on_message(filters.command("webdl"))
async def web_download(client, message: Message):
    if len(message.command) == 1:
        return await message.reply_text(
            "❗ Please enter a URL after the /webdl command.\n\nExample: `/webdl https://example.com`"
        )

    url = message.command[1]
    source_code = download_website(url)

    if source_code.startswith("❌") or source_code.startswith("⚠️"):
        return await message.reply_text(source_code)

    file_path = "website.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(source_code)

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("❌ Close", callback_data="close")]]
    )

    await message.reply_document(
        document=file_path,
        caption=f"🧾 Source code of: {url}",
        reply_markup=keyboard,
    )

    os.remove(file_path)
