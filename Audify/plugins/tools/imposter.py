# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import random
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.enums import ParseMode

from Audify import app
from Audify.plugins.tools.pretenderdb import (
    impo_off,
    impo_on,
    check_pretender,
    add_userdata,
    get_userdata,
    usr_data,
)

# ⏹ Inline close button
CLOSE_BUTTON = InlineKeyboardMarkup(
    [[InlineKeyboardButton("⏹ Close", callback_data="close")]]
)

# ✅ Detect profile changes in group messages
@app.on_message(filters.group & ~filters.bot & ~filters.via_bot, group=69)
async def chk_usr(_, message: Message):
    if message.sender_chat or not await check_pretender(message.chat.id):
        return

    if not await usr_data(message.from_user.id):
        return await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )

    usernamebefore, first_name, lastname_before = await get_userdata(message.from_user.id)
    msg = ""

    if (
        usernamebefore != message.from_user.username
        or first_name != message.from_user.first_name
        or lastname_before != message.from_user.last_name
    ):
        msg += f"✅ <b>Detected Profile Update</b>\n\n"
        msg += f"• <b>Name:</b> {message.from_user.mention}\n"
        msg += f"• <b>User ID:</b> <code>{message.from_user.id}</code>\n"

    if usernamebefore != message.from_user.username:
        before = f"@{usernamebefore}" if usernamebefore else "No username"
        after = f"@{message.from_user.username}" if message.from_user.username else "No username"
        msg += f"\n<b>🔁 Username Changed:</b>\n• Before: <code>{before}</code>\n• After: <code>{after}</code>\n"
        await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )

    if first_name != message.from_user.first_name:
        msg += f"\n<b>🔁 First Name Changed:</b>\n• Before: <code>{first_name}</code>\n• After: <code>{message.from_user.first_name}</code>\n"
        await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )

    if lastname_before != message.from_user.last_name:
        before = lastname_before or "No last name"
        after = message.from_user.last_name or "No last name"
        msg += f"\n<b>🔁 Last Name Changed:</b>\n• Before: <code>{before}</code>\n• After: <code>{after}</code>\n"
        await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )

    if msg:
        await message.reply_text(
            msg,
            reply_markup=CLOSE_BUTTON,
            parse_mode=ParseMode.HTML
        )


# ⚙️ /imposter command to enable or disable the detection
@app.on_message(filters.command("imposter") & filters.group)
async def set_imposter(_, message: Message):
    if len(message.command) < 2:
        return await message.reply(
            "🔧 <b>Usage:</b>\n• <code>/imposter enable</code>\n• <code>/imposter disable</code>",
            parse_mode=ParseMode.HTML
        )

    cmd = message.command[1].lower()

    if cmd == "enable":
        already = await impo_on(message.chat.id)
        if already:
            return await message.reply("ℹ️ Pretender mode is already enabled.")
        return await message.reply(
            f"✅ Pretender mode enabled in <b>{message.chat.title}</b>.",
            parse_mode=ParseMode.HTML
        )

    elif cmd == "disable":
        already = await impo_off(message.chat.id)
        if not already:
            return await message.reply("ℹ️ Pretender mode is already disabled.")
        return await message.reply(
            f"❌ Pretender mode disabled in <b>{message.chat.title}</b>.",
            parse_mode=ParseMode.HTML
        )

    else:
        return await message.reply(
            "❓ <b>Invalid argument.</b>\nUse:\n• <code>/imposter enable</code>\n• <code>/imposter disable</code>",
            parse_mode=ParseMode.HTML
        )
