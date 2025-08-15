# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import httpx
from pyrogram import filters
from pyrogram.types import Message
from Audify import app

API_URL = "https://api.urbandictionary.com/v0/define?term="

@app.on_message(filters.command("ud") & (filters.private | filters.group))
async def urban_lookup(_, message: Message):
    if not message.command or len(message.command) < 2:
        return await message.reply_text("❌ Please provide a word to look up.\n\nExample: `/ud savage`", quote=True)

    query = " ".join(message.command[1:])
    url = API_URL + query

    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(url, timeout=10)
            data = res.json()

        if not data.get("list"):
            return await message.reply_text(
                f"❌ No results found for **{query}**.\nTry checking the spelling or using simpler terms.",
                quote=True,
            )

        definition = data["list"][0]["definition"].strip().replace("[", "").replace("]", "")
        example = data["list"][0]["example"].strip().replace("[", "").replace("]", "")

        text = f"📘 **Urban Dictionary Lookup**\n\n"
        text += f"🔤 **Word:** `{query}`\n\n"
        text += f"📖 **Definition:**\n{definition}\n\n"
        text += f"💬 **Example:**\n_{example}_\n\n"
        text += f"🔎 [More on Google](https://www.google.com/search?q=urban+dictionary+{query.replace(' ', '+')})"

        await message.reply_text(text, disable_web_page_preview=True)

    except Exception as e:
        await message.reply_text(f"❌ Error fetching definition:\n`{e}`", quote=True)
