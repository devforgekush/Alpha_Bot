# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import calendar
from io import BytesIO
from PIL import Image, ImageEnhance
from pyrogram import filters
from pyrogram.types import Message
import aiohttp

from Audify import app


async def make_carbon(code: str) -> BytesIO:
    """
    Sends the code to Carbonara API and returns a brightened PNG image in memory.
    """
    url = "https://carbonara.solopov.dev/api/cook"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"code": code}) as response:
            if response.status != 200:
                raise Exception("Carbon API error")
            image_data = await response.read()

    # Enhance brightness using PIL
    carbon_image = Image.open(BytesIO(image_data))
    enhancer = ImageEnhance.Brightness(carbon_image)
    bright_image = enhancer.enhance(1.6)

    output_image = BytesIO()
    bright_image.save(output_image, format='PNG')
    output_image.name = "calendar.png"
    output_image.seek(0)
    return output_image


@app.on_message(filters.command("calendar"))
async def send_calendar(_, message: Message):
    """
    /calendar <year> - Sends full year calendar image.
    """
    args = message.text.split()

    if len(args) != 2 or not args[1].isdigit():
        return await message.reply_text(
            "❌ Please use the correct format:\n\n<b>/calendar 2025</b>",
            quote=True,
            disable_web_page_preview=True
        )

    year = int(args[1])

    # Generate full calendar text
    cal = calendar.TextCalendar()
    full_calendar = cal.formatyear(year, 2, 1, 1, 3)

    status = await message.reply("📤 Generating calendar...")

    try:
        image = await make_carbon(full_calendar)
    except Exception as e:
        return await status.edit(f"❌ Failed to generate image.\nError: <code>{e}</code>")

    await message.reply_photo(
        photo=image,
        caption=f"🗓️ <b>Calendar for {year}</b>",
    )
    await status.delete()
