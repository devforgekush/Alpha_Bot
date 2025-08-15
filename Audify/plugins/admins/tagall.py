# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import asyncio
import random
from pyrogram import filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from Audify import app

# Global spam control list
spam_chats = []

# High-rich emoji set for optional reply styling
EMOJI = [
    "🦋", "🌸", "💫", "🌷", "🍃", "🌺", "🪻", "🎈", "🕊️", "💖"
]

# High-rich tag messages
TAGMES = [
    "Hey baby, where are you? 🤗",
    "Did you fall asleep? Come online! 🥱",
    "Join VC? Let's talk a bit 😃",
    "Had your meal yet? 🥲",
    "How’s everyone at home? 🥺",
    "I’ve been missing you a lot 🤭",
    "What's up these days? 🤨",
    "Can you help me set up something? 🙂",
    "What's your name? 🥲",
    "Did you have breakfast? 😋",
    "Kidnap me to your group, please 😍",
    "Your partner is looking for you, come online 😅",
    "Wanna be friends with me? 🤔",
    "Did you sleep already? 🙄",
    "Play a song please 😕",
    "Where are you from? 🙃",
    "Namaste, how’s your day? 😛",
    "Hello baby, what’s up? 🤔",
    "Do you know who my owner is? 👀",
    "Let’s play some games 🤗",
    "How are you doing today? 😇",
    "What’s your mom doing now? 🤭",
    "Will you talk to me? 🥺",
    "Hey you, come online 😶",
    "Is today a holiday? 🤔",
    "Good morning! 😜",
    "Need a favor from you 🙂",
    "Play a song for us 😪",
    "Nice to meet you ☺",
    "Hi there 🙊",
    "Did you finish your studies? 😺",
    "Say something, yrr 🥲",
    "Who’s Sonali..? 😅",
    "Can I get your picture? 😅",
    "Did your mom come in? 😆",
    "How’s your bhabhi doing? 😉",
    "I love you 🙈",
    "Do you love me too..? 👀",
    "When’s Rakhi again? 🙉",
    "Should I sing a song for you? 😹",
    "Come online, I’m playing your fav song 😻",
    "Using Instagram much? 🙃",
    "Can I get your WhatsApp number..? 😕",
    "What kind of music do you enjoy? 🙃",
    "All work done today? 🙃",
    "Where are you from? 😊",
    "Hey, listen! 🧐",
    "Can you help me with one task?",
    "Don’t talk to me anymore 😠",
    "How are your parents? ❤️",
    "What happened..? 👱",
    "Missing you a lot 🤧❣️",
    "Did you forget me? 😏",
]

# ────────────────────────────────────────────────
@app.on_message(filters.command(
    ["tagall", "spam", "tagmember", "utag", "stag", "hftag", "bstag", "eftag", "tag", "etag", "atag"],
    prefixes=["/", "@", "#"]
))
async def mention_all(client, message):
    chat_id = message.chat.id

    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("ℹ️ This command works only in groups.")

    # Check if user is admin
    try:
        member = await client.get_chat_member(chat_id, message.from_user.id)
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply("🔒 Only admins can mention all members.")
    except UserNotParticipant:
        return await message.reply("🔒 Only admins can mention all members.")

    # Tagging logic
    if message.reply_to_message and message.text:
        return await message.reply("⚠️ Use `/tagall` or reply only without extra text.")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
    else:
        return await message.reply("ℹ️ Use `/tagall` or reply to a message.")

    if chat_id in spam_chats:
        return await message.reply("🚫 Tagging already in progress. Use `/tagoff` to stop.")

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
                final_text = f"{user_text}\n\n{random.choice(TAGMES)}"
                await client.send_message(chat_id, final_text)
            elif mode == "text_on_reply":
                await msg.reply(f"[{random.choice(EMOJI)}](tg://user?id={user.user.id})")

            await asyncio.sleep(4)
            user_count = 0
            user_text = ""

    try:
        spam_chats.remove(chat_id)
    except:
        pass


# ────────────────────────────────────────────────
@app.on_message(filters.command(["tagoff", "tagstop"]))
async def cancel_tag(client, message):
    chat_id = message.chat.id

    if chat_id not in spam_chats:
        return await message.reply("✅ No tag process is running currently.")

    try:
        member = await client.get_chat_member(chat_id, message.from_user.id)
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply("🔒 Only admins can stop the tag process.")
    except UserNotParticipant:
        return await message.reply("🔒 Only admins can stop the tag process.")

    try:
        spam_chats.remove(chat_id)
    except:
        pass

    return await message.reply("🛑 Tagging process stopped successfully.")
