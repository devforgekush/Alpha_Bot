# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from Audify import app
from Audify.misc import SUDOERS
from Audify.utils.database import autoend_off, autoend_on


# Inline close button
close_button = InlineKeyboardMarkup([
    [InlineKeyboardButton("✖️ Close", callback_data="close")]
])


@app.on_message(filters.command("autoend") & SUDOERS)
async def auto_end_stream(_, message: Message):
    usage = (
        "**🎧 Auto-End Command Help**\n\n"
        "**Usage:**\n"
        "• `/autoend enable` — Activate auto-end.\n"
        "• `/autoend disable` — Deactivate auto-end.\n\n"
        "This feature makes the assistant leave the voice chat if no one is listening for a while."
    )

    if len(message.command) != 2:
        return await message.reply_text(usage, reply_markup=close_button)

    state = message.text.split(None, 1)[1].strip().lower()

    if state == "enable":
        await autoend_on()
        return await message.reply_text(
            "✅ **Auto-End Enabled**\n\n"
            "• Assistant will automatically leave the voice chat when no one is listening.",
            reply_markup=close_button
        )

    elif state == "disable":
        await autoend_off()
        return await message.reply_text(
            "🛑 **Auto-End Disabled**\n\n"
            "• Assistant will stay even if the voice chat is empty.",
            reply_markup=close_button
        )

    else:
        return await message.reply_text(usage, reply_markup=close_button)
