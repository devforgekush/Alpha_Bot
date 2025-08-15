# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton as ikb, InlineKeyboardMarkup as ikm, Message
from pyrogram.enums import ChatAction
from requests import get
import pyshorteners

from Audify import app

shortener = pyshorteners.Shortener()

@app.on_message(filters.command("short"))
async def short_urls(client, message: Message):
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)

    if len(message.command) < 2:
        return await message.reply_text(
            "🔗 Please provide a valid URL to shorten.\n\n**Usage:**\n`/short https://example.com`"
        )

    link = message.command[1]

    try:
        tiny_link = shortener.tinyurl.short(link)
        dagd_link = shortener.dagd.short(link)
        clckru_link = shortener.clckru.short(link)

        keyboard = ikm([
            [ikb("🔹 TinyURL", url=tiny_link)],
            [ikb("🔹 Dagd", url=dagd_link), ikb("🔹 Clck.ru", url=clckru_link)]
        ])

        await message.reply_text(
            "✅ Your shortened links are ready:", reply_markup=keyboard
        )

    except Exception:
        await message.reply_text(
            "⚠️ Failed to shorten the URL. Please make sure it's valid and try again."
        )


@app.on_message(filters.command("unshort"))
async def unshort_url(client, message: Message):
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)

    if len(message.command) < 2:
        return await message.reply_text(
            "🔍 Please provide a shortened URL to expand.\n\n**Usage:**\n`/unshort https://tinyurl.com/xyz`"
        )

    short_url = message.command[1]

    try:
        final_url = get(short_url, allow_redirects=True).url
        keyboard = ikm([[ikb("🔗 Open Link", url=final_url)]])

        await message.reply_text(
            f"✅ Unshortened URL:\n`{final_url}`", reply_markup=keyboard
        )

    except Exception as e:
        await message.reply_text(
            f"⚠️ Error while expanding the URL:\n`{e}`"
        )
