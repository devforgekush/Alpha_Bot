# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import filters
from pyrogram.types import Message
from Audify import app
from gpytranslate import Translator

trans = Translator()


@app.on_message(filters.command("tr"))
async def translate(_, message: Message) -> None:
    reply_msg = message.reply_to_message

    if not reply_msg:
        return await message.reply_text("📌 <b>Reply to a message to translate it.</b>")

    to_translate = reply_msg.caption or reply_msg.text
    if not to_translate:
        return await message.reply_text("⚠️ <b>Message has no text to translate.</b>")

    try:
        args = message.text.split(maxsplit=1)[1].strip().lower()
        if "//" in args:
            source, dest = args.split("//", maxsplit=1)
        else:
            source = await trans.detect(to_translate)
            dest = args
    except IndexError:
        source = await trans.detect(to_translate)
        dest = "en"
    except Exception as e:
        return await message.reply_text(f"❌ <b>Error:</b> <code>{e}</code>")

    try:
        translation = await trans(to_translate, sourcelang=source, targetlang=dest)
        reply = (
            f"🌐 <b>Translated from</b> <code>{source}</code> <b>to</b> <code>{dest}</code>:\n\n"
            f"<i>{translation.text}</i>"
        )
        await message.reply_text(reply)
    except Exception as e:
        await message.reply_text(f"❌ <b>Failed to translate:</b>\n<code>{e}</code>")
