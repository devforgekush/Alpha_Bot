# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from Audify import app  # Change to Audify if needed

# Close button markup
CLOSE_BTN = InlineKeyboardMarkup([[InlineKeyboardButton("⏹ Close", callback_data="close")]])

@app.on_message(filters.command("mmf"))
async def mmf(_, message: Message):
    reply = message.reply_to_message

    if not reply or not (reply.photo or reply.sticker or (reply.document and reply.document.mime_type.startswith("image/"))):
        return await message.reply_text("📸 Please reply to a valid image, sticker, or photo file.")

    if len(message.text.split(None, 1)) < 2:
        return await message.reply_text("✏️ Provide some text after `/mmf` to generate a meme.\n\nExample:\n`/mmf top ; bottom`")

    msg = await message.reply_text("🎨 Creating your meme...")

    text = message.text.split(None, 1)[1]
    file = await app.download_media(reply)

    meme = await drawText(file, text)
    await message.reply_document(document=meme, caption="✅ Meme created successfully!", reply_markup=CLOSE_BTN)

    await msg.delete()
    os.remove(meme)


async def drawText(image_path, text):
    img = Image.open(image_path)
    os.remove(image_path)

    i_width, i_height = img.size

    font_path = "./Audify/assets/default.ttf" if os.name != "nt" else "arial.ttf"
    m_font = ImageFont.truetype(font_path, int((70 / 640) * i_width))

    if ";" in text:
        upper_text, lower_text = text.split(";", 1)
    else:
        upper_text = text
        lower_text = ""

    draw = ImageDraw.Draw(img)
    current_h, pad = 10, 5

    if upper_text:
        for u_text in textwrap.wrap(upper_text.strip(), width=15):
            u_width, u_height = draw.textsize(u_text, font=m_font)
            positions = [
                (((i_width - u_width) / 2) - 2, int((current_h / 640) * i_width)),
                (((i_width - u_width) / 2) + 2, int((current_h / 640) * i_width)),
                (((i_width - u_width) / 2), int(((current_h / 640) * i_width)) - 2),
                (((i_width - u_width) / 2), int(((current_h / 640) * i_width)) + 2)
            ]
            for pos in positions:
                draw.text(pos, u_text, font=m_font, fill=(0, 0, 0))
            draw.text(((i_width - u_width) / 2, int((current_h / 640) * i_width)), u_text, font=m_font, fill=(255, 255, 255))
            current_h += u_height + pad

    if lower_text:
        for l_text in textwrap.wrap(lower_text.strip(), width=15):
            u_width, u_height = draw.textsize(l_text, font=m_font)
            base_y = i_height - u_height - int((20 / 640) * i_width)
            positions = [
                (((i_width - u_width) / 2) - 2, base_y),
                (((i_width - u_width) / 2) + 2, base_y),
                (((i_width - u_width) / 2), base_y - 2),
                (((i_width - u_width) / 2), base_y + 2)
            ]
            for pos in positions:
                draw.text(pos, l_text, font=m_font, fill=(0, 0, 0))
            draw.text(((i_width - u_width) / 2, base_y), l_text, font=m_font, fill=(255, 255, 255))
            current_h += u_height + pad

    output_path = "memify.webp"
    img.save(output_path, "webp")
    return output_path
