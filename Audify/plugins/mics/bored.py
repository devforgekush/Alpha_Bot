# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import requests
from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from Audify import app

# ▸ Bored API endpoint
BORED_API_URL = "https://apis.scrimba.com/bored/api/activity"


@app.on_message(filters.command("bored", prefixes=["/", "!", ".", "#", "$"]))
async def bored_command(_, message):
    try:
        response = requests.get(BORED_API_URL)

        if response.status_code != 200:
            return await message.reply(
                "**⚠️ Failed to fetch activity. Please try again later.**"
            )

        data = response.json()
        activity = data.get("activity")

        if not activity:
            return await message.reply("❌ No activity found at the moment.")

        text = f"""
**😐 Feeling bored?**
Here’s something you could try:

**🎯 {activity}**
"""

        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("✖ Close", callback_data="close")]]
        )

        await message.reply(text, reply_markup=keyboard)

    except Exception as e:
        await message.reply(f"**⚠️ Error occurred:** `{str(e)}`")
