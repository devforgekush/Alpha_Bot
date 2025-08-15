# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import random
import httpx
from pyrogram import filters
from pyrogram.types import Message
from Audify import app

# /pickwinner - Randomly pick a winner from list
@app.on_message(filters.command("pickwinner"))
async def pick_winner(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("🎯 Usage: `/pickwinner name1 name2 name3 ...`")
    
    participants = message.command[1:]
    winner = random.choice(participants)
    await message.reply_text(f"🏆 **The Winner is:** `{winner}` 🎉")


# /echo - Repeat any message
@app.on_message(filters.command("echo"))
async def echo_back(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("🔁 Usage: `/echo your text here`")
    
    text = message.text.split(None, 1)[1]
    await message.reply_text(f"🔁 **Echo:**\n{text}")


# /webss - Take website screenshot
@app.on_message(filters.command("webss"))
async def web_screenshot(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("🌐 Usage: `/webss <url>`\nExample: `/webss https://example.com`")

    url = message.text.split(None, 1)[1].strip()

    screenshot_api = f"https://image.thum.io/get/fullpage/{url}"

    try:
        await message.reply_photo(screenshot_api, caption=f"🖼️ Screenshot of: `{url}`")
    except Exception:
        await message.reply_text("❌ Failed to capture screenshot. Make sure URL is valid and public.")


# /ud - Urban Dictionary slang definition
@app.on_message(filters.command("ud"))
async def urban_define(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("📖 Usage: `/ud <word>`\nExample: `/ud sus`")
    
    word = message.text.split(None, 1)[1]

    url = f"https://api.urbandictionary.com/v0/define?term={word}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            data = response.json()
            if data["list"]:
                entry = data["list"][0]
                definition = entry["definition"][:1000]
                example = entry["example"][:1000]
                await message.reply_text(
                    f"📖 **Urban Dictionary:** `{word}`\n\n"
                    f"🧠 **Definition:**\n{definition}\n\n"
                    f"💬 **Example:**\n_{example}_"
                )
            else:
                await message.reply_text("❌ No results found.")
        except Exception:
            await message.reply_text("❌ Failed to fetch definition.")
