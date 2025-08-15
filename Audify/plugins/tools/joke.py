# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import requests
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Audify import app

# Joke API URL (English only, safe jokes)
JOKE_API = "https://v2.jokeapi.dev/joke/Any?safe-mode"

# ⏹ Inline Close Button
CLOSE_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("⏹ Close", callback_data="close")]
])

# 📚 /joke Command Handler
@app.on_message(filters.command("joke"))
async def send_joke(_, message: Message):
    try:
        response = requests.get(JOKE_API, timeout=5)
        data = response.json()

        # Handle error in response
        if data.get("error") or not data.get("safe"):
            return await message.reply_text("⚠️ Couldn't fetch a safe joke. Try again.")

        # Format joke
        if data["type"] == "twopart":
            joke = f"😂 <b>{data['setup']}</b>\n\n👉 <i>{data['delivery']}</i>"
        else:
            joke = f"😂 <b>{data['joke']}</b>"

        await message.reply_text(
            joke,
            reply_markup=CLOSE_BUTTON,
            parse_mode=ParseMode.HTML
        )

    except Exception as e:
        await message.reply_text(
            f"❌ <b>Failed to fetch joke.</b>\n<code>{e}</code>",
            parse_mode=ParseMode.HTML
        )
