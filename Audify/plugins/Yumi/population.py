# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import requests
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from Audify import app

@app.on_message(filters.command("population"))
async def country_command_handler(client: Client, message: Message):
    try:
        country_code = message.text.split(maxsplit=1)[1].strip()
    except IndexError:
        return await message.reply_text(
            "❗ Please provide a country code.\n\nExample: `/population in`"
        )

    api_url = f"https://restcountries.com/v3.1/alpha/{country_code}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()

        country_info = response.json()
        if country_info:
            name = country_info[0].get("name", {}).get("common", "N/A")
            capital = country_info[0].get("capital", ["N/A"])[0]
            population = country_info[0].get("population", "N/A")

            text = (
                f"🌍 <b>Country Information</b>\n\n"
                f"<b>🇨🇴 Name:</b> {name}\n"
                f"<b>🏙️ Capital:</b> {capital}\n"
                f"<b>👥 Population:</b> {population:,}"
            )
        else:
            text = "❗ Unable to fetch country information. Please try again."
    except requests.exceptions.HTTPError:
        text = "⚠️ Invalid country code. Try again with a valid one."
    except Exception:
        text = "⚠️ Something went wrong while fetching the data."

    await message.reply_text(text, parse_mode=enums.ParseMode.HTML)
