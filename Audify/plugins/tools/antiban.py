# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import asyncio
from datetime import datetime, timedelta
from collections import defaultdict

from pyrogram import Client, filters
from pyrogram.types import Message, ChatMemberUpdated, ChatPrivileges

from Audify import app
from Audify.core.mongo import mongodb as db

COLL = db.antibanall_settings  # MongoDB collection
ban_tracker = defaultdict(list)  # Track bans per admin


# ✅ Check if antiban is enabled in group
async def is_antiban_enabled(chat_id: int) -> bool:
    doc = await COLL.find_one({"chat_id": chat_id})
    return bool(doc and doc.get("enabled", False))


# 🔄 Enable or disable antiban protection
async def set_antiban(chat_id: int, status: bool):
    await COLL.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": status}},
        upsert=True
    )


# 🧩 Command: /antibanall — Toggle antiban protection
@app.on_message(filters.command("antibanall") & filters.group)
async def toggle_antiban(_, message: Message):
    chat_id = message.chat.id
    current_status = await is_antiban_enabled(chat_id)
    new_status = not current_status
    await set_antiban(chat_id, new_status)

    if new_status:
        await message.reply(
            "🛡️ **Anti-BanAll Protection Enabled!**\n"
            "Admins who mass-ban users will be automatically demoted."
        )
    else:
        await message.reply("✅ **Anti-BanAll Protection Disabled.**")


# 🚨 Mass ban detection
@app.on_chat_member_updated()
async def detect_mass_bans(_, update: ChatMemberUpdated):
    chat_id = update.chat.id

    # Ensure antiban is enabled
    if not await is_antiban_enabled(chat_id):
        return

    # Ensure a user was banned (kicked)
    if not update.new_chat_member or update.new_chat_member.status != "kicked":
        return

    # Ensure we have the admin who performed the action
    actor = update.from_user
    if not actor:
        return

    user_id = actor.id
    now = datetime.utcnow()

    # Track ban timestamps
    ban_tracker[user_id].append(now)
    ban_tracker[user_id] = [t for t in ban_tracker[user_id] if now - t < timedelta(seconds=10)]

    if len(ban_tracker[user_id]) > 5:
        try:
            # Demote the admin by removing all privileges
            await app.promote_chat_member(
                chat_id,
                user_id,
                privileges=ChatPrivileges(
                    can_change_info=False,
                    can_post_messages=False,
                    can_edit_messages=False,
                    can_delete_messages=False,
                    can_invite_users=False,
                    can_restrict_members=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                    can_manage_video_chats=False,
                    can_manage_chat=False,
                    can_manage_topics=False
                )
            )

            await app.send_message(
                chat_id,
                f"🚷 Admin [{actor.mention}](tg://user?id={user_id}) was demoted for **mass banning** users.",
                disable_web_page_preview=True
            )
        except Exception as e:
            await app.send_message(
                chat_id,
                f"⚠️ **Mass Ban Detected!**\n"
                f"Admin [{actor.mention}](tg://user?id={user_id}) banned more than 5 users in 10 seconds.\n"
                f"❌ I couldn’t demote them. Please check manually.\n\n"
                f"🔧 Error: `{str(e)}`",
                disable_web_page_preview=True
            )

        # Reset their history
        ban_tracker[user_id].clear()
