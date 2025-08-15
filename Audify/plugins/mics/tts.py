# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import filters
from gtts import gTTS
from Audify import app
import os

@app.on_message(filters.command('tts'))
async def text_to_speech(client, message):
    if len(message.command) < 2:
        await message.reply_text(
            "🔊 Please provide some text to convert into speech.\n\n**Usage:** `/tts your text here`"
        )
        return

    try:
        text = message.text.split(' ', 1)[1]
        tts = gTTS(text=text, lang='hi')
        tts.save('speech.mp3')
        await client.send_audio(message.chat.id, 'speech.mp3', caption="🗣️ Here's your Hindi voice note.")
        os.remove("speech.mp3")
    except Exception as e:
        await message.reply_text("⚠️ An error occurred while generating speech.")
