import imghdr
import os
from asyncio import gather
from traceback import format_exc

from pyrogram import filters
from pyrogram.errors import (
    PeerIdInvalid,
    ShortnameOccupyFailed,
    StickerEmojiInvalid,
    StickerPngDimensions,
    StickerPngNopng,
    UserIsBlocked,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from Audify import app
from config import BOT_USERNAME
from Audify.utils.errors import capture_err
from Audify.utils.files import (
    get_document_from_file_id,
    resize_file_to_sticker_size,
    upload_document,
)
from Audify.utils.stickerset import (
    add_sticker_to_set,
    create_sticker,
    create_sticker_set,
    get_sticker_set_by_name,
)

MAX_STICKERS = 120
SUPPORTED_TYPES = ["jpeg", "png", "webp"]


@app.on_message(filters.command("getsticker"))
@capture_err
async def sticker_image(_, message: Message):
    r = message.reply_to_message

    if not r:
        return await message.reply("🔁 Please reply to a sticker to extract it.")
    if not r.sticker:
        return await message.reply("⚠️ That’s not a sticker. Reply to a valid sticker.")

    m = await message.reply("📤 Sending the sticker file...")
    f = await r.download(f"{r.sticker.file_unique_id}.png")

    await gather(
        message.reply_photo(f),
        message.reply_document(f),
    )

    await m.delete()
    os.remove(f)


@app.on_message(filters.command("kang"))
@capture_err
async def kang(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("🔁 Reply to a sticker or image to kang it.")
    if not message.from_user:
        return await message.reply_text("❗ You are using an anonymous admin account. Please kang in private chat.")

    msg = await message.reply_text("🛠️ Kanging the sticker...")

    args = message.text.split()
    if len(args) > 1:
        sticker_emoji = str(args[1])
    elif message.reply_to_message.sticker and message.reply_to_message.sticker.emoji:
        sticker_emoji = message.reply_to_message.sticker.emoji
    else:
        sticker_emoji = "🤔"

    doc = message.reply_to_message.photo or message.reply_to_message.document
    try:
        if message.reply_to_message.sticker:
            sticker = await create_sticker(
                await get_document_from_file_id(message.reply_to_message.sticker.file_id),
                sticker_emoji,
            )
        elif doc:
            if doc.file_size > 10_000_000:
                return await msg.edit("⚠️ File size too large to kang.")

            temp_file_path = await app.download_media(doc)
            image_type = imghdr.what(temp_file_path)
            if image_type not in SUPPORTED_TYPES:
                return await msg.edit(f"❌ Format not supported: ({image_type})")

            try:
                temp_file_path = await resize_file_to_sticker_size(temp_file_path)
            except OSError:
                await msg.edit_text("❌ Failed to resize sticker image.")
                raise Exception(f"Resize error on file: {temp_file_path}")

            sticker = await create_sticker(
                await upload_document(client, temp_file_path, message.chat.id),
                sticker_emoji,
            )
            if os.path.isfile(temp_file_path):
                os.remove(temp_file_path)
        else:
            return await msg.edit("❌ Unable to kang this file format.")
    except ShortnameOccupyFailed:
        return await message.reply_text("⚠️ Change your Telegram username to continue.")
    except Exception as e:
    await message.reply_text(f"⚠️ Error: {str(e)}")
    from Audify.logger import LOGGER
    LOGGER(__name__).error(format_exc())
    return

    # Add sticker to pack
    packnum = 0
    packname = f"f{message.from_user.id}_by_{BOT_USERNAME}"
    limit = 0
    try:
        while True:
            if limit >= 50:
                return await msg.delete()

            stickerset = await get_sticker_set_by_name(client, packname)
            if not stickerset:
                await create_sticker_set(
                    client,
                    message.from_user.id,
                    f"{message.from_user.first_name[:32]}'s Kang Pack",
                    packname,
                    [sticker],
                )
            elif stickerset.set.count >= MAX_STICKERS:
                packnum += 1
                packname = f"f{packnum}_{message.from_user.id}_by_{BOT_USERNAME}"
                limit += 1
                continue
            else:
                try:
                    await add_sticker_to_set(client, stickerset, sticker)
                except StickerEmojiInvalid:
                    return await msg.edit("❌ Invalid emoji provided.")
            break

        await msg.edit(
            f"✅ Sticker added to [Pack](https://t.me/addstickers/{packname})\n🎭 Emoji: {sticker_emoji}"
        )

    except (PeerIdInvalid, UserIsBlocked):
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔗 Start Chat", url=f"https://t.me/{BOT_USERNAME}")]]
        )
        await msg.edit(
            "❗ You need to start a private chat with me first.",
            reply_markup=keyboard,
        )
    except StickerPngNopng:
        await message.reply_text("❌ The uploaded file must be in PNG format.")
    except StickerPngDimensions:
        await message.reply_text("❌ The dimensions of the PNG are invalid for a sticker.")
