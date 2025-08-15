# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from uuid import uuid4
from pyrogram import filters
from Audify import app
from config import BOT_USERNAME
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import pyrogram


@app.on_message(filters.command("packkang"))
async def pack_kang_handler(app: app, message):
    txt = await message.reply_text("🔄 Processing...")

    if not message.reply_to_message or not message.reply_to_message.sticker:
        return await txt.edit("❗ Please reply to a sticker.")

    sticker = message.reply_to_message.sticker

    if sticker.is_video:
        return await txt.edit("❌ Video stickers are not supported.")

    pack_title = (
        message.text.split(maxsplit=1)[1]
        if len(message.command) >= 2
        else f"{message.from_user.first_name}'s Pack"
    )

    try:
        set_name = sticker.set_name
        sticker_set = await app.invoke(
            pyrogram.raw.functions.messages.GetStickerSet(
                stickerset=pyrogram.raw.types.InputStickerSetShortName(short_name=set_name),
                hash=0
            )
        )
    except Exception as e:
        return await txt.edit(f"❌ Failed to fetch sticker set.\n`{e}`")

    stickers = []

    for doc in sticker_set.documents:
        try:
            input_doc = pyrogram.raw.types.InputDocument(
                id=doc.id,
                access_hash=doc.access_hash,
                file_reference=doc.file_reference,
            )
            emoji = next(
                attr.alt for attr in doc.attributes if isinstance(attr, pyrogram.raw.types.DocumentAttributeSticker)
            )
            stickers.append(
                pyrogram.raw.types.InputStickerSetItem(
                    document=input_doc,
                    emoji=emoji,
                )
            )
        except Exception:
            continue

    if not stickers:
        return await txt.edit("❌ Failed to collect stickers from pack.")

    short_name = f"pack_{uuid4().hex}_by_{BOT_USERNAME}"
    user_peer = await app.resolve_peer(message.from_user.id)

    try:
        await app.invoke(
            pyrogram.raw.functions.stickers.CreateStickerSet(
                user_id=user_peer,
                title=pack_title,
                short_name=short_name,
                stickers=stickers,
                masks=False
            )
        )

        await txt.edit(
            f"✅ Successfully created sticker pack!\n🧩 Total stickers: <code>{len(stickers)}</code>",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🧷 Open Pack", url=f"https://t.me/addstickers/{short_name}")]
            ])
        )
    except Exception as e:
        await txt.edit(f"❌ Error while creating pack:\n`{e}`")
