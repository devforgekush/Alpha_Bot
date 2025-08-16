from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.errors import RPCError
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ChatMemberUpdated,
    CallbackQuery,
)

from Audify import app

# ───────────────────────────────────────────────────────── #

@app.on_chat_member_updated(filters.group, group=20)
async def member_has_left(_, member: ChatMemberUpdated):
    if (
        member.new_chat_member or
        member.old_chat_member.status in {"banned", "left", "restricted"}
    ):
        return

    user = member.old_chat_member.user if member.old_chat_member else member.from_user

    try:
        caption = (
            f"<b>🚪 Member Departure Notice</b>\n\n"
            f"• <b>User:</b> {user.mention}\n"
            f"• <b>Status:</b> Left the chat\n"
            f"• <i>Wishing them well!</i>"
        )

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔍 View Profile", url=f"tg://openmessage?user_id={user.id}")],
            [InlineKeyboardButton("✖ Close", callback_data="close")]
        ])

        await app.send_message(
            chat_id=member.chat.id,
            text=caption,
            reply_markup=buttons,
            parse_mode=ParseMode.HTML
        )

    except RPCError as err:
    from Audify.logger import LOGGER
    LOGGER(__name__).error(f"[ERROR] RPC: {err}")
    except Exception as e:
    LOGGER(__name__).error(f"[ERROR] Unexpected: {e}")

# ───────────────────────────────────────────────────────── #
