# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Audify import app
from config import OWNER_ID
from Audify.utils.Audify_BAN import admin_filter


def view_and_close(url: str):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🗒 View Message", url=url)],
        [InlineKeyboardButton("✖️ Close", callback_data="close")]
    ])


CLOSE_BTN = InlineKeyboardMarkup([[InlineKeyboardButton("✖️ Close", callback_data="close")]])

# ──────────────────────────────────────────────────────── #

@app.on_message(filters.command("pin") & admin_filter)
async def pin_message(_, message: Message):
    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply_text("❌ This command works only in groups.", reply_markup=CLOSE_BTN)

    if not message.reply_to_message:
        return await message.reply_text("🔖 Reply to a message to pin it.", reply_markup=CLOSE_BTN)

    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    if user.privileges and user.privileges.can_pin_messages:
        try:
            await message.reply_to_message.pin()
            await message.reply_text(
                f"📌 Message pinned successfully!\n\n➤ By: {message.from_user.mention}",
                reply_markup=view_and_close(message.reply_to_message.link)
            )
        except Exception as e:
            await message.reply_text(f"❗️ Failed to pin:\n`{e}`", reply_markup=CLOSE_BTN)
    else:
        await message.reply_text("🚫 You need 'Pin Messages' permission.", reply_markup=CLOSE_BTN)

# ──────────────────────────────────────────────────────── #

@app.on_message(filters.command("unpin") & admin_filter)
async def unpin_message(_, message: Message):
    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply_text("❌ This command works only in groups.", reply_markup=CLOSE_BTN)

    if not message.reply_to_message:
        return await message.reply_text("🔓 Reply to a pinned message to unpin it.", reply_markup=CLOSE_BTN)

    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    if user.privileges and user.privileges.can_pin_messages:
        try:
            await message.reply_to_message.unpin()
            await message.reply_text(
                f"🧹 Message unpinned successfully.\n\n➤ By: {message.from_user.mention}",
                reply_markup=view_and_close(message.reply_to_message.link)
            )
        except Exception as e:
            await message.reply_text(f"❗️ Failed to unpin:\n`{e}`", reply_markup=CLOSE_BTN)
    else:
        await message.reply_text("🚫 You don't have permission to unpin messages.", reply_markup=CLOSE_BTN)

# ──────────────────────────────────────────────────────── #

@app.on_message(filters.command("pinned"))
async def show_pinned(_, message: Message):
    chat = await app.get_chat(message.chat.id)
    if not chat.pinned_message:
        return await message.reply_text("📭 No pinned message found.", reply_markup=CLOSE_BTN)

    try:
        await message.reply_text(
            "📍 Here's the latest pinned message:",
            reply_markup=view_and_close(chat.pinned_message.link)
        )
    except Exception as e:
        await message.reply_text(f"⚠️ Couldn’t fetch pinned message:\n`{e}`", reply_markup=CLOSE_BTN)

# ──────────────────────────────────────────────────────── #

@app.on_message(filters.command("removephoto") & admin_filter)
async def remove_photo(_, message: Message):
    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply_text("🚫 This command works only in groups.", reply_markup=CLOSE_BTN)

    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    if user.privileges and user.privileges.can_change_info:
        try:
            await app.delete_chat_photo(message.chat.id)
            await message.reply_text(f"🖼 Group photo removed successfully.\n\n➤ By: {message.from_user.mention}")
        except Exception as e:
            await message.reply_text(f"⚠️ Failed to remove photo:\n`{e}`", reply_markup=CLOSE_BTN)
    else:
        await message.reply_text("❌ You need 'Change Info' rights to remove photo.", reply_markup=CLOSE_BTN)

# ──────────────────────────────────────────────────────── #

@app.on_message(filters.command("setphoto") & admin_filter)
async def set_photo(_, message: Message):
    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply_text("❌ This command works only in groups.", reply_markup=CLOSE_BTN)

    reply = message.reply_to_message
    if not reply or not (reply.photo or reply.document):
        return await message.reply_text("🖼 Reply to a photo or image document to set it as group photo.", reply_markup=CLOSE_BTN)

    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    if user.privileges and user.privileges.can_change_info:
        try:
            file = await reply.download()
            await app.set_chat_photo(message.chat.id, photo=file)
            await message.reply_text(f"✅ Group photo updated!\n\n➤ By: {message.from_user.mention}")
        except Exception as e:
            await message.reply_text(f"⚠️ Failed to set photo:\n`{e}`", reply_markup=CLOSE_BTN)
    else:
        await message.reply_text("🚫 You need 'Change Info' rights to change group photo.", reply_markup=CLOSE_BTN)

# ──────────────────────────────────────────────────────── #

@app.on_message(filters.command("settitle") & admin_filter)
async def set_title(_, message: Message):
    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply_text("❌ This command works only in groups.", reply_markup=CLOSE_BTN)

    title = None
    if message.reply_to_message:
        title = message.reply_to_message.text
    elif len(message.command) > 1:
        title = message.text.split(None, 1)[1]

    if not title:
        return await message.reply_text("📝 Please provide a group title.", reply_markup=CLOSE_BTN)

    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    if user.privileges and user.privileges.can_change_info:
        try:
            await app.set_chat_title(message.chat.id, title)
            await message.reply_text(f"🎉 Group title updated to:\n`{title}`\n\n➤ By: {message.from_user.mention}")
        except Exception as e:
            await message.reply_text(f"⚠️ Failed to update title:\n`{e}`", reply_markup=CLOSE_BTN)
    else:
        await message.reply_text("🚫 You need 'Change Info' rights to update title.", reply_markup=CLOSE_BTN)

# ──────────────────────────────────────────────────────── #

@app.on_message(filters.command("setdescription") & admin_filter)
async def set_description(_, message: Message):
    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply_text("❌ This command works only in groups.", reply_markup=CLOSE_BTN)

    description = None
    if message.reply_to_message:
        description = message.reply_to_message.text
    elif len(message.command) > 1:
        description = message.text.split(None, 1)[1]

    if not description:
        return await message.reply_text("💬 Please provide a group description.", reply_markup=CLOSE_BTN)

    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    if user.privileges and user.privileges.can_change_info:
        try:
            await app.set_chat_description(message.chat.id, description)
            await message.reply_text(f"✅ Group description updated.\n\n➤ By: {message.from_user.mention}")
        except Exception as e:
            await message.reply_text(f"⚠️ Failed to set description:\n`{e}`", reply_markup=CLOSE_BTN)
    else:
        await message.reply_text("🚫 You need 'Change Info' rights to update description.", reply_markup=CLOSE_BTN)

# ──────────────────────────────────────────────────────── #

@app.on_message(filters.command("lg") & filters.user(OWNER_ID))
async def leave_group(_, message: Message):
    await message.reply_text("👋 Leaving this group...", reply_markup=CLOSE_BTN)
    await app.leave_chat(message.chat.id)

# ──────────────────────────────────────────────────────── #

