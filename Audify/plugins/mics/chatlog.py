import logging
import html
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from Audify import app
from config import LOGGER_ID as JOINLOGS

# Setup logging
logger = logging.getLogger(__name__)
if not logging.getLogger().hasHandlers():
    logging.basicConfig(level=logging.INFO)

BOT_ID = None

# Log when bot is added to a group
@app.on_message(filters.new_chat_members)
async def on_new_chat_members(client: Client, message: Message):
    global BOT_ID

    try:
        if BOT_ID is None:
            bot_user = await client.get_me()
            BOT_ID = bot_user.id
    except Exception as e:
        logger.exception("Failed to get bot info")
        return

    for new_member in message.new_chat_members:
        if new_member.id == BOT_ID:
            chat = message.chat
            chat_type = chat.type.name.capitalize()

            if chat_type == "Channel":
                try:
                    await client.leave_chat(chat.id)
                    logger.warning(f"Left channel: {chat.title} ({chat.id})")
                    return
                except Exception as e:
                    logger.exception(f"Failed to leave channel: {chat.title}")
                    return

            try:
                added_by = (
                    f"<a href='tg://user?id={message.from_user.id}'>👤 {html.escape(message.from_user.first_name)}</a>"
                    if message.from_user else "🕵️‍♂️ Unknown User"
                )

                chat_title = html.escape(chat.title)
                chat_id = chat.id

                # Handle group link (public/private)
                if chat.username:
                    chat_username = f"@{chat.username}"
                    chat_link = f"https://t.me/{chat.username}"
                else:
                    try:
                        chat_link = await client.export_chat_invite_link(chat.id)
                        chat_username = "🔗 Private Invite Link"
                    except:
                        chat_link = None
                        chat_username = "🔒 Private Group (No Access)"

                try:
                    members_count = await client.get_chat_members_count(chat_id)
                except:
                    members_count = "N/A"

                log_text = (
                    "<b>🚀 Bot Added Successfully!</b>\n\n"
                    "╭───────⍟\n"
                    f"├ 💬 <b>Chat Name:</b> <code>{chat_title}</code>\n"
                    f"├ 🆔 <b>Chat ID:</b> <code>{chat_id}</code>\n"
                    f"├ 🧩 <b>Chat Type:</b> {chat_type}\n"
                    f"├ 👥 <b>Members:</b> <code>{members_count}</code>\n"
                    f"├ 🌐 <b>Username:</b> {chat_username}\n"
                    f"└ 👤 <b>Added By:</b> {added_by}\n"
                    "╰─────────────⍟"
                )

                buttons = [[InlineKeyboardButton("🌟 Visit Chat", url=chat_link)]] if chat_link else None

                await client.send_message(
                    JOINLOGS,
                    text=log_text,
                    reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
                    disable_web_page_preview=True
                )
                logger.info(f"Join log sent for chat ID: {chat_id}")
            except Exception as e:
                logger.exception(f"[JOINLOG ERROR] Failed to send join log for chat ID: {chat.id}")

# Log when bot is removed from a group
@app.on_message(filters.left_chat_member)
async def on_left_chat_member(client: Client, message: Message):
    global BOT_ID

    try:
        if BOT_ID is None:
            bot_user = await client.get_me()
            BOT_ID = bot_user.id
    except Exception as e:
        logger.exception("Failed to get bot info")
        return

    if message.left_chat_member.id == BOT_ID:
        try:
            chat = message.chat
            chat_type = chat.type.name.capitalize()
            removed_by = (
                f"<a href='tg://user?id={message.from_user.id}'>👤 {html.escape(message.from_user.first_name)}</a>"
                if message.from_user else "🕵️‍♂️ Unknown User"
            )

            chat_title = html.escape(chat.title)
            chat_id = chat.id

            # Handle group link (public/private)
            if chat.username:
                chat_username = f"@{chat.username}"
                chat_link = f"https://t.me/{chat.username}"
            else:
                try:
                    chat_link = await client.export_chat_invite_link(chat.id)
                    chat_username = "🔗 Private Invite Link"
                except:
                    chat_link = None
                    chat_username = "🔒 Private Group (No Access)"

            try:
                members_count = await client.get_chat_members_count(chat_id)
            except:
                members_count = "N/A"

            log_text = (
                "<b>❌ Bot Removed from Chat</b>\n\n"
                "╭───────⍟\n"
                f"├ 💬 <b>Chat Name:</b> <code>{chat_title}</code>\n"
                f"├ 🆔 <b>Chat ID:</b> <code>{chat_id}</code>\n"
                f"├ 🧩 <b>Chat Type:</b> {chat_type}\n"
                f"├ 👥 <b>Members:</b> <code>{members_count}</code>\n"
                f"├ 🌐 <b>Username:</b> {chat_username}\n"
                f"└ 👤 <b>Removed By:</b> {removed_by}\n"
                "╰─────────────⍟"
            )

            buttons = [[InlineKeyboardButton("🌐 Visit Chat", url=chat_link)]] if chat_link else None

            await client.send_message(
                JOINLOGS,
                text=log_text,
                reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
                disable_web_page_preview=True
            )
            logger.info(f"Left log sent for chat ID: {chat_id}")
        except Exception as e:
            logger.exception(f"[LEFTLOG ERROR] Failed to send left log for chat ID: {chat.id}")
