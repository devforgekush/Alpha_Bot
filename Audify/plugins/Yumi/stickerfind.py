# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import Client, filters
from Audify import app

@app.on_message(filters.command("st"))
async def generate_sticker(client, message):
    if len(message.command) == 2:
        sticker_id = message.command[1]
        try:
            await client.send_sticker(message.chat.id, sticker=sticker_id)
        except Exception as e:
            await message.reply_text(f"⚠️ An error occurred while sending the sticker:\n`{e}`")
    else:
        await message.reply_text("❗ Please provide a sticker ID after the `/st` command.\nExample: `/st CAACAgUAAxkBA...`")
