# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from datetime import datetime

from pyrogram import filters
from pyrogram.errors import PeerIdInvalid, UserNotMutualContact
from pyrogram.types import Message, User

from Audify import app


def FullName(user: User):
    return f"{user.first_name} {user.last_name}" if user.last_name else user.first_name


def LastOnline(user: User):
    if user.is_bot:
        return "🤖 Bot"
    status = getattr(user.status, "value", user.status)
    if status == "recently":
        return "🕒 Recently"
    elif status == "within_week":
        return "📆 Within the last week"
    elif status == "within_month":
        return "🗓 Within the last month"
    elif status == "long_time_ago":
        return "⌛ A long time ago"
    elif status == "online":
        return "🟢 Currently online"
    elif status == "offline":
        return datetime.fromtimestamp(user.last_online_date).strftime("%d %b %Y, %I:%M %p")
    return "❓ Unknown"


@app.on_message(filters.command("whois"))
async def whois(_, message: Message):
    args = message.command

    if len(args) == 1 and message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(args) == 1:
        user_id = message.from_user.id
    else:
        user_id = args[1]
        try:
            user_id = int(user_id)
        except ValueError:
            pass

    try:
        user = await app.get_users(user_id)
        chat = await app.get_chat(user.id)
    except PeerIdInvalid:
        return await message.reply("❌ I couldn't find that user.")
    except UserNotMutualContact:
        chat = user
    except Exception as e:
        return await message.reply(f"⚠️ Error: `{e}`")

    bio = chat.bio or "No bio available."
    name = FullName(user)
    username = f"@{user.username}" if user.username else "No username"
    last_seen = LastOnline(user)

    text = (
        f"**🙋 User Info**\n\n"
        f"• **Name:** [{name}](tg://user?id={user.id})\n"
        f"• **ID:** `{user.id}`\n"
        f"• **Username:** {username}\n"
        f"• **First Name:** `{user.first_name}`\n"
        f"• **Last Name:** `{user.last_name or 'None'}`\n"
        f"• **Last Seen:** `{last_seen}`\n"
        f"• **Bio:** `{bio}`"
    )

    await message.reply_text(text, disable_web_page_preview=True)
