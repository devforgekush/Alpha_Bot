# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Audify import app


# ─── Handle Callback for Unpin ───────────────────────────────
@app.on_callback_query(filters.regex(r"^unpinall=(yes|no)$"))
async def unpin_callback(client, query):
    user_id = query.from_user.id
    chat_id = query.message.chat.id
    decision = query.data.split("=")[1]

    member = await app.get_chat_member(chat_id, user_id)
    if member.status not in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        return await query.answer("You don't have permission to unpin.", show_alert=True)

    if not member.privileges or not member.privileges.can_pin_messages:
        return await query.answer("Missing 'pin messages' permission.", show_alert=True)

    if decision == "yes":
        try:
            await app.unpin_all_chat_messages(chat_id)
            await query.message.edit_text(
                "✅ All pinned messages have been unpinned.",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🗑️ Close", callback_data="close")]]
                )
            )
        except Exception as e:
            await query.message.edit_text(f"❌ Failed to unpin messages.\n\n**Error:** `{e}`")
    else:
        await query.message.edit_text(
            "❎ Unpin action cancelled.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🗑️ Close", callback_data="close")]]
            )
        )


# ─── Unpin All Command ───────────────────────────────
@app.on_message(filters.command("unpinall"))
async def unpin_command(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    member = await app.get_chat_member(chat_id, user_id)
    if member.status not in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        return await message.reply_text("🚫 Only admins can use this command.")

    if not member.privileges or not member.privileges.can_pin_messages:
        return await message.reply_text("🔐 You lack permission to unpin messages.")

    await message.reply_text(
        "⚠️ Are you sure you want to unpin **all pinned messages** in this chat?",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("✅ Yes", callback_data="unpinall=yes"),
                    InlineKeyboardButton("❌ No", callback_data="unpinall=no")
                ]
            ]
        )
    )
