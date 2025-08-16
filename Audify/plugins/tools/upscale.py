import os
import aiohttp
import asyncio
from pyrogram import filters
from pyrogram.types import Message
from Audify import app

API_URL = "https://api.itsrose.life/image/upscale"

@app.on_message(filters.command(["upscale", "enhance"]) & filters.reply)
async def upscale_image(_, message: Message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.reply_text("❌ Please reply to a photo with /upscale or /enhance.", quote=True)

    msg = await message.reply("🖼️ Upscaling the image... Please wait ⏳")

    try:
        photo = message.reply_to_message.photo
        download_path = await photo.download()
        upscale_path = f"upscaled_{message.chat.id}.jpg"

        # Send image to API
        async with aiohttp.ClientSession() as session:
            with open(download_path, "rb") as f:
                form = aiohttp.FormData()
                form.add_field("image", f, filename="image.jpg", content_type="image/jpeg")

                async with session.post(API_URL, data=form) as response:
                    if response.status != 200:
                        return await msg.edit(f"❌ Upscaling failed. API responded with status {response.status}.")
                    result = await response.json()

        upscale_url = result.get("output")
        if not upscale_url:
            return await msg.edit("❌ Upscaling failed. No image returned.")

        # Download upscaled image
        async with aiohttp.ClientSession() as session:
            async with session.get(upscale_url) as r:
                if r.status != 200:
                    return await msg.edit("❌ Failed to download upscaled image.")
                with open(upscale_path, "wb") as f:
                    f.write(await r.read())

        await message.reply_photo(upscale_path, caption="✨ Image successfully enhanced using AI Upscaler.")
        await msg.delete()

    except Exception as e:
        await msg.edit(f"❌ Error during upscaling:\n<code>{str(e)}</code>")

    finally:
        for f in [download_path, upscale_path]:
            if f and os.path.exists(f):
                os.remove(f)
