# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import uvloop

uvloop.install()

from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config
from ..logging import LOGGER


class Audify(Client):
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

        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=f"<u><b>✅ {self.mention} Bot Started Successfully.</b><u>\n\n🆔 <b>Bot ID:</b> <code>{self.id}</code>\n👤 <b>Name:</b> {self.name}\n🔗 <b>Username:</b> @{self.username}",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "❌ Failed to send startup log.\n➡️ Ensure the bot is added to the specified log group or channel."
            )
            exit()
        except Exception as ex:
            LOGGER(__name__).error(
                f"❌ Unable to access the log group/channel..\n➡️ Reason: {type(ex).__name__}."
            )
            exit()

        a = await self.get_chat_member(config.LOGGER_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error(
                "⚠️ Bot is not an admin in the log group/channel.\n➡️ Please promote the bot to admin to ensure logging works properly."
            )
            exit()
        LOGGER(__name__).info(f"✅ Audify is now running as {self.name}")

    async def stop(self):
        await super().stop()
