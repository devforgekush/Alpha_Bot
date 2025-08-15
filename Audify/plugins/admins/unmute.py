# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from Audify import app
from pyrogram import filters, enums
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from Audify.utils.Audify_BAN import admin_filter


@app.on_message(filters.command("unmuteall") & admin_filter)
async def unmute_all(_, msg):
    chat_id = msg.chat.id
    bot_user = await app.get_me()

    bot_member = await app.get_chat_member(chat_id, bot_user.id)
    if not bot_member.privileges or not bot_member.privileges.can_restrict_members:
        return await msg.reply_text(
            "🚫 I don't have permission to unmute members in this group."
        )

    count = 0
    async for member in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.RESTRICTED):
        try:
            await app.restrict_chat_member(
                chat_id,
                member.user.id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_polls=True,
                    can_add_web_page_previews=True,
                    can_invite_users=True,
                    can_send_other_messages=True
                )
            )
            count += 1
        except Exception as e:
            from Audify.logging import LOGGER
            LOGGER(__name__).error(f"❌ Failed to unmute {member.user.id} -> {e}")

    await msg.reply_text(
        f"✅ Successfully unmuted {count} users.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("❌ Close", callback_data="stop")]]
        )
    )


@app.on_callback_query(filters.regex("^stop$"))
async def stop_callback(_, query):
    await query.message.delete()
