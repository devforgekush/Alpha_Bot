# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import os
import csv
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from Audify import app
from Audify.utils.Audify_BAN import admin_filter
from pyrogram.errors import UserNotParticipant


@app.on_message(filters.command("user") & admin_filter)
async def user_command(client, message):
    chat_id = message.chat.id
    members_list = []

    # Fetch all chat members
    async for member in client.get_chat_members(chat_id):
        if member.user.is_bot:
            continue
        members_list.append({
            "username": member.user.username or "N/A",
            "userid": member.user.id
        })

    # Save as CSV
    filename = "members.csv"
    with open(filename, "w", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["username", "userid"])
        writer.writeheader()
        writer.writerows(members_list)

    # Send document
    await message.reply_document(
        document=filename,
        caption=f"👥 Member list exported: {len(members_list)} users"
    )

    # Clean up local file
    os.remove(filename)


@app.on_message(filters.command("givelink"))
async def give_link_command(client, message):
    chat = message.chat
    try:
        member = await client.get_chat_member(chat.id, message.from_user.id)
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply_text("🔒 Only admins can generate invite links.")
    except UserNotParticipant:
        return await message.reply_text("🔒 Only admins can generate invite links.")

    try:
        link = await app.export_chat_invite_link(chat.id)
        await message.reply_text(f"🔗 Here’s the invite link:\n{link}")
    except Exception as e:
        await message.reply_text(f"❌ Failed to generate invite link:\n`{e}`")
