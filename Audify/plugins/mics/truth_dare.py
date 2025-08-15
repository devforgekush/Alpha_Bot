# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import Client, filters
import requests
from Audify import app

# API Endpoints
TRUTH_API_URL = "https://api.truthordarebot.xyz/v1/truth"
DARE_API_URL = "https://api.truthordarebot.xyz/v1/dare"

@app.on_message(filters.command("truth"))
async def get_truth(client, message):
    try:
        response = requests.get(TRUTH_API_URL)
        if response.status_code == 200:
            question = response.json().get("question")
            await message.reply_text(f"🧠 **Truth**\n\n{question}")
        else:
            await message.reply_text("❌ Couldn't fetch a truth question. Please try again later.")
    except Exception:
        await message.reply_text("⚠️ An error occurred while fetching a truth question.")

@app.on_message(filters.command("dare"))
async def get_dare(client, message):
    try:
        response = requests.get(DARE_API_URL)
        if response.status_code == 200:
            question = response.json().get("question")
            await message.reply_text(f"🔥 **Dare**\n\n{question}")
        else:
            await message.reply_text("❌ Couldn't fetch a dare challenge. Please try again later.")
    except Exception:
        await message.reply_text("⚠️ An error occurred while fetching a dare challenge.")
