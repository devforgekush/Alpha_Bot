from Audify import app
from config import OWNER_ID
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Audify.utils.Audify_BAN import admin_filter

BOT_ID = "7982320685"

@app.on_message(filters.command("unbanall") & admin_filter)
async def unban_all(_, msg):
    chat_id = msg.chat.id
    x = 0
    bot = await app.get_chat_member(chat_id, BOT_ID)
    bot_permission = bot.privileges.can_restrict_members == True

    if bot_permission:
        banned_users = []
        async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BANNED):
            banned_users.append(m.user.id)
            try:
                await app.unban_chat_member(chat_id, banned_users[x])
                from Audify.logger import LOGGER
                LOGGER(__name__).info(f"🔓 Unbanning: {m.user.mention}")
                x += 1
            except Exception:
                pass
        await msg.reply_text(f"✅ **Successfully unbanned {x} user(s) from the group.**")
    else:
        await msg.reply_text(
            "⚠️ **Unable to unban users.**\n\n"
            "Please ensure I have the permission to manage bans, and that you are an authorized sudo user."
        )

@app.on_callback_query(filters.regex("^stop$"))
async def stop_callback(_, query):
    await query.message.delete()
