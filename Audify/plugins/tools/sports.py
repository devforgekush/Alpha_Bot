# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import httpx
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Audify import app

# ----------------------------
# Cricket Match Updates
# ----------------------------
CRICKET_API = "https://api.cricapi.com/v1/currentMatches?apikey=demo&offset=0"
FOOTBALL_API = "https://api.api-football.com/v3/fixtures?live=all"

# --- Cricket Command ---
@app.on_message(filters.command("cricket"))
async def cricket_handler(_, message: Message):
    await message.reply_chat_action("typing")
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(CRICKET_API)
            data = res.json()

        if not data.get("data"):
            return await message.reply_text("❌ No cricket matches found currently.")

        msg = "🏏 **Live Cricket Matches:**\n\n"
        for match in data["data"][:5]:
            teams = f"{match['teamInfo'][0]['name']} vs {match['teamInfo'][1]['name']}"
            status = match["status"]
            score = ""
            for s in match.get("score", []):
                score += f"{s['inning']}: {s['r']}/{s['w']} in {s['o']} overs\n"
            msg += f"• **{teams}**\n{status}\n{score}\n"

        btn = InlineKeyboardMarkup([[InlineKeyboardButton("⏩ Next Match", callback_data="next_cricket")]])
        await message.reply_text(msg, reply_markup=btn)
    except Exception as e:
        await message.reply_text("⚠️ Failed to fetch cricket data.")


# --- Football Command (renamed to /fball) ---
@app.on_message(filters.command("fball"))
async def football_handler(_, message: Message):
    await message.reply_chat_action("typing")
    headers = {"x-apisports-key": "your_api_key_here"}  # Replace with real key
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(FOOTBALL_API, headers=headers)
            data = res.json()

        if not data.get("response"):
            return await message.reply_text("❌ No live football matches found.")

        msg = "⚽ **Live Football Matches:**\n\n"
        for match in data["response"][:5]:
            league = match["league"]["name"]
            teams = f"{match['teams']['home']['name']} vs {match['teams']['away']['name']}"
            goals = f"{match['goals']['home']} - {match['goals']['away']}"
            time = match["fixture"]["status"]["elapsed"]
            msg += f"• **{teams}** ({league})\nScore: {goals} | ⏱️ {time} mins\n\n"

        btn = InlineKeyboardMarkup([[InlineKeyboardButton("⏩ Next Match", callback_data="next_football")]])
        await message.reply_text(msg, reply_markup=btn)
    except Exception:
        await message.reply_text("⚠️ Failed to fetch football data.")


# --- Callback Handling ---
@app.on_callback_query(filters.regex("next_cricket"))
async def next_cricket(_, cb):
    await cb.answer("Loading next match...", show_alert=False)
    await cricket_handler(_, cb.message)


@app.on_callback_query(filters.regex("next_football"))
async def next_football(_, cb):
    await cb.answer("Loading next match...", show_alert=False)
    await football_handler(_, cb.message)
