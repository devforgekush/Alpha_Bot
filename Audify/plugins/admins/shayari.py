# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import asyncio
import random
import aiohttp
from pyrogram import filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from Audify import app

# Anti-spam memory
spam_chats = []

# Minimal emoji set for reply visuals
EMOJI = [
    "🦋", "🌸", "💫", "🌷", "🍃", "🌺", "🪻", "🎈", "🕊️", "💖"
]

# ────────────────────────────────────────────────
# Fetch Shayari from API
async def get_random_shayari():
    url = "https://www.purevichar.in/api/shayari/"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    shayari_list = data.get("shayari", [])
                    if shayari_list:
                        selected = random.choice(shayari_list)
                        lines = selected.get("quote", [])
                        author = selected.get("author", "")
                        text = "\n".join(lines)
                        return f"📝 {text}\n\n👤 _{author}_"
    except Exception:
        pass
    return "❌ Shayari not available at the moment."


# ────────────────────────────────────────────────
@app.on_message(filters.command(["shayari"], prefixes=["/", "#", "@"]))
async def shayari_tag(client, message):
    chat_id = message.chat.id

    if message.chat.type != ChatType.SUPERGROUP:
        return await message.reply("ℹ️ This command works only in groups.")

    # Admin check
    try:
        member = await client.get_chat_member(chat_id, message.from_user.id)
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply("🔒 Only admins can use this command.")
    except UserNotParticipant:
        return await message.reply("🔒 Only admins can use this command.")

    # Mode check
    if message.reply_to_message and message.text:
        return await message.reply("ℹ️ Use `/shayari` or reply to a message directly.")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("ℹ️ Invalid reply target.")
    else:
        return await message.reply("ℹ️ Use `/shayari` or reply to a message.")

    if chat_id in spam_chats:
        return await message.reply("🚫 Tagging already in progress. Use `/shayarioff` to stop.")

    spam_chats.append(chat_id)
    user_count = 0
    user_text = ""

    async for user in client.get_chat_members(chat_id):
        if chat_id not in spam_chats:
            break
        if user.user.is_bot:
            continue

        user_count += 1
        user_text += f"[{user.user.first_name}](tg://user?id={user.user.id}) "

        if user_count == 1:
            if mode == "text_on_cmd":
                quote = await get_random_shayari()
                await client.send_message(chat_id, f"{user_text}\n\n{quote}")
            elif mode == "text_on_reply":
                emoji = random.choice(EMOJI)
                await msg.reply(f"[{emoji}](tg://user?id={user.user.id})")

            await asyncio.sleep(3)
            user_count = 0
            user_text = ""

    try:
        spam_chats.remove(chat_id)
    except:
        pass


# ────────────────────────────────────────────────
@app.on_message(filters.command(["shayarioff", "cancelshayari"]))
async def stop_shayari(client, message):
    chat_id = message.chat.id

    if chat_id not in spam_chats:
        return await message.reply("✅ No shayari tagging is currently running.")

    try:
        member = await client.get_chat_member(chat_id, message.from_user.id)
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply("🔒 Only admins can stop the shayari tagging.")
    except UserNotParticipant:
        return await message.reply("🔒 Only admins can stop the shayari tagging.")

    try:
        spam_chats.remove(chat_id)
    except:
        pass

    return await message.reply("🛑 Shayari tagging stopped.")
