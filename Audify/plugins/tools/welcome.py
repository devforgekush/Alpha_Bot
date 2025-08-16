import os
import time
import random
import asyncio
from pathlib import Path
from logging import getLogger
from typing import Optional, Union

import aiohttp
from pyrogram import Client, filters, enums
from pyrogram.errors import RPCError
from pyrogram.enums import ParseMode
from pyrogram.types import ChatMemberUpdated, Message, Chat, User

from Audify import app
from Audify.utils.Audify_BAN import admin_filter

# Logger
LOGGER = getLogger(__name__)

# Welcome database mock
class WelDatabase:
    def __init__(self):
        self.data = {}

    async def find_one(self, chat_id):
        return chat_id in self.data

    async def add_wlcm(self, chat_id):
        if chat_id not in self.data:
            self.data[chat_id] = {"state": "on"}

    async def rm_wlcm(self, chat_id):
        if chat_id in self.data:
            del self.data[chat_id]

wlcm = WelDatabase()

# Temporary store
class temp:
    ME = None
    CURRENT = 2
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None

# Command to toggle welcome messages
@app.on_message(filters.command("welcome") & ~filters.private)
async def auto_state(_, message: Message):
    usage = "**ᴜsᴀɢᴇ:**\n**⦿ /welcome [on|off]**"
    if len(message.command) == 1:
        return await message.reply_text(usage)

    chat_id = message.chat.id
    user = await app.get_chat_member(chat_id, message.from_user.id)

    if user.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        A = await wlcm.find_one(chat_id)
        state = message.text.split(None, 1)[1].strip().lower()
        if state == "off":
            if A:
                await message.reply_text("**Welcome notification already disabled.**")
            else:
                await wlcm.add_wlcm(chat_id)
                await message.reply_text(f"**Disabled welcome notification in** {message.chat.title}")
        elif state == "on":
            if not A:
                await message.reply_text("**Welcome notification already enabled.**")
            else:
                await wlcm.rm_wlcm(chat_id)
                await message.reply_text(f"**Enabled welcome notification in** {message.chat.title}")
        else:
            await message.reply_text(usage)
    else:
        await message.reply("**Only group admins can change welcome settings.**")

# Greet new members with random messages
@app.on_chat_member_updated(filters.group, group=-3)
async def greet_new_member(_, member: ChatMemberUpdated):
    chat_id = member.chat.id

    # Fix: avoid crash if bot can't access member count
    try:
        count = await app.get_chat_members_count(chat_id)
    except RPCError as e:
        LOGGER.warning(f"[WELCOME] Could not fetch member count for {chat_id}: {e}")
        count = "N/A"

    A = await wlcm.find_one(chat_id)
    if A:
        return

    user: User = member.new_chat_member.user if member.new_chat_member else member.from_user

    if member.new_chat_member and not member.old_chat_member and member.new_chat_member.status != "kicked":
        try:
            if (temp.MELCOW).get(f"welcome-{chat_id}") is not None:
                try:
                    await temp.MELCOW[f"welcome-{chat_id}"].delete()
                except Exception as e:
                    LOGGER.error(e)

            # Welcome messages
            welcome_messages = [
                f"👋 Welcome {user.mention} to {member.chat.title}!",
                f"🎉 Glad to have you here, {user.mention}!",
                f"🔥 {user.mention} just landed in {member.chat.title}!",
                f"💥 Say hi to {user.mention}! Welcome aboard!",
                f"🌟 {user.mention}, welcome to the gang!",
                f"👑 A warm welcome to our newest member, {user.mention}!",
                f"🪄 Welcome {user.mention}, enjoy your stay in {member.chat.title}!",
                f"🚀 {user.mention} joined the chat. Fasten your seatbelt!",
                f"🎊 {user.mention} just arrived. Let’s celebrate!",
                f"🥳 Welcome, {user.mention}! Let the fun begin!",
                f"🤗 Glad to see you here, {user.mention}!",
                f"🫱 Give it up for {user.mention}! Welcome!",
                f"🎈 {user.mention} just joined the party in {member.chat.title}!",
                f"💫 Welcome {user.mention}! You’re going to love it here.",
                f"🙌 Say hey to {user.mention}, everyone!",
                f"🌍 {user.mention} has entered the world of {member.chat.title}.",
                f"🧡 Welcome, {user.mention}! We were waiting for you.",
                f"👾 New member alert: {user.mention} has joined {member.chat.title}!",
                f"🕺 {user.mention} just stepped in like a boss!",
                f"🧨 Boom! {user.mention} is now part of {member.chat.title}!",
                f"😎 Welcome {user.mention}! Time to vibe.",
                f"🥂 Raise your glasses for {user.mention}!",
                f"🎮 Game on! {user.mention} joined the crew!",
                f"🌊 {user.mention} just surfed into {member.chat.title}!",
                f"🦸‍♂️ {user.mention} joined us. The team is stronger now!",
                f"📢 Welcome {user.mention}! Let’s make some noise!",
                f"📬 A new message has arrived: {user.mention} joined!",
                f"🗺️ {user.mention} found their way to {member.chat.title}!",
                f"🚁 {user.mention} landed safely. Welcome!",
                f"🫡 {user.mention} has reported for duty!",
                f"🛸 Alien detected: {user.mention} joined {member.chat.title}!",
                f"🍕 Pizza for everyone! {user.mention} just joined!",
                f"🔔 Ding ding! {user.mention} is here!",
                f"🐣 Fresh member alert! Welcome {user.mention}!",
                f"💌 Welcome {user.mention}, we’ve been expecting you.",
                f"🧸 {user.mention} joined — let’s make them feel at home!",
                f"👣 New footsteps echo! {user.mention} is in!",
                f"📢 Announcement: {user.mention} is now in the chat!",
                f"🎤 {user.mention}, take the mic. Welcome!",
                f"🎩 Hats off! {user.mention} just walked in.",
                f"💬 A new voice has joined — say hi to {user.mention}!",
                f"🪄 {user.mention}, you've entered the magic circle!",
                f"🌅 A new dawn with {user.mention} in {member.chat.title}!",
                f"📍 You are now here, {user.mention}. Welcome!",
                f"💯 Welcome {user.mention}! You make us 100x better!",
                f"🎯 Bullseye! {user.mention} hit the target and joined!",
                f"🧭 Found your way here, {user.mention}? Welcome!",
                f"🔑 You just unlocked {member.chat.title}, {user.mention}!",
                f"🫶 Let’s give a warm hug to {user.mention}!",
                f"⚡ {user.mention} just boosted the energy here!",
                f"🔮 The prophecy was true — {user.mention} has arrived!"
            ]

            welcome_text = random.choice(welcome_messages)

            temp.MELCOW[f"welcome-{chat_id}"] = await app.send_message(
                chat_id,
                text=welcome_text,
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            LOGGER.error(f"Failed to send welcome message: {e}")
