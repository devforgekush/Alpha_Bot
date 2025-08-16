from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import BOT_USERNAME
from Audify import app
import requests

@app.on_message(filters.command("write"))
async def handwrite(_, message: Message):
    if message.reply_to_message:
        text = message.reply_to_message.text
    else:
        text = message.text.split(None, 1)[1]

    m = await message.reply_text("✍️ Generating handwritten text image... Please wait.")
    
    write = requests.get(f"https://apis.xditya.me/write?text={text}").url

    caption = f"""
✅ Successfully written your text on paper.

🖋️ Created by: [Alphabot](https://t.me/{BOT_USERNAME})
🙋 Requested by: {message.from_user.mention}
"""
    await m.delete()
    await message.reply_photo(photo=write, caption=caption)


mod_name = "WriteTool"

help = """
This tool writes the given text on a white paper using a pen ✍️

❍ /write <text> — Converts the text into handwritten image.
❍ Reply to any message with /write to convert that message text into writing.
"""
