# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import Message
from Audify import app
from httpx import AsyncClient, Timeout
import re, random

# ──────────────── Quote API HTTP Client ────────────────
fetch = AsyncClient(
    http2=True,
    verify=False,
    headers={
        "Accept-Language": "id-ID",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edge/107.0.1418.42",
    },
    timeout=Timeout(20),
)

class QuotlyException(Exception):
    pass

# ──────────────── Helpers to extract message data ────────────────
async def get_message_sender_id(ctx: Message):
    if ctx.forward_date:
        if ctx.forward_sender_name:
            return 1
        elif ctx.forward_from:
            return ctx.forward_from.id
        elif ctx.forward_from_chat:
            return ctx.forward_from_chat.id
        else:
            return 1
    elif ctx.from_user:
        return ctx.from_user.id
    elif ctx.sender_chat:
        return ctx.sender_chat.id
    else:
        return 1

async def get_message_sender_name(ctx: Message):
    if ctx.forward_date:
        if ctx.forward_sender_name:
            return ctx.forward_sender_name
        elif ctx.forward_from:
            return f"{ctx.forward_from.first_name} {ctx.forward_from.last_name}" if ctx.forward_from.last_name else ctx.forward_from.first_name
        elif ctx.forward_from_chat:
            return ctx.forward_from_chat.title
        else:
            return ""
    elif ctx.from_user:
        return f"{ctx.from_user.first_name} {ctx.from_user.last_name}" if ctx.from_user.last_name else ctx.from_user.first_name
    elif ctx.sender_chat:
        return ctx.sender_chat.title
    else:
        return ""

async def get_message_sender_username(ctx: Message):
    if ctx.forward_date:
        if (
            not ctx.forward_sender_name and not ctx.forward_from
            and ctx.forward_from_chat and ctx.forward_from_chat.username
        ):
            return ctx.forward_from_chat.username
        elif (
            not ctx.forward_sender_name and not ctx.forward_from
            and ctx.forward_from_chat or ctx.forward_sender_name or not ctx.forward_from
        ):
            return ""
        else:
            return ctx.forward_from.username or ""
    elif ctx.from_user and ctx.from_user.username:
        return ctx.from_user.username
    elif (ctx.from_user or ctx.sender_chat and not ctx.sender_chat.username or not ctx.sender_chat):
        return ""
    else:
        return ctx.sender_chat.username

async def get_message_sender_photo(ctx: Message):
    if ctx.forward_date:
        if (not ctx.forward_sender_name and not ctx.forward_from and ctx.forward_from_chat and ctx.forward_from_chat.photo):
            return {
                "small_file_id": ctx.forward_from_chat.photo.small_file_id,
                "small_photo_unique_id": ctx.forward_from_chat.photo.small_photo_unique_id,
                "big_file_id": ctx.forward_from_chat.photo.big_file_id,
                "big_photo_unique_id": ctx.forward_from_chat.photo.big_photo_unique_id,
            }
        elif (not ctx.forward_sender_name and not ctx.forward_from and ctx.forward_from_chat or ctx.forward_sender_name or not ctx.forward_from):
            return ""
        else:
            return ({
                "small_file_id": ctx.forward_from.photo.small_file_id,
                "small_photo_unique_id": ctx.forward_from.photo.small_photo_unique_id,
                "big_file_id": ctx.forward_from.photo.big_file_id,
                "big_photo_unique_id": ctx.forward_from.photo.big_photo_unique_id,
            } if ctx.forward_from.photo else "")
    elif ctx.from_user and ctx.from_user.photo:
        return {
            "small_file_id": ctx.from_user.photo.small_file_id,
            "small_photo_unique_id": ctx.from_user.photo.small_photo_unique_id,
            "big_file_id": ctx.from_user.photo.big_file_id,
            "big_photo_unique_id": ctx.from_user.photo.big_photo_unique_id,
        }
    elif (ctx.from_user or ctx.sender_chat and not ctx.sender_chat.photo or not ctx.sender_chat):
        return ""
    else:
        return {
            "small_file_id": ctx.sender_chat.photo.small_file_id,
            "small_photo_unique_id": ctx.sender_chat.photo.small_photo_unique_id,
            "big_file_id": ctx.sender_chat.photo.big_file_id,
            "big_photo_unique_id": ctx.sender_chat.photo.big_photo_unique_id,
        }

