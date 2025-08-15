# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from Audify import app
from config import BOT_USERNAME
from pyrogram import filters
from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from pyrogram.errors import Unauthorized

# In-memory whisper storage
whisper_db = {}

# Inline help button
switch_btn = InlineKeyboardMarkup([
    [InlineKeyboardButton("💒 Start Whisper", switch_inline_query_current_chat="")]
])

# Help response when no input provided
async def in_help():
    return [
        InlineQueryResultArticle(
            title="💒 One-Time Whisper",
            description=f"@{BOT_USERNAME} @username your whisper text here!",
            input_message_content=InputTextMessageContent(
                f"💒 Usage:\n\n@{BOT_USERNAME} @username your whisper text here!\n"
                f"(You can also use numeric user ID instead of username.)"
            ),
            reply_markup=switch_btn
        )
    ]

# Whisper inline handler
async def _whisper(client, inline_query):
    data = inline_query.query.strip()

    if len(data.split()) < 2:
        return await in_help()

    try:
        user_input, msg = data.split(None, 1)

        # Try resolving user by ID or username
        user = await client.get_users(int(user_input) if user_input.isdigit() else user_input)

        whisper_key = f"{inline_query.from_user.id}_{user.id}"
        whisper_db[whisper_key] = msg

        return [
            InlineQueryResultArticle(
                title="💒 One-Time Whisper",
                description=f"A whisper to @{user.username or user.first_name}. Only they can read this.",
                input_message_content=InputTextMessageContent(
                    f"A whisper was sent to @{user.username or user.first_name}.\nOnly they can read the message."
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💬 Show Whisper", callback_data=f"whisper_{inline_query.from_user.id}_{user.id}")]
                ])
            )
        ]

    except Exception:
        return [
            InlineQueryResultArticle(
                title="💒 One-Time Whisper",
                description="❌ Invalid username or ID!",
                input_message_content=InputTextMessageContent("❌ Invalid username or ID!"),
                reply_markup=switch_btn
            )
        ]

# Handle all inline queries
@app.on_inline_query()
async def bot_inline(client, inline_query):
    query = inline_query.query.strip()
    answers = await in_help() if not query else await _whisper(client, inline_query)
    await inline_query.answer(answers, cache_time=0)

# Handle whisper reveal button
@app.on_callback_query(filters.regex(r"^whisper_"))
async def reveal_whisper(client, query):
    try:
        _, from_user, to_user = query.data.split("_")
        from_user = int(from_user)
        to_user = int(to_user)
        user_id = query.from_user.id

        if user_id not in [from_user, to_user]:
            try:
                await client.send_message(
                    from_user,
                    f"🔐 {query.from_user.mention} tried to view your whisper."
                )
            except Unauthorized:
                pass
            return await query.answer("🚫 This whisper is not for you!", show_alert=True)

        key = f"{from_user}_{to_user}"
        msg = whisper_db.get(key)

        if not msg:
            return await query.answer("🚫 Whisper not found or already viewed.", show_alert=True)

        await query.answer(msg, show_alert=True)

        # Auto-delete after viewing by recipient
        if user_id == to_user:
            whisper_db.pop(key, None)
            await query.edit_message_text(f"🔓 {query.from_user.mention} read the whisper.")

    except Exception:
        return await query.answer("⚠️ Failed to process whisper.", show_alert=True)
