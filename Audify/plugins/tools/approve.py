from pyrogram import filters
from pyrogram.types import Message
from Audify import app
from Audify.utils.database import authuserdb
from Audify.utils.Audify_BAN import admin_filter


async def get_approved_users(chat_id: int):
    chat = await authuserdb.find_one({"chat_id": chat_id})
    return chat.get("approved_users", []) if chat else []


async def is_user_approved(chat_id: int, user_id: int):
    users = await get_approved_users(chat_id)
    return user_id in users


async def approve_user(chat_id: int, user_id: int):
    await authuserdb.update_one(
        {"chat_id": chat_id},
        {"$addToSet": {"approved_users": user_id}},
        upsert=True,
    )


async def unapprove_user(chat_id: int, user_id: int):
    await authuserdb.update_one(
        {"chat_id": chat_id},
        {"$pull": {"approved_users": user_id}},
        upsert=True,
    )


async def clear_all_approvals(chat_id: int):
    await authuserdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"approved_users": []}},
        upsert=True,
    )


@app.on_message(filters.command("approve") & admin_filter)
async def approve_cmd(_, message: Message):
    if not message.reply_to_message:
        return await message.reply("❗ Reply to a user to approve them.")
    user_id = message.reply_to_message.from_user.id
    await approve_user(message.chat.id, user_id)
    await message.reply(f"✅ [User](tg://user?id={user_id}) has been approved.")


@app.on_message(filters.command("unapprove") & admin_filter)
async def unapprove_cmd(_, message: Message):
    if not message.reply_to_message:
        return await message.reply("❗ Reply to a user to unapprove them.")
    user_id = message.reply_to_message.from_user.id
    await unapprove_user(message.chat.id, user_id)
    await message.reply(f"❌ [User](tg://user?id={user_id}) has been unapproved.")


@app.on_message(filters.command("approval") & admin_filter)
async def check_approval_cmd(_, message: Message):
    if not message.reply_to_message:
        return await message.reply("❗ Reply to a user to check their approval status.")
    user_id = message.reply_to_message.from_user.id
    approved = await is_user_approved(message.chat.id, user_id)
    status = "✅ Approved" if approved else "🚫 Not Approved"
    await message.reply(f"{status}: [User](tg://user?id={user_id})")


@app.on_message(filters.command("approved") & admin_filter)
async def approved_list_cmd(_, message: Message):
    users = await get_approved_users(message.chat.id)
    if not users:
        return await message.reply("📭 No approved users found.")
    msg = "✅ Approved Users:\n\n"
    for uid in users:
        msg += f"• [User](tg://user?id={uid}) (`{uid}`)\n"
    await message.reply(msg)


@app.on_message(filters.command("unapproveall") & admin_filter)
async def unapprove_all_cmd(_, message: Message):
    await clear_all_approvals(message.chat.id)
    await message.reply("🗑️ All approved users have been unapproved.")
