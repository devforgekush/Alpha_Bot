# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import Client, filters
from Audify import app
from config import BOT_USERNAME


def hex_to_text(hex_string):
    try:
        text = bytes.fromhex(hex_string).decode('utf-8')
        return text
    except Exception as e:
        return f"Error decoding hex: {str(e)}"


def text_to_hex(text):
    hex_representation = ' '.join(format(ord(char), 'x') for char in text)
    return hex_representation


@app.on_message(filters.command("code"))
async def convert_text(_, message):
    if len(message.command) > 1:
        input_text = " ".join(message.command[1:])

        hex_representation = text_to_hex(input_text)
        decoded_text = hex_to_text(input_text)

        response_text = (
            f"🔹 **Original Text**:\n`{input_text}`\n\n"
            f"🔸 **Hex Representation**:\n`{hex_representation}`\n\n"
            f"🔹 **Decoded Text (if input was hex)**:\n`{decoded_text}`\n\n"
            f"🔧 Powered by ➤ @{BOT_USERNAME}"
        )

        await message.reply_text(response_text)
    else:
        await message.reply_text("ℹ️ Please provide some text after the `/code` command.")
