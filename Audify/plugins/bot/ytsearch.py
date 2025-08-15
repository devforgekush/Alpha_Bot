# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import logging
from pyrogram import filters
from pyrogram.types import Message
from youtube_search import YoutubeSearch

from Audify import app
from config import BOT_USERNAME


@app.on_message(filters.command("search"))
async def ytsearch(_, message: Message):
    try:
        if len(message.command) < 2:
            return await message.reply_text("❗️ Please provide a search term.\n\n**Usage:** `/search song name`")

        query = message.text.split(None, 1)[1]
        m = await message.reply_text("🔍 Searching on YouTube...")
        results = YoutubeSearch(query, max_results=5).to_dict()

        text = "🎬 **Top 5 YouTube Results:**\n\n"
        for i in range(5):
            text += f"➤ **Title:** `{results[i]['title']}`\n"
            text += f"⏱️ **Duration:** `{results[i]['duration']}`\n"
            text += f"👁️ **Views:** `{results[i]['views']}`\n"
            text += f"📺 **Channel:** `{results[i]['channel']}`\n"
            text += f"🔗 https://www.youtube.com{results[i]['url_suffix']}\n\n"

        await m.edit(text, disable_web_page_preview=True)

    except Exception as e:
        await m.edit(f"❌ Error:\n`{e}`") 
