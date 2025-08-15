# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# Developed by @devforgekush. All rights reserved.
# ---------------------------------------------------------

from pyrogram import filters
from pyrogram.types import Message, ChatPermissions
from Audify import app
from Audify.core.mongo import mongodb as db

LOCKDB = db.locks

# 🧷 Available lock types mapped to Pyrogram ChatPermissions attributes
LOCK_TYPES = {
    "messages": "can_send_messages",
    "media": "can_send_media_messages",
    "polls": "can_send_polls",
    "other": "can_send_other_messages",
    "preview": "can_add_web_page_previews",
    "invite": "can_invite_users",
    "pin": "can_pin_messages",
    "info": "can_change_info",
}

# 📍 /locktypes: Show available lock types and their descriptions
@app.on_message(filters.command("locktypes") & filters.group)
async def locktypes_cmd(_, message: Message):
    text = (
        "**🔐 Available Lock Types:**\n\n"
        "`messages` - Prevent users from sending messages.\n"
        "`media` - Prevent sending photos, videos, gifs, voice notes, etc.\n"
        "`polls` - Prevent creating polls.\n"
        "`other` - Block stickers, animations, games, and contacts.\n"
        "`preview` - Disable link previews in messages.\n"
        "`invite` - Block sending invite links.\n"
        "`pin` - Block non-admins from pinning messages.\n"
        "`info` - Block non-admins from changing group info."
    )
    await message.reply(text)

# 📍 Fetch current locks from database
async def get_current_locks(chat_id: int):
    data = await LOCKDB.find_one({"chat_id": chat_id})
    return data.get("locks", []) if data else []

# 📍 /locks: View all currently active locks
@app.on_message(filters.command("locks") & filters.group)
async def view_locks(_, message: Message):
    locks = await get_current_locks(message.chat.id)
    if not locks:
        await message.reply("🔓 No active locks in this chat.")
    else:
        text = "🔐 **Active Locks:**\n\n" + "\n".join([f"• `{x}`" for x in locks])
        await message.reply(text)

# 📍 /lock <type>: Lock specific group permission
@app.on_message(filters.command("lock") & filters.group)
async def lock_chat(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("❓ Usage: `/lock media`")

    lock_type = message.command[1].lower()
    if lock_type not in LOCK_TYPES:
        return await message.reply("❌ Invalid lock type. Use `/locktypes` to see all options.")

    locks = await get_current_locks(message.chat.id)
    if lock_type in locks:
        return await message.reply(f"🔐 `{lock_type}` is already locked.")

    locks.append(lock_type)
    await LOCKDB.update_one({"chat_id": message.chat.id}, {"$set": {"locks": locks}}, upsert=True)
    await apply_locks(message.chat.id, locks)
    await message.reply(f"🔐 Locked `{lock_type}` for this chat.")

# 📍 /unlock <type>: Unlock specific group permission
@app.on_message(filters.command("unlock") & filters.group)
async def unlock_chat(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("❓ Usage: `/unlock media`")

    lock_type = message.command[1].lower()
    if lock_type not in LOCK_TYPES:
        return await message.reply("❌ Invalid lock type. Use `/locktypes` to see all options.")

    locks = await get_current_locks(message.chat.id)
    if lock_type not in locks:
        return await message.reply(f"🔓 `{lock_type}` is already unlocked.")

    locks.remove(lock_type)
    await LOCKDB.update_one({"chat_id": message.chat.id}, {"$set": {"locks": locks}}, upsert=True)
    await apply_locks(message.chat.id, locks)
    await message.reply(f"🔓 Unlocked `{lock_type}` for this chat.")

# ✅ Apply permission changes to group
async def apply_locks(chat_id: int, locks: list):
    permissions = ChatPermissions()
    for lock_name, attr in LOCK_TYPES.items():
        setattr(permissions, attr, lock_name not in locks)
    await app.set_chat_permissions(chat_id, permissions=permissions)
