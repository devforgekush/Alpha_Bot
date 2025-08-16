try:
    import uvloop
    uvloop.install()
except Exception:
    # uvloop is optional; fall back to default asyncio event loop if unavailable
    pass

from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config
from ..logger import LOGGER


class Alphabot(Client):
    def __init__(self):
        LOGGER(__name__).info(f"🚀 Initializing Audify Bot...")
        super().__init__(
            name="Audify",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        # Validate LOGGER_ID before attempting to send startup logs
        try:
            lid = int(getattr(config, 'LOGGER_ID', 0))
        except Exception:
            lid = None

        if lid and lid != 0:
            try:
                await self.send_message(
                    chat_id=lid,
                    text=f"<u><b>✅ {self.mention} Bot Started Successfully.</b><u>\n\n🆔 <b>Bot ID:</b> <code>{self.id}</code>\n👤 <b>Name:</b> {self.name}\n🔗 <b>Username:</b> @{self.username}",
                )
                LOGGER(__name__).info(f"✅ Startup log sent successfully to {lid}")
            except (errors.ChannelInvalid, errors.PeerIdInvalid) as e:
                LOGGER(__name__).error(
                    f"❌ Failed to send startup log.\n➡️ LOGGER_ID: {lid}\n➡️ Ensure the bot is added to the specified log group or channel.\n➡️ Error: {type(e).__name__}"
                )
                LOGGER(__name__).info("ℹ️ Bot will continue running without logging capability")
            except Exception as ex:
                LOGGER(__name__).error(
                    f"❌ Unable to access the log group/channel.\n➡️ LOGGER_ID: {lid}\n➡️ Reason: {type(ex).__name__} - {str(ex)}"
                )
                LOGGER(__name__).info("ℹ️ Bot will continue running without logging capability")
        else:
            LOGGER(__name__).info("ℹ️ LOGGER_ID not configured or invalid; startup logs disabled")

        # Check bot permissions in log group
        try:
            a = await self.get_chat_member(config.LOGGER_ID, self.id)
            if a.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).warning(
                    f"⚠️ Bot is not an admin in the log group/channel {config.LOGGER_ID}.\n➡️ Please promote the bot to admin to ensure logging works properly."
                )
            else:
                LOGGER(__name__).info(f"✅ Bot has admin permissions in log group {config.LOGGER_ID}")
        except Exception as ex:
            LOGGER(__name__).warning(
                f"⚠️ Could not verify bot permissions in log group {config.LOGGER_ID}: {type(ex).__name__}"
            )
        LOGGER(__name__).info(f"✅ Audify is now running as {self.name}")

    async def stop(self):
        await super().stop()
