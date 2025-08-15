# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from Audify import app
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import PeerIdInvalid, UserNotMutualContact, UsernameNotOccupied

@app.on_message(filters.command("id"))
async def get_id(client, message: Message):
    chat = message.chat
    from_user = message.from_user or message.sender_chat
    reply = message.reply_to_message
    msg_id = message.id

    if not from_user:
        return await message.reply_text("❌ Unable to determine your user ID.")

    text = f"<b>🧾 Message ID:</b> <code>{msg_id}</code>\n"
    text += f"<b>👤 Your ID:</b> <code>{from_user.id}</code>\n"
    text += f"<b>💬 Chat ID:</b> <code>{chat.id}</code>\n"

    if len(message.command) > 1:
        try:
            user_arg = message.command[1].strip()
            user = await client.get_users(user_arg)
            text += f"\n<b>🙋 Queried User:</b> {user.mention}\n"
            text += f"<b>🆔 User ID:</b> <code>{user.id}</code>\n"
        except (PeerIdInvalid, UserNotMutualContact, UsernameNotOccupied, ValueError):
            return await message.reply_text("❌ <b>User not found or invalid input.</b>")

    if reply:
        if reply.from_user:
            text += (
                f"\n<b>↩️ Replied Message ID:</b> <code>{reply.id}</code>\n"
                f"<b>👥 Replied User:</b> {reply.from_user.mention}\n"
                f"<b>🆔 Replied User ID:</b> <code>{reply.from_user.id}</code>\n"
            )
        elif reply.forward_from_chat:
            text += (
                f"\n<b>📢 Forwarded Channel:</b> {reply.forward_from_chat.title}\n"
                f"<b>🆔 Channel ID:</b> <code>{reply.forward_from_chat.id}</code>\n"
            )
        elif reply.sender_chat:
            text += (
                f"\n<b>📡 Sender Chat Name:</b> {reply.sender_chat.title}\n"
                f"<b>🆔 Sender Chat ID:</b> <code>{reply.sender_chat.id}</code>\n"
            )

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Close", callback_data="close")]
    ])

    await message.reply_text(
        text,
        reply_markup=buttons,
        disable_web_page_preview=True,
        parse_mode=ParseMode.HTML,
    )
