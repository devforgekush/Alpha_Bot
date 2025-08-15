# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.raw.functions.messages import DeleteHistory

from Audify import userbot as us, app
from Audify.core.userbot import assistants


# ➤ /sg command handler
@app.on_message(filters.command("sg"))
async def sg(client: Client, message: Message):
    replied = message.reply_to_message
    args = message.text.split()

    if not replied and len(args) < 2:
        return await message.reply_text(
            "❌ Please reply to a user or provide a username/user ID.\n\n**Usage:** `/sg @username`",
            quote=True,
        )

    target = replied.from_user.id if replied else args[1]

    lol = await message.reply_text("🔍 Querying SangMata...")

    try:
        user = await client.get_users(target)
    except Exception:
        return await lol.edit("❌ Invalid user. Please check the username or ID.")

    sangmata_bots = ["sangmata_bot", "sangmata_beta_bot"]
    selected_bot = random.choice(sangmata_bots)

    if 1 not in assistants:
        return await lol.edit("⚠️ Assistant not started.")

    ubot = us.one

    try:
        msg = await ubot.send_message(selected_bot, str(user.id))
        await msg.delete()
    except Exception as e:
        return await lol.edit(f"⚠️ Error sending to SangMata:\n`{str(e)}`")

    await asyncio.sleep(2)

    found = False
    async for result in ubot.search_messages(selected_bot):
        if result.text:
            await message.reply_text(
                text=f"📜 {result.text}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("⏹ Close", callback_data="close")]
                ]),
                quote=True
            )
            found = True
            break

    if not found:
        await message.reply_text(
            "❌ No name history found.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⏹ Close", callback_data="close")]
            ]),
            quote=True
        )

    try:
        peer = await ubot.resolve_peer(selected_bot)
        await ubot.send(DeleteHistory(peer=peer, max_id=0, revoke=True))
    except Exception:
        pass

    await lol.delete()
