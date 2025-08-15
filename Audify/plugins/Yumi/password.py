# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import random
from pyrogram import Client, filters, enums
from Audify import app
from config import BOT_USERNAME
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@app.on_message(filters.command(["genpassword", "genpw"]))
async def password(bot, update):
    message = await update.reply_text(text="🔐 Generating your password...")

    charset = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+".lower()

    if len(update.command) > 1:
        length_input = update.text.split(" ", 1)[1]
    else:
        length_input = random.choice(["5", "6", "7", "8", "9", "10", "12", "13", "14"])

    try:
        limit = int(length_input)
    except ValueError:
        return await message.edit_text("❗ Please provide a valid number for password length.")

    generated_password = "".join(random.sample(charset, limit))

    txt = (
        f"<b>Password Length:</b> {limit}\n"
        f"<b>Generated Password:</b> <code>{generated_password}</code>"
    )

    btn = InlineKeyboardMarkup(
        [[InlineKeyboardButton("➕ Add Me to Your Group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")]]
    )

    await message.edit_text(text=txt, reply_markup=btn, parse_mode=enums.ParseMode.HTML)
