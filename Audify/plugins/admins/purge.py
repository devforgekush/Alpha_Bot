from asyncio import sleep
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.errors import MessageDeleteForbidden, RPCError
from pyrogram.types import Message
from Audify.utils.Audify_BAN import admin_filter
from Audify.utils.inline import close_markup
from Audify import app


@app.on_message(filters.command("purge") & filters.group & admin_filter)
async def purge_messages(app, message: Message):
    if message.chat.type != ChatType.SUPERGROUP:
        return await message.reply_text(
            "⚠️ I can't purge messages in a basic group. Please upgrade to a supergroup."
        )

    if not message.reply_to_message:
        return await message.reply_text("✏️ Reply to a message to start purging from there.")

    message_ids = list(range(message.reply_to_message.id, message.id))

    def divide_chunks(data, size=100):
        for i in range(0, len(data), size):
            yield data[i : i + size]

    grouped_ids = list(divide_chunks(message_ids))

    try:
        for batch in grouped_ids:
            await app.delete_messages(chat_id=message.chat.id, message_ids=batch, revoke=True)
        await message.delete()
    except MessageDeleteForbidden:
        return await message.reply_text(
            "🚫 Unable to delete all messages. I may lack delete rights or the messages may be too old."
        )
    except RPCError as err:
        return await message.reply_text(
            f"⚠️ An unexpected error occurred. Please report with `/bug`\n\nError: `{err}`"
        )

    count = len(message_ids)
    confirmation = await message.reply_text(f"✅ Successfully deleted {count} messages.")
    await sleep(3)
    await confirmation.delete()


@app.on_message(filters.command("spurge") & filters.group & admin_filter)
async def silent_purge(app, message: Message):
    if message.chat.type != ChatType.SUPERGROUP:
        return await message.reply_text(
            "⚠️ I can't purge messages in a basic group. Please upgrade to a supergroup."
        )

    if not message.reply_to_message:
        return await message.reply_text("✏️ Reply to a message to start silent purging.")

    message_ids = list(range(message.reply_to_message.id, message.id))

    def divide_chunks(data, size=100):
        for i in range(0, len(data), size):
            yield data[i : i + size]

    grouped_ids = list(divide_chunks(message_ids))

    try:
        for batch in grouped_ids:
            await app.delete_messages(chat_id=message.chat.id, message_ids=batch, revoke=True)
        await message.delete()
    except MessageDeleteForbidden:
        return await message.reply_text(
            "🚫 Unable to delete all messages. I may lack delete rights or the messages may be too old."
        )
    except RPCError as err:
        return await message.reply_text(
            f"⚠️ An unexpected error occurred. Please report with `/bug`\n\nError: `{err}`"
        )


@app.on_message(filters.command("del") & filters.group & admin_filter)
async def delete_single_message(app, message: Message):
    if message.chat.type != ChatType.SUPERGROUP:
        return await message.reply_text(
            "⚠️ I can't delete messages in a basic group. Please upgrade to a supergroup."
        )

    if not message.reply_to_message:
        return await message.reply_text("✏️ What message do you want me to delete?")

    await message.delete()
    await app.delete_messages(chat_id=message.chat.id, message_ids=message.reply_to_message.id)
