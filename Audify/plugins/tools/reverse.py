# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import os
import time
import httpx
from uuid import uuid4
from typing import BinaryIO, Dict, List
from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from Audify import app

SAUCENAO_API_KEY = "27ab8b6f0a9e67ce164e67dcbecc45a362b538ef"
SAUCENAO_API = "https://saucenao.com/search.php"

class STRINGS:
    REPLY_TO_MEDIA = "🔍 Please reply to an image or document to reverse search."
    UNSUPPORTED_MEDIA_TYPE = "⚠️ Unsupported media type. Use a photo, sticker, or file."
    DOWNLOADING_MEDIA = "⏳ Downloading media..."
    UPLOADING_TO_API_SERVER = "📡 Uploading to SauceNao..."
    PARSING_RESULT = "🧠 Parsing results..."
    EXCEPTION_OCCURRED = "❌ An error occurred:\n\n`{}`"
    RESULT = """
🔎 <b>Similarity:</b> <code>{similarity}%</code>
🖼️ <b>Title:</b> <code>{title}</code>
🔗 <b>Link:</b> <a href="{url}">Source</a>
⏱️ <b>Time:</b> <code>{time_taken}</code> sec"""
    OPEN_PAGE = "🔗 Open Source"
    CLOSE = "✖ Close"

@app.on_message(filters.command(["reverse", "sauce", "pp"]))
async def reverse_image_search(app: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply(STRINGS.REPLY_TO_MEDIA)

    if message.reply_to_message.media not in (
        MessageMediaType.PHOTO,
        MessageMediaType.STICKER,
        MessageMediaType.DOCUMENT,
    ):
        return await message.reply(STRINGS.UNSUPPORTED_MEDIA_TYPE)

    start_time = time.time()
    status = await message.reply(STRINGS.DOWNLOADING_MEDIA)

    file_path = f"temp_download/{uuid4()}.jpg"
    try:
        await message.reply_to_message.download(file_path)
    except Exception as exc:
        await status.delete()
        return await message.reply(STRINGS.EXCEPTION_OCCURRED.format(str(exc)))

    await status.edit(STRINGS.UPLOADING_TO_API_SERVER)
    try:
        with open(file_path, "rb") as img:
            files = {"file": img}
            data = {"output_type": 2, "api_key": SAUCENAO_API_KEY}
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(SAUCENAO_API, data=data, files=files)

        os.remove(file_path)
        result = response.json()
    except Exception as exc:
        await status.delete()
        return await message.reply(STRINGS.EXCEPTION_OCCURRED.format(str(exc)))

    try:
        best = result["results"][0]
        header = best["header"]
        data = best["data"]

        similarity = header.get("similarity", "N/A")
        title = data.get("title") or data.get("material") or "Unknown"
        ext_urls = data.get("ext_urls", ["https://saucenao.com"])[0]

        end_time = time.time()
        time_taken = "{:.2f}".format(end_time - start_time)

        text = STRINGS.RESULT.format(
            similarity=similarity,
            title=title,
            url=ext_urls,
            time_taken=time_taken
        )
        buttons = [
            [InlineKeyboardButton(STRINGS.OPEN_PAGE, url=ext_urls)],
            [InlineKeyboardButton(STRINGS.CLOSE, callback_data="close")]
        ]
        await message.reply(text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
        await status.delete()
    except Exception as exc:
        await status.delete()
        return await message.reply(STRINGS.EXCEPTION_OCCURRED.format(str(exc)))
