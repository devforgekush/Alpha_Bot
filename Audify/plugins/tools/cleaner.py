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

# MongoDB Collection
cleaner_col = db.cleaner

# -------------------------------
# Helper Functions
# -------------------------------

async def is_cleaner_on(chat_id: int) -> bool:
    return bool(await cleaner_col.find_one({"chat_id": chat_id}))

async def enable_cleaner(chat_id: int):
    await cleaner_col.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": True}},
        upsert=True
    )

async def disable_cleaner(chat_id: int):
    await cleaner_col.delete_one({"chat_id": chat_id})

# -------------------------------
# Command: /cleaner (toggle)
# -------------------------------

@app.on_message(filters.command("cleaner") & filters.group)
async def toggle_cleaner(_, message: Message):
    chat_id = message.chat.id
    if await is_cleaner_on(chat_id):
        await disable_cleaner(chat_id)
        await message.reply_text("🧹 Service Cleaner has been **disabled**.")
    else:
        await enable_cleaner(chat_id)
        await message.reply_text(
            "🧹 Service Cleaner has been **enabled**.\n"
            "All service messages and join/leave clutter will now be automatically deleted."
        )

# -------------------------------
# Auto Message Cleaner (safe)
# -------------------------------

@app.on_message(
    filters.group & (
        filters.new_chat_members |
        filters.left_chat_member |
        filters.new_chat_title |
        filters.new_chat_photo |
        filters.delete_chat_photo |
        filters.group_chat_created |
        filters.channel_chat_created |
        filters.pinned_message
    )
)
async def auto_clean_services(_, message: Message):
    chat_id = message.chat.id

    if not await is_cleaner_on(chat_id):
        return

    try:
        await message.delete()
    except Exception:
        pass