async def get_text_or_caption(ctx: Message):
    return ctx.text or ctx.caption or ""

# ──────────────── Quote JSON Builder ────────────────
async def pyrogram_to_quotly(messages, is_reply=False, format_type="png", bg_color="#1b1429"):
    if not isinstance(messages, list):
        messages = [messages]
    payload = {
        "type": "quote",
        "format": format_type,
        "backgroundColor": bg_color,
        "messages": [],
    }
    for message in messages:
        msg_dict = {
            "chatId": await get_message_sender_id(message),
            "text": await get_text_or_caption(message),
            "avatar": True,
            "entities": [
                {"type": e.type.name.lower(), "offset": e.offset, "length": e.length}
                for e in (message.entities or message.caption_entities or [])
            ],
            "from": {
                "id": await get_message_sender_id(message),
                "name": await get_message_sender_name(message),
                "username": await get_message_sender_username(message),
                "type": message.chat.type.name.lower(),
                "photo": await get_message_sender_photo(message),
            },
            "replyMessage": {
                "name": await get_message_sender_name(message.reply_to_message),
                "text": await get_text_or_caption(message.reply_to_message),
                "chatId": await get_message_sender_id(message.reply_to_message),
            } if message.reply_to_message and is_reply else {},
        }
        payload["messages"].append(msg_dict)

    r = await fetch.post("https://bot.lyo.su/quote/generate.png", json=payload)
    if not r.is_error:
        return r.read()
    else:
        raise QuotlyException(r.json())

# ──────────────── Argument Parser ────────────────
def parse_q_args(text):
    args = text.split()[1:] if len(text.split()) > 1 else []
    flags = {
        "count": 1,
        "reply": False,
        "format": "webp",
        "bg_color": "#1b1429",
    }
    common_colors = [
        "red", "blue", "green", "yellow", "purple", "orange", "pink", "black", "white",
        "gray", "cyan", "brown", "lime", "teal", "violet"
    ]
    for arg in args:
        a = arg.lower()
        if a.isdigit():
            flags["count"] = max(1, min(10, int(a)))
        elif a in ("r", "reply"):
            flags["reply"] = True
        elif a in ("i", "img", "p", "png"):
            flags["format"] = "png"
        elif a == "random":
            flags["bg_color"] = random.choice(common_colors)
        elif a in common_colors:
            flags["bg_color"] = a
        elif re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", a):
            flags["bg_color"] = a
    return flags

# ──────────────── Main Command Handler ────────────────
@app.on_message(filters.command("q"))
async def msg_quotly_cmd(self: app, ctx: Message):
    if not ctx.reply_to_message:
        return await ctx.reply("❗ **Please reply to or forward the message you'd like to quote ✨**")
    try:
        flags = parse_q_args(ctx.text)
        msg_ids = range(ctx.reply_to_message.id, ctx.reply_to_message.id + flags["count"])
        messages = [
            msg for msg in await self.get_messages(ctx.chat.id, list(msg_ids))
            if not msg.empty and not msg.media
        ]
        quote_bytes = await pyrogram_to_quotly(
            messages,
            is_reply=flags["reply"],
            format_type=flags["format"],
            bg_color=flags["bg_color"]
        )
        out_file = BytesIO(quote_bytes)
        out_file.name = f"quote.{flags['format']}"
        if flags["format"] == "webp":
            return await ctx.reply_sticker(out_file)
        return await ctx.reply_document(out_file)
    except Exception as e:
        return await ctx.reply_text(f"❌ Failed: {e}")
