# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
import requests
from Audify import app

SUPPORT_CHAT = "GrayBotSupport"

# Common support button
BUTTON = [[InlineKeyboardButton("Support", url=f"https://t.me/{SUPPORT_CHAT}")]]

# /wish command
@app.on_message(filters.command("wish"))
async def wish(_, m):
    if len(m.command) < 2:
        await m.reply("❗ Please write your wish after the command.")
        return

    try:
        api = requests.get("https://nekos.best/api/v2/happy").json()
        url = api["results"][0]['url']
    except Exception:
        url = "https://media.tenor.com/NeYijHtdUZkAAAAC/hello-wave.gif"  # fallback

    text = m.text.split(None, 1)[1]
    wish_count = random.randint(1, 100)

    wish_text = f"✨ Hey {m.from_user.first_name},\n"
    wish_text += f"🎯 Your Wish: `{text}`\n"
    wish_text += f"📈 Possibility: `{wish_count}%`"

    await app.send_animation(
        chat_id=m.chat.id,
        animation=url,
        caption=wish_text,
        reply_markup=InlineKeyboardMarkup(BUTTON)
    )

# /cute command with cute gif from API
@app.on_message(filters.command("cute"))
async def cute(_, message):
    if not message.reply_to_message:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
    else:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name

    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    percent = random.randint(1, 100)
    caption_text = f"🌸 {mention}, you are `{percent}%` cute!"

    # Get cute gif from API
    try:
        gif_api = requests.get("https://nekos.best/api/v2/neko").json()
        gif_url = gif_api["results"][0]["url"]
    except Exception:
        gif_url = "https://media.tenor.com/Tq7SHJExmHcAAAAC/anime-cute.gif"  # fallback

    await app.send_document(
        chat_id=message.chat.id,
        document=gif_url,
        caption=caption_text,
        reply_markup=InlineKeyboardMarkup(BUTTON),
        reply_to_message_id=message.reply_to_message.message_id if message.reply_to_message else None,
    )

# Help Text (optional)
help_text = """
🎯 /wish [your wish]
→ Example: /wish I want to be a topper

🌸 /cute
→ Replies with your cuteness percentage + random cute gif.
"""
