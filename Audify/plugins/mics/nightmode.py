import motor.motor_asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    CallbackQuery, ChatPermissions, Message
)
from config import MONGO_DB_URI
from Audify import app

# ─── MongoDB Setup ───
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB_URI)
nightdb = mongo_client.Audify.nightmode

async def nightmode_on(chat_id: int):
    await nightdb.update_one({"chat_id": chat_id}, {"$set": {"chat_id": chat_id}}, upsert=True)

async def nightmode_off(chat_id: int):
    await nightdb.delete_one({"chat_id": chat_id})

async def is_night_enabled(chat_id: int):
    return await nightdb.find_one({"chat_id": chat_id}) is not None

async def get_nightchats():
    return await nightdb.find({}).to_list(length=1000)

# ─── Permissions ───
CLOSE_CHAT = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_polls=False,
    can_change_info=False,
    can_add_web_page_previews=False,
    can_pin_messages=False,
    can_invite_users=False
)

OPEN_CHAT = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=True,
    can_add_web_page_previews=True,
    can_pin_messages=True,
    can_invite_users=True
)

# ─── Buttons ───
nightmode_buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("✅ Enable", callback_data="add_night"),
        InlineKeyboardButton("❌ Disable", callback_data="rm_night")
    ],
    [InlineKeyboardButton("✖ Close", callback_data="close_query")]
])

# ─── Command Handler ───
@app.on_message(filters.command("nightmode") & filters.group)
async def nightmode_cmd(_, message: Message):
    status = await is_night_enabled(message.chat.id)
    txt = (
        f"**🌙 Night Mode Setup**\n\n"
        f"• Auto-locks the group at 12:00 AM (IST)\n"
        f"• Auto-unlocks at 6:00 AM (IST)\n"
        f"• Current Status: {'✅ Enabled' if status else '❌ Disabled'}"
    )
    await message.reply(txt, reply_markup=nightmode_buttons)

# ─── Callback Handler ───
@app.on_callback_query(filters.regex("^(add_night|rm_night|close_query)$"))
async def handle_night_cb(_, query: CallbackQuery):
    data = query.data
    chat_id = query.message.chat.id
    user_id = query.from_user.id

    try:
        admins = [
            m.user.id async for m in app.get_chat_members(
                chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS
            )
        ]
    except:
        return await query.answer("Unable to fetch admin list.", show_alert=True)

    if user_id not in admins:
        return await query.answer("Only group admins can use this.", show_alert=True)

    if data == "add_night":
        if await is_night_enabled(chat_id):
            return await query.answer("Already enabled.", show_alert=True)
        await nightmode_on(chat_id)
        await query.message.edit_text("✅ Night mode enabled. Group will auto-lock at 12:00 AM and unlock at 6:00 AM.")

    elif data == "rm_night":
        if not await is_night_enabled(chat_id):
            return await query.answer("Already disabled.", show_alert=True)
        await nightmode_off(chat_id)
        await query.message.edit_text("❌ Night mode disabled for this chat.")

    elif data == "close_query":
        try:
            await query.message.delete()
        except:
            await query.message.edit_text("❌ Couldn't close the message.")

# ─── Auto Lock ───
async def start_nightmode():
    chats = [int(chat["chat_id"]) for chat in await get_nightchats()]
    for cid in chats:
        try:
            await app.set_chat_permissions(cid, CLOSE_CHAT)
            await app.send_message(cid, "🌙 Group is now locked. Good night!")
        except Exception as e:
            from Audify.logger import LOGGER
            LOGGER(__name__).error(f"[!] Failed to lock group {cid}: {e}")

# ─── Auto Unlock ───
async def close_nightmode():
    chats = [int(chat["chat_id"]) for chat in await get_nightchats()]
    for cid in chats:
        try:
            await app.set_chat_permissions(cid, OPEN_CHAT)
            await app.send_message(cid, "🌞 Group is now unlocked. Good morning!")
        except Exception as e:
            LOGGER(__name__).error(f"[!] Failed to unlock group {cid}: {e}")

# ─── Scheduler ───
try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
    scheduler.add_job(start_nightmode, trigger="cron", hour=0, minute=0)
    scheduler.add_job(close_nightmode, trigger="cron", hour=6, minute=0)
    scheduler.start()
except Exception:
    # apscheduler not available; nightmode cron jobs will be disabled until dependency is installed
    pass
