from pyrogram import filters
from pyrogram.types import Message, ChatPermissions
from Audify import app
from Audify.core.mongo import mongodb as db

COLL = db.antichannel_settings  # MongoDB collection

# ✅ Check status
async def is_antichannel_enabled(chat_id: int) -> bool:
    doc = await COLL.find_one({"chat_id": chat_id})
    return bool(doc and doc.get("enabled", False))

# 🔄 Toggle status
async def set_antichannel(chat_id: int, status: bool):
    await COLL.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": status}},
        upsert=True
    )

# 🧩 /antichannel command
@app.on_message(filters.command("antichannel") & filters.group)
async def toggle_antichannel(_, message: Message):
    chat_id = message.chat.id
    current = await is_antichannel_enabled(chat_id)
    new_status = not current
    await set_antichannel(chat_id, new_status)

    if new_status:
        await message.reply("🚫 **Anti-Channel Protection Enabled!**\nUsers with channel-linked profiles will now be auto-kicked.")
    else:
        await message.reply("✅ **Anti-Channel Protection Disabled.**")

# 🛡️ Detect new users with linked channels
@app.on_message(filters.new_chat_members)
async def handle_new_members(_, message: Message):
    chat_id = message.chat.id
    if not await is_antichannel_enabled(chat_id):
        return

    for member in message.new_chat_members:
        if member.is_bot:
            continue
        if member.linked_chat:
            try:
                await app.kick_chat_member(chat_id, member.id)
                await message.reply(
                    f"🔨 Kicked [{member.mention}](tg://user?id={member.id}) — Channel-linked profile detected.",
                    disable_web_page_preview=True
                )
            except Exception as e:
                from Audify.logger import LOGGER
                LOGGER(__name__).error(f"❌ Error kicking channel-linked user: {e}")
