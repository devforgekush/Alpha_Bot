# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import filters, enums
from pyrogram.types import Message, ChatPrivileges
from pyrogram.enums import ChatMemberStatus
from Audify import app
from Audify.core.mongo import mongodb as db

# ----------------------------
# Database functions (LOG_DB)
# ----------------------------
class LogDatabase:
    def __init__(self):
        self.collection = db.get_collection("logchannel")

    async def set_log(self, chat_id: int, channel_id: int):
        await self.collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"log_channel": channel_id}},
            upsert=True
        )

    async def get_log(self, chat_id: int):
        data = await self.collection.find_one({"chat_id": chat_id})
        return data.get("log_channel") if data else None

    async def remove_log(self, chat_id: int):
        await self.collection.delete_one({"chat_id": chat_id})

LOG_DB = LogDatabase()


# ----------------------------
# Admin check (inline)
# ----------------------------
async def is_admin(chat_id: int, user_id: int) -> bool:
    try:
        member = await app.get_chat_member(chat_id, user_id)
        return member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]
    except Exception:
        return False


# ----------------------------
# /setlog Command
# ----------------------------
@app.on_message(filters.command("setlog") & filters.group)
async def set_log_channel(_, message: Message):
    user = message.from_user
    chat = message.chat

    if not await is_admin(chat.id, user.id):
        return await message.reply_text("🚫 Only group admins can configure log channel.")

    if not message.reply_to_message or not message.reply_to_message.forward_from_chat:
        return await message.reply_text("🔗 Reply to a forwarded message from the log channel.")

    log_channel_id = message.reply_to_message.forward_from_chat.id

    try:
        member = await app.get_chat_member(log_channel_id, "me")
        if not member.can_post_messages:
            return await message.reply_text("❌ Bot must be an admin in log channel with post permissions.")
    except Exception:
        return await message.reply_text("❌ Couldn't access the log channel. Ensure the bot is added there.")

    await LOG_DB.set_log(chat.id, log_channel_id)
    await message.reply_text("✅ Log channel has been linked successfully!")


# ----------------------------
# /unsetlog Command
# ----------------------------
@app.on_message(filters.command("unsetlog") & filters.group)
async def unset_log_channel(_, message: Message):
    user = message.from_user
    chat = message.chat

    if not await is_admin(chat.id, user.id):
        return await message.reply_text("🚫 Only group admins can remove log channel.")

    await LOG_DB.remove_log(chat.id)
    await message.reply_text("❌ Log channel has been removed.")


# ----------------------------
# /logchannel Command
# ----------------------------
@app.on_message(filters.command("logchannel") & filters.group)
async def show_log_channel(_, message: Message):
    chat_id = message.chat.id
    log_id = await LOG_DB.get_log(chat_id)

    if not log_id:
        return await message.reply_text("ℹ️ No log channel linked yet.")

    try:
        chat = await app.get_chat(log_id)
        title = chat.title or "Private/Deleted Channel"
        await message.reply_text(f"📥 **Current Log Channel:** `{log_id}`\n🏷️ **Title:** {title}")
    except Exception:
        await message.reply_text(f"⚠️ Log channel set, but I can't access it. Maybe removed or revoked.")


# ----------------------------
# Log event function (used anywhere)
# ----------------------------
async def log_event(group_id: int, log_text: str):
    log_channel = await LOG_DB.get_log(group_id)
    if not log_channel:
        return
    try:
        await app.send_message(log_channel, log_text)
    except Exception:
        pass
