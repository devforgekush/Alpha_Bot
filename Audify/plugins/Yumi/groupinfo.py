# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import Client, filters
from pyrogram.types import Message
from Audify import app

# /groupinfo command for checking details of a group by username
@app.on_message(filters.command("groupinfo", prefixes="/"))
async def get_group_status(_, message: Message):
    if len(message.command) != 2:
        await message.reply(
            "⚠️ Please provide a group username.\n\n"
            "💡 Example: `/groupinfo YourGroupUsername`"
        )
        return

    group_username = message.command[1]

    try:
        group = await app.get_chat(group_username)
    except Exception as e:
        await message.reply(f"❌ Error: {e}")
        return

    total_members = await app.get_chat_members_count(group.id)
    group_description = group.description or "Not available"
    
    response_text = (
        "**📊 Group Details Panel**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📛 **Title:** {group.title}\n"
        f"🆔 **ID:** `{group.id}`\n"
        f"👥 **Members:** {total_members}\n"
        f"🔤 **Username:** @{group_username}\n"
        f"📝 **Description:** {group_description}\n"
        "━━━━━━━━━━━━━━━━━━━━━━"
    )

    await message.reply(response_text)


# /status command to check current group info (only works in groups)
@app.on_message(filters.command("status") & filters.group)
def group_status(client, message):
    chat = message.chat
    status_text = (
        "**📄 Current Group Status**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📛 **Title:** {chat.title}\n"
        f"🆔 **ID:** `{chat.id}`\n"
        f"📦 **Type:** {chat.type}\n"
        f"🔗 **Username:** @{chat.username if chat.username else 'None'}\n"
        "━━━━━━━━━━━━━━━━━━━━━━"
    )
    message.reply_text(status_text)
