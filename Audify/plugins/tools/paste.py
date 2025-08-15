# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import os
import re
import aiofiles
from aiohttp import ClientSession
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from Audify import app

# ─── Session and Post ─── #
aiohttpsession = ClientSession()


async def post(url: str, *args, **kwargs):
    async with aiohttpsession.post(url, *args, **kwargs) as resp:
        text = await resp.text()
        try:
            return await resp.json()
        except Exception:
            raise Exception(f"BatBin error: {resp.status} | Response: {text}")


# ─── BatBin Pasting ─── #
async def batbin(text: str) -> str:
    resp = await post("https://batbin.me/api/v2/paste", data=text)
    if "message" not in resp:
        raise Exception(f"BatBin failed: {resp}")
    return f"https://batbin.me/{resp['message']}"


# ─── File Type Pattern ─── #
TEXT_TYPES_PATTERN = re.compile(r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$")


# ─── /paste Handler ─── #
@app.on_message(filters.command("paste"))
async def paste_func(_, message: Message):
    reply = message.reply_to_message
    input_text = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else None

    if not reply and not input_text:
        return await message.reply("❗ **Please reply to a message or provide text with** `/paste <your text>`.")

    m = await message.reply_text("📤 **Pasting content... please wait a moment.**")

    try:
        if input_text:
            content = input_text

        elif reply.text:
            content = reply.text

        elif reply.document:
            doc = reply.document
            if doc.file_size > 1_000_000:
                return await m.edit("⚠️ **File too large. Only under 1MB allowed.**")
            if not TEXT_TYPES_PATTERN.search(doc.mime_type):
                return await m.edit("❌ **Only code or text-based files are allowed.**")
            file_path = await reply.download()
            async with aiofiles.open(file_path, mode="r") as f:
                content = await f.read()
            os.remove(file_path)
        else:
            return await m.edit("⚠️ **Only text messages or supported documents are allowed.**")

        link = await batbin(content)

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔗 View Paste", url=link)],
            [InlineKeyboardButton("✖️ Close", callback_data="close")]
        ])

        await m.edit(f"✅ **Your paste has been uploaded to [BatBin]({link})**", reply_markup=buttons)

    except Exception as e:
        await m.edit(f"❌ **Failed to paste:**\n`{e}`")
