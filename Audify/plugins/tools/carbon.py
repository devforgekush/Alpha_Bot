# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import aiohttp
from io import BytesIO
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Audify import app


# Generate carbon image from text
async def make_carbon(code: str) -> BytesIO:
    url = "https://carbonara.solopov.dev/api/cook"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"code": code}) as resp:
            image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image


# /carbon command handler
@app.on_message(filters.command("carbon"))
async def carbon_handler(client, message):
    replied = message.reply_to_message
    input_text = message.text.split(None, 1)[1] if len(message.command) > 1 else None

    if replied and (replied.text or replied.caption):
        target_text = replied.text or replied.caption
    elif input_text:
        target_text = input_text
    else:
        return await message.reply_text(
            "📝 Please reply to a message or give text with the command.\n\nExample: `/carbon print('Hello')`",
            quote=True
        )

    status = await message.reply("⚙️ Generating your carbon image...")

    try:
        carbon = await make_carbon(target_text)
        await status.edit("📤 Uploading image...")

        # Send image with close button
        await message.reply_photo(
            photo=carbon,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("✖️ Close", callback_data="close")]]
            )
        )
        await status.delete()
    except Exception as e:
        await status.edit(f"❌ Failed to generate image.\n\nError: `{e}`")
    finally:
        if 'carbon' in locals():
            carbon.close()
