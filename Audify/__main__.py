# ---------------------------------------------------------
# Alphabot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Alphabot project.
# Unauthorized copying, distribution, or use is prohibited.
# Developed by @devforgekush. All rights reserved.
# ---------------------------------------------------------


import asyncio
import importlib
import threading
import time
import requests


from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from Audify import LOGGER, app, userbot
from Audify.core.call import Audify
from Audify.misc import sudo
from Audify.plugins import ALL_MODULES
from Audify.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


def start_pinger():
    def ping_loop():
        url = getattr(config, "RAILWAY_URL", None)
        if not url:
            return
        while True:
            try:
                requests.get(url)
            except Exception:
                pass
            time.sleep(720)  # 12 minutes
    t = threading.Thread(target=ping_loop, daemon=True)
    t.start()

async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("🚫 String Session Missing! Please configure at least one Pyrogram session string.")
        exit()
    start_pinger()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("Audify.plugins" + all_module)
    LOGGER("Audify.plugins").info("✅ All modules successfully loaded. Alphabot is ready to serve 🎶")
    await userbot.start()
    await Audify.start()
    try:
        await Audify.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("Audify").error(
            "📢 Please start a voice chat in your log group or linked channel!\n\n⚠️ Alphabot cannot stream without an active group call."
        )
        exit()
    except:
        pass
    await Audify.decorators()
    LOGGER("Audify").info(
        "🎧 Alphabot Music Bot started successfully.\n🛡️ Developed with passion by @devforgekush 💻"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("Audify").info("🛑 Alphabot Music Bot has stopped. See you soon! 👋")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
