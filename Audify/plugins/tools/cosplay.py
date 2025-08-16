import requests
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from Audify import app
from config import SUPPORT_CHAT

# ── Buttons ───────────────────────────────────────────────
COSPLAY_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("💬 Support", url=SUPPORT_CHAT)],
    [InlineKeyboardButton("✖ Close", callback_data="close")]
])

# ── Cosplay Command ───────────────────────────────────────
@app.on_message(filters.command("cosplay"))
async def cosplay(_, msg: Message):
    try:
        image_url = requests.get("https://waifu-api.vercel.app").json()

        if not isinstance(image_url, str) or not image_url.startswith("http"):
            return await msg.reply_text("❌ Couldn't fetch image. Please try again later.")

        await msg.reply_photo(
            photo=image_url,
            caption="🎭 Here's your cosplay of the day!",
            reply_markup=COSPLAY_BUTTONS
        )
    except Exception as e:
        await msg.reply_text(f"❌ Error:\n<code>{e}</code>")
