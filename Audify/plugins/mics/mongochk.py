# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import filters
from pyrogram.types import Message
from pymongo import MongoClient
import re
from Audify import app as Audify

# MongoDB URI validation regex
mongo_url_pattern = re.compile(r'mongodb(?:\+srv)?:\/\/[^\s]+')

# /mongochk command to validate MongoDB URI
@Audify.on_message(filters.command("mongochk"))
async def mongo_check_handler(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "⚠️ <b>Missing MongoDB URI</b>\n\n"
            "Usage:\n<code>/mongochk &lt;your_mongo_uri&gt;</code>"
        )

    mongo_url = message.command[1]
    
    if not re.match(mongo_url_pattern, mongo_url):
        return await message.reply_text("❌ <b>Invalid MongoDB URI format.</b>\nPlease provide a valid URI starting with <code>mongodb://</code> or <code>mongodb+srv://</code>.")

    try:
        client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
        client.server_info()  # Attempt connection
        await message.reply_text("✅ <b>MongoDB URI is valid and connection was successful.</b>")
    except Exception as e:
        await message.reply_text(f"❌ <b>Connection failed:</b>\n<code>{str(e)}</code>")
