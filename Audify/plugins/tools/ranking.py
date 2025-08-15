# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import filters
from pyrogram.enums import ChatType, ParseMode
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message
)
from pymongo import MongoClient
from Audify import app
from config import MONGO_DB_URI

# MongoDB Setup
mongo_client = MongoClient(MONGO_DB_URI)
db = mongo_client["natu_rankings"]
collection = db["ranking"]

# In-memory data stores
user_data = {}
today = {}

# -------------------- Watchers -------------------- #

@app.on_message(filters.group, group=6)
async def today_watcher(_, message: Message):
    if not message.from_user:
        return  # Skip messages without a sender (e.g., anonymous admin)
    chat_id = message.chat.id
    user_id = message.from_user.id
    today.setdefault(chat_id, {}).setdefault(user_id, {"total_messages": 0})
    today[chat_id][user_id]["total_messages"] += 1


@app.on_message(filters.group, group=11)
async def overall_watcher(_, message: Message):
    if not message.from_user:
        return  # Skip messages without a sender (e.g., anonymous admin)
    user_id = message.from_user.id
    user_data.setdefault(user_id, {}).setdefault("total_messages", 0)
    user_data[user_id]["total_messages"] += 1
    collection.update_one({"_id": user_id}, {"$inc": {"total_messages": 1}}, upsert=True)


# -------------------- Utilities -------------------- #

def get_medal(rank):
    return "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "🔹"

async def get_user_display_name(user_id):
    try:
        user = await app.get_users(user_id)
        return user.mention if user.first_name else f"<a href='tg://user?id={user_id}'>User {user_id}</a>"
    except:
        return f"<a href='tg://user?id={user_id}'>User {user_id}</a>"

async def format_leaderboard(entries):
    text = "✨ <b>Overall Leaderboard</b> ✨\n━━━━━━━━━━━━━━━━━━━━\n"
    for idx, (user_id, count) in enumerate(entries, start=1):
        name = await get_user_display_name(user_id)
        medal = get_medal(idx)
        text += f"{medal} {idx}. {name} ➤ <code>{count}</code>\n"
    text += "━━━━━━━━━━━━━━━━━━━━"
    return text


# -------------------- Commands -------------------- #

@app.on_message(filters.command("today") & filters.group)
async def today_command(_, message: Message):
    chat_id = message.chat.id
    if chat_id in today and today[chat_id]:
        users_data = [
            (user_id, data["total_messages"])
            for user_id, data in today[chat_id].items()
        ]
        sorted_users = sorted(users_data, key=lambda x: x[1], reverse=True)[:10]
        text = "📊 <b>Today's Leaderboard</b>\n━━━━━━━━━━━━━━━━━━━━\n"
        for idx, (user_id, count) in enumerate(sorted_users, start=1):
            name = await get_user_display_name(user_id)
            medal = get_medal(idx)
            text += f"{medal} {idx}. {name} ➤ <code>{count}</code>\n"
        text += "━━━━━━━━━━━━━━━━━━━━"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🏆 Overall Leaderboard", callback_data="overall")],
            [InlineKeyboardButton("❌ Close", callback_data="close")],
        ])
        await message.reply_text(
            text,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    else:
        await message.reply("ℹ️ No data available for today.")


@app.on_message(filters.command("ranking") & filters.group)
async def ranking_command(_, message: Message):
    top_members = collection.find().sort("total_messages", -1).limit(10)
    entries = [(member["_id"], member["total_messages"]) for member in top_members]
    text = await format_leaderboard(entries)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Today's Leaderboard", callback_data="today")],
        [InlineKeyboardButton("❌ Close", callback_data="close")],
    ])
    await message.reply_text(
        text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )


# -------------------- Callbacks -------------------- #

@app.on_callback_query(filters.regex("^today$"))
async def today_callback(_, query: CallbackQuery):
    chat_id = query.message.chat.id
    if chat_id in today and today[chat_id]:
        users_data = [
            (user_id, data["total_messages"])
            for user_id, data in today[chat_id].items()
        ]
        sorted_users = sorted(users_data, key=lambda x: x[1], reverse=True)[:10]
        text = "📊 <b>Today's Leaderboard</b>\n━━━━━━━━━━━━━━━━━━━━\n"
        for idx, (user_id, count) in enumerate(sorted_users, start=1):
            name = await get_user_display_name(user_id)
            medal = get_medal(idx)
            text += f"{medal} {idx}. {name} ➤ <code>{count}</code>\n"
        text += "━━━━━━━━━━━━━━━━━━━━"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🏆 Overall Leaderboard", callback_data="overall")],
            [InlineKeyboardButton("❌ Close", callback_data="close")],
        ])
        await query.message.edit_text(
            text,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    else:
        await query.answer("ℹ️ No data available for today.", show_alert=True)


@app.on_callback_query(filters.regex("^overall$"))
async def overall_callback(_, query: CallbackQuery):
    top_members = collection.find().sort("total_messages", -1).limit(10)
    entries = [(member["_id"], member["total_messages"]) for member in top_members]
    text = await format_leaderboard(entries)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Today's Leaderboard", callback_data="today")],
        [InlineKeyboardButton("❌ Close", callback_data="close")],
    ])
    await query.message.edit_text(
        text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )
