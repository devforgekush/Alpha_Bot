# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import requests
from pyrogram import filters
from pyrogram.types import InputMediaPhoto
from Audify import app

PIXABAY_API_KEY = "51452132-4125973c96102b2af09e3f13c"

@app.on_message(filters.command(["image"]))
async def pixabay_image(_, message):
    chat_id = message.chat.id

    try:
        query = message.text.split(None, 1)[1]
    except:
        return await message.reply(
            "🔍 **Please provide a keyword to search images.**\n\nExample: `/image nature`"
        )

    msg = await message.reply("📡 **Searching images...**")

    url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={query}&image_type=photo&per_page=6"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return await msg.edit("❌ **API returned an error. Try again later.**")

        data = response.json()
        hits = data.get("hits", [])
        if not hits:
            return await msg.edit("⚠️ No results found. Try another keyword.")

        media_group = []
        for hit in hits:
            media_group.append(InputMediaPhoto(media=hit["largeImageURL"]))

        await app.send_media_group(
            chat_id=chat_id,
            media=media_group,
            reply_to_message_id=message.id
        )
        await msg.delete()

    except Exception as e:
        await msg.edit(f"❌ **Error while fetching images:**\n`{str(e)}`")
