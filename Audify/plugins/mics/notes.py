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
from Audify.utils.Audify_BAN import admin_filter
from Audify.mongo.notesdb import *
from Audify.utils.notes_func import (
    GetNoteMessage, exceNoteMessageSender,
    privateNote_and_admin_checker
)
from Audify.utils.yumidb import user_admin
from pyrogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup,
    Message, CallbackQuery
)
from pyrogram.enums import ChatMemberStatus


@app.on_message(filters.command("save") & admin_filter)
@user_admin
async def save_note_handler(client, message: Message):
    chat_id = message.chat.id
    chat_title = message.chat.title

    if message.reply_to_message and len(message.command) < 2:
        return await message.reply("🔹 Please provide a name for the note!")

    if not message.reply_to_message and len(message.command) < 3:
        return await message.reply("🔹 You must provide content to save in the note!")

    note_name = message.command[1]
    content, text, data_type = GetNoteMessage(message)
    await SaveNote(chat_id, note_name, content, text, data_type)

    await message.reply(f"✅ Note `{note_name}` has been saved in <b>{chat_title}</b>.")


@app.on_message(filters.command("get") & admin_filter)
async def get_note_handler(client, message: Message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        return await message.reply("🔹 Please specify the note name.")

    note_name = message.command[1]
    if not await isNoteExist(chat_id, note_name):
        return await message.reply("⚠️ This note doesn't exist.")

    await send_note(message, note_name)


@app.on_message(filters.regex(r"^#[^\s]+") & filters.group)
async def hashtag_note_handler(client, message: Message):
    chat_id = message.chat.id
    note_name = message.text.split()[0][1:]

    if await isNoteExist(chat_id, note_name):
        await send_note(message, note_name)


@app.on_message(filters.command("privatenotes") & filters.group)
@user_admin
async def private_note_toggle(client, message: Message):
    chat_id = message.chat.id
    if len(message.command) >= 2:
        arg = message.command[1].lower()
        if arg in ['on', 'true', 'yes', 'y']:
            await set_private_note(chat_id, True)
            return await message.reply("🔒 Notes will now be sent in private chat.")

        elif arg in ['off', 'false', 'no', 'n']:
            await set_private_note(chat_id, False)
            return await message.reply("📢 Notes will now be shown in the group.")

        else:
            return await message.reply("❌ Invalid option. Use on/off or true/false.")
    else:
        current = await is_pnote_on(chat_id)
        if current:
            await message.reply("🔒 Notes are currently being sent privately.")
        else:
            await message.reply("📢 Notes are currently shown in the group.")


@app.on_message(filters.command("clear") & admin_filter)
@user_admin
async def clear_note_handler(client, message: Message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        return await message.reply("🔹 Please specify the note name to delete.")

    note_name = message.command[1].lower()
    if await isNoteExist(chat_id, note_name):
        await ClearNote(chat_id, note_name)
        await message.reply(f"✅ Note `{note_name}` has been removed.")
    else:
        await message.reply("⚠️ No such note found.")


@app.on_message(filters.command("clearall") & admin_filter)
async def clear_all_handler(client, message: Message):
    chat_id = message.chat.id
    user = await client.get_chat_member(chat_id, message.from_user.id)
    if user.status != ChatMemberStatus.OWNER:
        return await message.reply("🚫 Only group owner can perform this action.")

    notes = await NoteList(chat_id)
    if not notes:
        return await message.reply("ℹ️ There are no notes in this group.")

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Delete all notes", callback_data=f"clearallnotes_clear_{message.from_user.id}_{chat_id}")],
        [InlineKeyboardButton("❌ Cancel", callback_data=f"clearallnotes_cancel_{message.from_user.id}")]
    ])
    await message.reply("⚠️ Are you sure you want to delete all saved notes?", reply_markup=markup)


@app.on_callback_query(filters.regex("^clearallnotes_"))
async def clear_all_callback(client, callback: CallbackQuery):
    data = callback.data.split('_')
    action = data[1]
    owner_id = int(data[2])
    user_id = callback.from_user.id

    if user_id != owner_id:
        return await callback.answer("Only the initiator can confirm this action.", show_alert=True)

    if action == "clear":
        chat_id = int(data[3])
        await ClearAllNotes(chat_id)
        await callback.edit_message_text("✅ All notes have been deleted.")
    elif action == "cancel":
        await callback.edit_message_text("❌ Operation cancelled.")


@app.on_message(filters.command(['notes', 'saved']) & filters.group)
async def list_notes(client, message: Message):
    chat_id = message.chat.id
    title = message.chat.title
    notes = await NoteList(chat_id)

    if notes:
        formatted_notes = "\n".join([f" • `#{note}`" for note in notes])
        await message.reply(
            f"<b>Notes saved in {title}:</b>\n\n{formatted_notes}\n\n"
            "You can use `/get notename` or `#notename` to retrieve them.",
            quote=True
        )
    else:
        await message.reply(f"ℹ️ No notes found in {title}.")


# ─── Utility Handlers ───
async def send_note(message: Message, note_name: str):
    chat_id = message.chat.id
    content, text, data_type = await GetNote(chat_id, note_name)
    private_note, allowed = await privateNote_and_admin_checker(message, text)

    if allowed:
        if private_note is None:
            if await is_pnote_on(chat_id):
                await send_private_button(message, chat_id, note_name)
            else:
                await exceNoteMessageSender(message, note_name)
        elif private_note:
            await send_private_button(message, chat_id, note_name)
        else:
            await exceNoteMessageSender(message, note_name)


async def send_private_button(message: Message, chat_id, note_name):
    button = InlineKeyboardMarkup([[
        InlineKeyboardButton("🔎 View Note", url=f"https://t.me/{BOT_USERNAME}?start=note_{chat_id}_{note_name}")
    ]])
    await message.reply(f"Tap below to view `{note_name}` in private.", reply_markup=button)


async def note_redirect(message: Message):
    chat_id = int(message.command[1].split('_')[1])
    note_name = message.command[1].split('_')[2]
    await exceNoteMessageSender(message, note_name, from_chat_id=chat_id)
