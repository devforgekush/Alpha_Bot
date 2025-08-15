# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from io import BytesIO
from os import path, remove
from time import time

import img2pdf
from PIL import Image
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from Audify import app
from Audify.utils.errors import capture_err
from Audify.core.sections import section

# ⏹ Inline Close Button
CLOSE_BTN = InlineKeyboardMarkup([
    [InlineKeyboardButton("⏹ Close", callback_data="close")]
])


async def convert(main_message: Message, reply_messages, status_message: Message, start_time: float):
    m = status_message
    documents = []

    for message in reply_messages:
        if message.document and message.document.mime_type.startswith("image"):
            file_path = await message.download()
        elif message.photo:
            file_path = await message.download()
        else:
            return await m.edit("⚠️ Not a valid image or photo. Aborting...")

        if path.getsize(file_path) > 5_000_000:
            return await m.edit("⚠️ Image size too large (max 5MB). Aborting...")

        documents.append(file_path)

    for img_path in documents:
        img = Image.open(img_path).convert("RGB")
        img.save(img_path, "JPEG", quality=100)

    pdf = BytesIO(img2pdf.convert(documents))
    pdf.name = "Audify.pdf"

    if len(main_message.command) >= 2:
        names = main_message.text.split(None, 1)[1]
        pdf.name = names if names.endswith(".pdf") else f"{names}.pdf"

    elapsed = round(time() - start_time, 2)

    await main_message.reply_document(
        document=pdf,
        caption=section(
            "📄 Image to PDF",
            body={
                "📘 Title": pdf.name,
                "📦 Size": f"{pdf.getbuffer().nbytes / (10**6):.2f} MB",
                "🖼️ Pages": len(documents),
                "⏱️ Time Taken": f"{elapsed}s",
            },
        ),
        reply_markup=CLOSE_BTN,
    )

    await m.delete()
    pdf.close()
    for file in documents:
        if path.exists(file):
            remove(file)


@app.on_message(filters.command("pdf"))
@capture_err
async def img_to_pdf(_, message: Message):
    reply = message.reply_to_message
    if not reply:
        return await message.reply("⚠️ Reply to one or more image documents or photos to convert into PDF.")

    m = await message.reply_text("⏳ Converting image(s) to PDF...")
    start_time = time()

    if reply.media_group_id:
        messages = await app.get_media_group(message.chat.id, reply.id)
        return await convert(message, messages, m, start_time)

    return await convert(message, [reply], m, start_time)
