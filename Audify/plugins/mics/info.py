# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Audify import app

# Close button for all messages
CLOSE_BTN = InlineKeyboardMarkup([
    [InlineKeyboardButton("✖ Close", callback_data="close")]
])

# Convert user status enum to readable label
async def user_status_text(user_id):
    try:
        user = await app.get_users(user_id)
        return {
            enums.UserStatus.RECENTLY: "Recently online",
            enums.UserStatus.LAST_WEEK: "Seen last week",
            enums.UserStatus.LONG_AGO: "Inactive for long",
            enums.UserStatus.OFFLINE: "Currently offline",
            enums.UserStatus.ONLINE: "🟢 Online now",
        }.get(user.status, "Unknown")
    except:
        return "Unknown"

# /info or /userinfo command
@app.on_message(filters.command(["info", "userinfo", "information"]))
async def user_info(_, message: Message):
    try:
        # Determine target user
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        elif len(message.command) == 2:
            user_id = message.text.split()[1]
        else:
            user_id = message.from_user.id

        # Fetch user info
        user = await app.get_users(user_id)
        chat = await app.get_chat(user.id)

        # Build message
        text = (
            f"<b>👤 User Profile Summary</b>\n\n"
            f"<b>🆔 ID:</b> <code>{user.id}</code>\n"
            f"<b>🔗 Username:</b> @{user.username or 'Not set'}\n"
            f"<b>📛 Name:</b> {user.first_name}\n"
            f"<b>📡 Status:</b> {await user_status_text(user.id)}\n"
            f"<b>🌐 DC ID:</b> {user.dc_id or 'Unavailable'}\n"
            f"<b>📝 Bio:</b> {chat.bio or 'No bio available.'}"
        )

        # Send nicely formatted message
        await message.reply(text, reply_markup=CLOSE_BTN, quote=True)

    except Exception as e:
        await message.reply_text(f"⚠️ <b>Error:</b> <code>{str(e)}</code>")
