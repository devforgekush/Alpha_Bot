# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from Audify import app
import aiohttp
import re

GOOGLE_API_KEY = "AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM"
CX_CODE = "ec8db9e1f9e41e65e"

def clean_link(link: str) -> str:
    if "/s" in link:
        link = link.replace("/s", "")
    elif re.search(r"/\d", link):
        link = re.sub(r"/\d", "", link)
    if "?" in link:
        link = link.split("?")[0]
    return link

async def fetch_results(query: str, start: int = 1):
    url = f"https://content-customsearch.googleapis.com/customsearch/v1"
    params = {
        "cx": CX_CODE,
        "q": query,
        "key": GOOGLE_API_KEY,
        "start": start
    }
    headers = {"x-referer": "https://explorer.apis.google.com"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as resp:
            return await resp.json()

def build_result_list(items):
    result = ""
    links_seen = set()
    for item in items:
        title = item.get("title")
        link = clean_link(item.get("link", ""))
        if link and link not in links_seen:
            result += f"🔹 {title}\n{link}\n\n"
            links_seen.add(link)
    return result or "❌ No valid results found."

def build_nav_buttons(query: str, start: int):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("◀️ Prev", callback_data=f"tg_prev_{start-10}_{query}"),
            InlineKeyboardButton("Next ▶️", callback_data=f"tg_next_{start+10}_{query}")
        ],
        [InlineKeyboardButton("✖ Close", callback_data="close")]
    ])

@app.on_message(filters.command("tg"))
async def tg_search(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("❗ Please provide a search query.\n\n**Usage:** `/tg telegram bots`")

    query = message.text.split(" ", 1)[1]
    msg = await message.reply("🔍 Searching...")

    data = await fetch_results(query)
    items = data.get("items", [])
    if not items:
        return await msg.edit("❌ No results found.")

    result = build_result_list(items)
    nav_buttons = build_nav_buttons(query, 11)

    await msg.edit(result, reply_markup=nav_buttons, disable_web_page_preview=True)

@app.on_callback_query(filters.regex(r"^tg_(prev|next)_(\d+)_(.+)$"))
async def tg_pagination(_, callback_query: CallbackQuery):
    action, start, query = callback_query.data.split("_", 2)
    start = int(start)

    data = await fetch_results(query, start=start)
    items = data.get("items", [])
    if not items:
        return await callback_query.answer("❌ No more results.")

    result = build_result_list(items)
    nav_buttons = build_nav_buttons(query, start)

    await callback_query.edit_message_text(result, reply_markup=nav_buttons, disable_web_page_preview=True)
