# ---------------------------------------------------------
# Alphabot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Alphabot project.
# Unauthorized copying, distribution, or use is prohibited.
# Developed by @devforgekush. All rights reserved.
# ---------------------------------------------------------

import re
import aiohttp
from bs4 import BeautifulSoup
from pyrogram import filters
from pyrogram.types import Message
from Audify import app

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# ---------------------------------------------------------
# Helper: TextPro Scraper (No API Key Required)
async def textpro_logo(theme_url: str, text: str) -> str:
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(theme_url) as resp:
            html = await resp.text()

        soup = BeautifulSoup(html, "html.parser")
        token = soup.find("input", {"name": "token"})["value"]

        data = {
            "text[]": text,
            "submit": "Go",
            "token": token
        }

        async with session.post(theme_url, data=data) as post_resp:
            post_html = await post_resp.text()

        match = re.search(r"(https:\/\/textpro\.me\/output\/[^\"]+)", post_html)
        if not match:
            raise Exception("Logo generation failed")
        return match.group(1)

# ---------------------------------------------------------
# Default Logo - /logo
@app.on_message(filters.command("logo") & filters.text)
async def logo_cmd(_, message: Message):
    if len(message.command) < 2:
    return await message.reply("⚠️ Send text like: `/logo Alphabot`")

    text = " ".join(message.command[1:])
    msg = await message.reply("🎨 Generating logo...")

    try:
        url = await textpro_logo("https://textpro.me/neon-light-text-effect-online-882.html", text)
        await msg.delete()
        await message.reply_photo(url, caption=f"🖌️ Logo for `{text}`")
    except Exception as e:
        await msg.edit(f"❌ Logo generation failed!\n`{e}`")

# ---------------------------------------------------------
# Custom Logo - /clogo
@app.on_message(filters.command("clogo") & filters.text)
async def clogo_cmd(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("⚠️ Send text like: `/clogo Custom Style`")

    text = " ".join(message.command[1:])
    msg = await message.reply("🎨 Generating custom logo...")

    try:
        url = await textpro_logo("https://textpro.me/create-3d-glue-text-effect-with-realistic-style-986.html", text)
        await msg.delete()
        await message.reply_photo(url, caption=f"🎨 Custom Logo for `{text}`")
    except Exception as e:
        await msg.edit(f"❌ Logo generation failed!\n`{e}`")

# ---------------------------------------------------------
# Black-Pink Logo - /blogo
@app.on_message(filters.command("blogo") & filters.text)
async def blogo_cmd(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("⚠️ Send text like: `/blogo Blink Style`")

    text = " ".join(message.command[1:])
    msg = await message.reply("🖤 Generating black-pink logo...")

    try:
        url = await textpro_logo("https://textpro.me/create-blackpink-logo-style-online-1001.html", text)
        await msg.delete()
        await message.reply_photo(url, caption=f"🖤 BlackPink Logo for `{text}`")
    except Exception as e:
        await msg.edit(f"❌ Logo generation failed!\n`{e}`")
