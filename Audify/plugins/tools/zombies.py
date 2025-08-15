# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram import enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait
from Audify import app

# ------------------------------------------------------------------------------- #

chatQueue = []
stopProcess = False

# ------------------------------------------------------------------------------- #

@app.on_message(filters.command(["zombies", "clean"]))
async def remove(client, message):
    global stopProcess
    try:
        try:
            sender = await app.get_chat_member(message.chat.id, message.from_user.id)
            has_permissions = sender.privileges
        except:
            has_permissions = message.sender_chat

        if has_permissions:
            bot = await app.get_chat_member(message.chat.id, "self")
            if bot.status == ChatMemberStatus.MEMBER:
                await message.reply("⚠️ | I need **admin rights** to remove deleted accounts.")
            else:
                if len(chatQueue) > 30:
                    await message.reply("🚧 | I'm handling **30 groups** right now. Try again shortly.")
                else:
                    if message.chat.id in chatQueue:
                        await message.reply("♻️ | A cleanup is already running.\nUse `/stop` to restart.")
                    else:
                        chatQueue.append(message.chat.id)
                        deletedList = []
                        async for member in app.get_chat_members(message.chat.id):
                            if member.user.is_deleted:
                                deletedList.append(member.user)
                        lenDeletedList = len(deletedList)
                        if lenDeletedList == 0:
                            await message.reply("✅ | No **deleted accounts** found.")
                            chatQueue.remove(message.chat.id)
                        else:
                            k = 0
                            processTime = lenDeletedList * 1
                            temp = await app.send_message(
                                message.chat.id,
                                f"🧹 | Found **{lenDeletedList} deleted users**.\n⏱️ Estimated time: **{processTime} sec**"
                            )
                            if stopProcess:
                                stopProcess = False
                            while len(deletedList) > 0 and not stopProcess:
                                deletedAccount = deletedList.pop(0)
                                try:
                                    await app.ban_chat_member(message.chat.id, deletedAccount.id)
                                except Exception:
                                    pass
                                k += 1
                                await asyncio.sleep(10)
                            if k == lenDeletedList:
                                await message.reply("✅ | Successfully **removed all deleted accounts**.")
                                await temp.delete()
                            else:
                                await message.reply(f"✅ | Removed **{k} deleted accounts**.")
                                await temp.delete()
                            chatQueue.remove(message.chat.id)
        else:
            await message.reply("🔒 | Only **admins** can run this command.")
    except FloodWait as e:
        await asyncio.sleep(e.value)

# ------------------------------------------------------------------------------- #

@app.on_message(filters.command(["admins", "staff"]))
async def admins(client, message):
    try:
        adminList = []
        ownerList = []
        async for admin in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            if not admin.privileges.is_anonymous:
                if not admin.user.is_bot:
                    if admin.status == ChatMemberStatus.OWNER:
                        ownerList.append(admin.user)
                    else:
                        adminList.append(admin.user)
        lenAdminList = len(ownerList) + len(adminList)
        text2 = f"👥 **Group Staff - {message.chat.title}**\n\n"
        try:
            owner = ownerList[0]
            if owner.username:
                text2 += f"👑 **Owner**\n└ @{owner.username}\n\n🛡️ **Admins**\n"
            else:
                text2 += f"👑 **Owner**\n└ {owner.mention}\n\n🛡️ **Admins**\n"
        except:
            text2 += f"👑 **Owner**\n└ <i>Hidden</i>\n\n🛡️ **Admins**\n"
        if len(adminList) == 0:
            text2 += "└ <i>Admins are hidden</i>"
            await app.send_message(message.chat.id, text2)
        else:
            while len(adminList) > 1:
                admin = adminList.pop(0)
                text2 += f"├ @{admin.username}\n" if admin.username else f"├ {admin.mention}\n"
            admin = adminList.pop(0)
            text2 += f"└ @{admin.username}\n\n" if admin.username else f"└ {admin.mention}\n\n"
            text2 += f"📊 | Total Admins: **{lenAdminList}**"
            await app.send_message(message.chat.id, text2)
    except FloodWait as e:
        await asyncio.sleep(e.value)

# ------------------------------------------------------------------------------- #

@app.on_message(filters.command("bots"))
async def bots(client, message):
    try:
        botList = []
        async for bot in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BOTS):
            botList.append(bot.user)
        lenBotList = len(botList)
        text3 = f"🤖 **Bot List - {message.chat.title}**\n\n"
        while len(botList) > 1:
            bot = botList.pop(0)
            text3 += f"├ @{bot.username}\n"
        bot = botList.pop(0)
        text3 += f"└ @{bot.username}\n\n"
        text3 += f"📦 | Total Bots: **{lenBotList}**"
        await app.send_message(message.chat.id, text3)
    except FloodWait as e:
        await asyncio.sleep(e.value)

# ------------------------------------------------------------------------------- #
