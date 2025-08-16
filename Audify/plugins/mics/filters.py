import re
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from Audify import app
from config import BOT_USERNAME
from Audify.utils.Audify_BAN import admin_filter
from Audify.mongo.filtersdb import (
    add_filter_db,
    get_filters_list,
    get_filter,
    stop_db,
    stop_all_db,
)
from Audify.utils.yumidb import user_admin


# ➤ Get reply message info
async def GetFIlterMessage(message):
    reply = message.reply_to_message

    if not reply:
        return None, None, None

    if reply.text:
        return reply.text, reply.text, "text"

    if reply.photo:
        return reply.photo.file_id, reply.caption or None, "photo"

    if reply.video:
        return reply.video.file_id, reply.caption or None, "video"

    if reply.document:
        return reply.document.file_id, reply.caption or None, "document"

    return None, None, None


# ➤ Send the filter message back to chat
async def SendFilterMessage(message, filter_name, content, text, data_type):
    if data_type == "text":
        return await message.reply(text)

    elif data_type == "photo":
        return await message.reply_photo(photo=content, caption=text or None)

    elif data_type == "video":
        return await message.reply_video(video=content, caption=text or None)

    elif data_type == "document":
        return await message.reply_document(document=content, caption=text or None)

    else:
        return await message.reply("❌ Failed to send the filter content.")


# ── Add a Filter ────────────────────────────────
@app.on_message(filters.command("filter") & admin_filter)
@user_admin
async def add_filter(_, message: Message):
    chat_id = message.chat.id

    if not message.reply_to_message:
        return await message.reply("❌ Please reply to the message you want to save as a filter.")

    if len(message.command) < 2:
        return await message.reply("❌ You need to give the filter a name!\n\nExample: `/filter welcome`")

    filter_name = message.command[1].lower()
    content, text, data_type = await GetFIlterMessage(message)

    if not content:
        return await message.reply("❌ Unsupported message type. Please reply to text, photo, video, or document.")

    await add_filter_db(chat_id, filter_name, content, text, data_type)
    await message.reply(f"✅ Filter saved with name: `{filter_name}`.")


# ── Filter Trigger Checker ────────────────────────
@app.on_message(~filters.bot & filters.group, group=4)
async def filter_checker(_, message: Message):
    if not message.text:
        return

    chat_id = message.chat.id
    ALL_FILTERS = await get_filters_list(chat_id)
    if not ALL_FILTERS:
        return

    for filter_ in ALL_FILTERS:
        pattern = r"( |^|[^\w])" + re.escape(filter_) + r"( |$|[^\w])"
        if re.search(pattern, message.text, flags=re.IGNORECASE):
            filter_name, content, text, data_type = await get_filter(chat_id, filter_)
            return await SendFilterMessage(
                message=message,
                filter_name=filter_,
                content=content,
                text=text,
                data_type=data_type
            )


# ── Show All Filters ───────────────────────────────
@app.on_message(filters.command("filters") & filters.group)
async def list_filters(_, message: Message):
    chat_id = message.chat.id
    chat_title = message.chat.title or "this chat"

    filters_ = await get_filters_list(chat_id)
    if not filters_:
        return await message.reply(f"❌ No filters saved in **{chat_title}**.")

    text = f"📋 **List of filters in {chat_title}:**\n\n"
    text += "\n".join([f"• `{x}`" for x in filters_])
    await message.reply(text)


# ── Remove One Filter ──────────────────────────────
@app.on_message(filters.command("stopfilter") & admin_filter)
@user_admin
async def remove_filter(_, message: Message):
    chat_id = message.chat.id

    if len(message.command) < 2:
        return await message.reply("⚠️ Usage: `/stopfilter <filter name>`")

    filter_name = message.command[1].lower()
    all_filters = await get_filters_list(chat_id)

    if filter_name not in all_filters:
        return await message.reply("⚠️ No such filter exists.")

    await stop_db(chat_id, filter_name)
    await message.reply(f"✅ Filter `{filter_name}` has been deleted.")


# ── Confirm Delete All Filters ─────────────────────
@app.on_message(filters.command("stopall") & admin_filter)
async def stop_all_confirm(_, message: Message):
    chat_id = message.chat.id
    chat_title = message.chat.title or "this chat"

    member = await app.get_chat_member(chat_id, message.from_user.id)
    if member.status != ChatMemberStatus.OWNER:
        return await message.reply("❌ Only the chat owner can delete all filters.")

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚠ Delete All Filters", callback_data="custfilters_stopall")],
        [InlineKeyboardButton("✖ Cancel", callback_data="custfilters_cancel")]
    ])

    await message.reply(
        f"⚠ Are you sure you want to **delete all filters** in **{chat_title}**?\n\nThis action is irreversible.",
        reply_markup=keyboard
    )


# ── Handle Callback for StopAll ─────────────────────
@app.on_callback_query(filters.regex("^custfilters_"))
async def stopall_callback(_, query: CallbackQuery):
    chat_id = query.message.chat.id
    data = query.data.split("_")[1]

    member = await app.get_chat_member(chat_id, query.from_user.id)
    if member.status != ChatMemberStatus.OWNER:
        return await query.answer("❌ Only the chat owner can perform this action.", show_alert=True)

    if data == "stopall":
        await stop_all_db(chat_id)
        await query.edit_message_text("✅ All filters have been removed from this chat.")
    else:
        await query.edit_message_text("❎ Cancelled filter deletion.")
