from pyrogram.enums import ParseMode
from Audify import app
from Audify.utils.database import is_on_off
from config import LOGGER_ID


async def play_logs(message, streamtype):
    if await is_on_off(2):
        logger_text = f"""
<b>🎧 Alphabot Play Log</b>

<b>📍 Chat Info</b>
├ ID: <code>{message.chat.id}</code>
├ Title: {message.chat.title}
└ Username: @{message.chat.username if message.chat.username else 'N/A'}

<b>🙋‍♂️ User Info</b>
├ ID: <code>{message.from_user.id}</code>
├ Name: {message.from_user.mention}
└ Username: @{message.from_user.username if message.from_user.username else 'N/A'}

<b>🎵 Playback Info</b>
├ Query: <code>{message.text.split(None, 1)[1]}</code>
└ Stream Type: <code>{streamtype}</code>
"""
        if message.chat.id != LOGGER_ID:
            try:
                await app.send_message(
                    chat_id=LOGGER_ID,
                    text=logger_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except Exception:
                pass
