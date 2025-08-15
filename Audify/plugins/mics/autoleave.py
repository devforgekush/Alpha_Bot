import asyncio
import logging
from datetime import datetime, timedelta
import pytz

from pyrogram.enums import ChatType

import config
from Audify import app
from Audify.utils.database import get_client, is_active_chat

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("AutoLeave")

# Constants
EXCLUDED_CHAT_IDS = {config.LOGGER_ID}
MAX_LEAVES_PER_RUN = 20
TIMEZONE = "Asia/Kolkata"
TARGET_HOUR = 4
TARGET_MINUTE = 35

def seconds_until_target_time(hour: int = TARGET_HOUR, minute: int = TARGET_MINUTE) -> float:
    """Calculate seconds remaining until the next target time (default: 4:35 AM IST)."""
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if now >= target:
        target += timedelta(days=1)
    return (target - now).total_seconds()

async def leave_inactive_chats(client, client_num: int):
    """Make the client leave inactive chats."""
    left_count = 0
    try:
        async for dialog in client.get_dialogs():
            chat = dialog.chat
            if chat.type in {ChatType.SUPERGROUP, ChatType.GROUP, ChatType.CHANNEL}:
                if chat.id in EXCLUDED_CHAT_IDS:
                    continue
                if left_count >= MAX_LEAVES_PER_RUN:
                    break
                if not await is_active_chat(chat.id):
                    try:
                        await client.leave_chat(chat.id)
                        logger.info(f"{client.me.first_name} left inactive chat: {chat.title} ({chat.id})")
                        left_count += 1
                    except Exception as e:
                        logger.warning(f"Failed to leave chat {chat.title} ({chat.id}): {e}")
    except Exception as e:
        logger.error(f"Assistant {client_num} failed to fetch dialogs: {e}")

async def auto_leave():
    """Run auto leave job daily at 4:35 AM IST."""
    if not config.AUTO_LEAVING_ASSISTANT:
        logger.info("AUTO_LEAVING_ASSISTANT is disabled. Exiting auto_leave task.")
        return

    logger.info("AutoLeave task started and running in background.")
    from Audify.core.userbot import assistants

    while True:
        seconds_to_sleep = seconds_until_target_time()
        hrs, mins = divmod(seconds_to_sleep // 60, 60)
        logger.info(f"Sleeping for {int(hrs)}h {int(mins)}m until 4:35 AM IST.")
        await asyncio.sleep(seconds_to_sleep)

        logger.info("Running cleanup of inactive chats...")
        for num in assistants:
            client = await get_client(num)
            await leave_inactive_chats(client, num)
        logger.info("Cleanup complete. Sleeping again until next 4:35 AM.")

# Start the background auto leave task
asyncio.create_task(auto_leave())
