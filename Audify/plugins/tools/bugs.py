# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from datetime import datetime
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from config import OWNER_ID as owner_id, LOGGER_ID
from Audify import app


def content(msg: Message) -> [None, str]:
    if not msg.text or " " not in msg.text:
        return None
    return msg.text.split(None, 1)[1]


@app.on_message(filters.command("bug"))
async def report_bug(_, msg: Message):
    if msg.chat.type == "private":
        return await msg.reply_text("❗ This command can only be used in groups.")

    user = msg.from_user
    user_id = user.id
    mention = f"[{user.first_name}](tg://user?id={user_id})"
    chat_info = f"@{msg.chat.username}/`{msg.chat.id}`" if msg.chat.username else f"Private Group/`{msg.chat.id}`"
    bug_text = content(msg)
    date_str = datetime.utcnow().strftime("%d-%m-%Y")

    if user_id == owner_id:
        if bug_text:
            return await msg.reply_text("🧠 You're the bot owner. Stop trolling, bro!")
        return await msg.reply_text("😑 No bug content. You're just clicking buttons.")

    if not bug_text:
        return await msg.reply_text("⚠️ Please write the bug description after the command.")

    await msg.reply_text(
        f"🛠️ Bug reported:\n\n<b>{bug_text}</b>\n\n✅ Successfully sent to support.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✖️ Close", callback_data="close")]]),
        disable_web_page_preview=True
    )

    report_caption = f"""
📡 <b>Bug Report Received!</b>

👤 <b>Reported By:</b> {mention}
🆔 <b>User ID:</b> <code>{user_id}</code>
💬 <b>Chat:</b> {chat_info}
🐞 <b>Bug:</b> <code>{bug_text}</code>
🗓️ <b>Date:</b> <code>{date_str}</code>
"""

    await app.send_photo(
        LOGGER_ID,
        photo="https://telegra.ph/file/f66e5843568d4b7f2a652.jpg",
        caption=report_caption,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔍 View Bug", url=msg.link if msg.link else "https://t.me/")],
            [InlineKeyboardButton("✖️ Close", callback_data="close")]
        ])
    )
