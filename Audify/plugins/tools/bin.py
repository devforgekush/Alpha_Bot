# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from ... import *
from pyrogram import *
from pyrogram.enums import ParseMode
from pyrogram.types import *
from config import BOT_USERNAME
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@app.on_message(filters.command(["bin", "ccbin", "bininfo"], prefixes=[".", "!", "/"]))
async def check_ccbin(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "⚠️ Please provide a BIN to get BIN details.",
            parse_mode=ParseMode.HTML
        )
    try:
        await message.delete()
    except Exception:
        pass

    aux = await message.reply_text("🔎 Processing your request...")
    bin_code = message.text.split(None, 1)[1].strip()

    if len(bin_code) < 6:
        return await aux.edit("❗ BIN should be at least 6 digits.")

    try:
        resp = await api.bininfo(bin_code)

        output = f"""
<b>💳 BIN Full Details</b>

🏦 Bank: <code>{resp.bank}</code>
💳 BIN: <code>{resp.bin}</code>
🌍 Country: <code>{resp.country}</code> {resp.flag}
🔢 ISO: <code>{resp.iso}</code>
📊 Level: <code>{resp.level}</code>
💰 Prepaid: <code>{resp.prepaid}</code>
🛠️ Type: <code>{resp.type}</code>
🏷️ Vendor: <code>{resp.vendor}</code>

👤 Checked by: <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
"""

        Audify_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton(text="➕ Add Me", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
            [InlineKeyboardButton(text="❌ Close", callback_data="close")]
        ])

        await aux.edit(output, reply_markup=Audify_buttons, parse_mode=ParseMode.HTML)

    except Exception:
        return await aux.edit(
            "❌ BIN not recognized. Please enter a valid BIN.",
            parse_mode=ParseMode.HTML
        )
