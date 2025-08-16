from pyrogram import Client, filters
import requests
from Audify import app

# Command handler for /meme
@app.on_message(filters.command("meme"))
async def meme_command(client, message):
    api_url = "https://meme-api.com/gimme"

    try:
        response = requests.get(api_url)
        data = response.json()

        meme_url = data.get("url")
        title = data.get("title")

        bot_user = await app.get_me()  # ← async method

        caption = (
            f"🖼️ **{title}**\n\n"
            f"🔸 Requested by: {message.from_user.mention}\n"
            f"🤖 Bot: @{bot_user.username}"
        )

        await message.reply_photo(  # ← must await
            photo=meme_url,
            caption=caption
        )

    except Exception as e:
    from Audify.logger import LOGGER
    LOGGER(__name__).error(f"Error fetching meme: {e}")
    await message.reply_text("⚠️ Sorry, I couldn't fetch a meme at the moment.")
