from Audify import app
from pyrogram.types import ChatJoinRequest, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import filters

WELCOME_TEXT = (
    "👋 Hello {mention},\n"
    "✅ You've been approved to join **{title}**.\n\n"
    "We're glad to have you here!"
)

CLOSE_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("✖ Close", callback_data="close_message")]
])


@app.on_chat_join_request()
async def auto_approve_request(client, request: ChatJoinRequest):
    user = request.from_user
    chat = request.chat

    await client.approve_chat_join_request(chat.id, user.id)

    await client.send_message(
        chat_id=chat.id,
        text=WELCOME_TEXT.format(mention=user.mention, title=chat.title),
        reply_markup=CLOSE_BUTTON
    )
