# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Audify import app
from config import SUPPORT_CHAT

BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("💬 Support", url=SUPPORT_CHAT)]
])

# Fun commands with percentage/random meters
PREFIXES = ["!", "/", "."]

def mention_user(user):
    return f"[{user.first_name}](tg://user?id={user.id})"

# ── Command: /horny ───────────────────────────────
@app.on_message(filters.command("horny", prefixes=PREFIXES))
async def horny(_, message):
    if not message.from_user:
        return
    percent = random.randint(1, 100)
    await message.reply_text(
        f"🔥 {mention_user(message.from_user)} is {percent}% horny!",
        reply_markup=BUTTON,
        disable_web_page_preview=True,
        quote=True
    )

# ── Command: /gay ───────────────────────────────
@app.on_message(filters.command("gay", prefixes=PREFIXES))
async def gay(_, message):
    if not message.from_user:
        return
    percent = random.randint(1, 100)
    await message.reply_text(
        f"💅 {mention_user(message.from_user)} is {percent}% gay!",
        reply_markup=BUTTON,
        disable_web_page_preview=True,
        quote=True
    )

# ── Command: /cute ───────────────────────────────
@app.on_message(filters.command("cute", prefixes=PREFIXES))
async def cute(_, message):
    if not message.from_user:
        return
    percent = random.randint(1, 100)
    await message.reply_text(
        f"🧸 {mention_user(message.from_user)} is {percent}% cute!",
        reply_markup=BUTTON,
        disable_web_page_preview=True,
        quote=True
    )

# ── Command: /lesbo ───────────────────────────────
@app.on_message(filters.command("lesbo", prefixes=PREFIXES))
async def lesbo(_, message):
    if not message.from_user:
        return
    percent = random.randint(1, 100)
    await message.reply_text(
        f"🌈 {mention_user(message.from_user)} is {percent}% lesbian!",
        reply_markup=BUTTON,
        disable_web_page_preview=True,
        quote=True
    )

# ── Command: /depressed ───────────────────────────────
@app.on_message(filters.command("depressed", prefixes=PREFIXES))
async def depressed(_, message):
    if not message.from_user:
        return
    percent = random.randint(1, 100)
    await message.reply_text(
        f"😔 {mention_user(message.from_user)} is feeling {percent}% depressed today.",
        reply_markup=BUTTON,
        disable_web_page_preview=True,
        quote=True
    )

# ── Command: /rand ───────────────────────────────
@app.on_message(filters.command("rand", prefixes=PREFIXES))
async def rand(_, message):
    if not message.from_user:
        return
    percent = random.randint(1, 100)
    await message.reply_text(
        f"🎲 {mention_user(message.from_user)} has a randomness level of {percent}%.",
        reply_markup=BUTTON,
        disable_web_page_preview=True,
        quote=True
    )

# ── Command: /bkl ───────────────────────────────
@app.on_message(filters.command("bkl", prefixes=PREFIXES))
async def bkl(_, message):
    if not message.from_user:
        return
    percent = random.randint(1, 100)
    await message.reply_text(
        f"🤪 {mention_user(message.from_user)} is {percent}% baklol!",
        reply_markup=BUTTON,
        disable_web_page_preview=True,
        quote=True
    )

# ── Command: /boobs ───────────────────────────────
@app.on_message(filters.command("boobs", prefixes=PREFIXES))
async def boobs(_, message):
    if not message.from_user:
        return
    size = random.randint(1, 100)
    await message.reply_text(
        f"👙 {mention_user(message.from_user)}'s boob size is {size}!",
        reply_markup=BUTTON,
        disable_web_page_preview=True,
        quote=True
    )

# ── Command: /dick ───────────────────────────────
@app.on_message(filters.command("dick", prefixes=PREFIXES))
async def dick(_, message):
    if not message.from_user:
        return
    size = random.randint(1, 100)
    await message.reply_text(
        f"🍆 {mention_user(message.from_user)}'s dick size is {size} cm!",
        reply_markup=BUTTON,
        disable_web_page_preview=True,
        quote=True
    )

# ── Command: /sigma ───────────────────────────────
@app.on_message(filters.command("sigma", prefixes=PREFIXES))
async def sigma(_, message):
    if not message.from_user:
        return
    percent = random.randint(1, 100)
    await message.reply_text(
        f"😎 {mention_user(message.from_user)} is {percent}% sigma!",
        reply_markup=BUTTON,
        disable_web_page_preview=True,
        quote=True
    )
