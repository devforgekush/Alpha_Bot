# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import filters
from pyrogram.types import Message
from Audify import app
from Audify.core.mongo import mongodb as db

COLL = db.announcement_settings  # MongoDB collection

# 🔄 Check if announcements are enabled
async def is_announcement_enabled(chat_id: int) -> bool:
    result = await COLL.find_one({"chat_id": chat_id})
    return bool(result and result.get("enabled", False))

# ⚙️ Toggle announcement mode
async def set_announcement(chat_id: int, status: bool):
    await COLL.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": status}},
        upsert=True
    )

# 🧩 /announcement command
@app.on_message(filters.command("announcement") & filters.group)
async def toggle_announcement(_, message: Message):
    chat_id = message.chat.id
    current = await is_announcement_enabled(chat_id)
    new_status = not current
    await set_announcement(chat_id, new_status)

    if new_status:
        text = "📢 **Announcement system enabled!**\nNow you can send important messages to your group easily."
    else:
        text = "🔕 **Announcement system disabled.**"

    await message.reply(text)
