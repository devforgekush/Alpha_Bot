import requests
from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from Audify import app

# ─── API Configuration ─── #
API_KEY = "M2HSYGYWRb3Zqn8xv3Rgdlez6pWUYNQo"
API_URL = "https://api.apilayer.com/number_verification/validate"

# ─── /phone Command Handler ─── #
@app.on_message(filters.command("phone"))
def phone_lookup(_, message: Message):
    if len(message.command) < 2:
        return message.reply_text("❗ **Usage:** `/phone <number>`")

    number = message.text.split(None, 1)[1]

    try:
        response = requests.get(
            API_URL,
            params={"number": number},
            headers={"apikey": API_KEY},
            timeout=10,
        )

        if response.status_code != 200:
            return message.reply_text(f"❌ API Error: `{response.status_code}`")

        data = response.json()

        if not data.get("valid"):
            return message.reply_text("❌ **Invalid phone number.**")

        msg = (
            f"📞 **Phone Lookup Result**\n\n"
            f"✅ **Valid:** Yes\n"
            f"🔢 **Number:** `{data.get('number', '-')}`\n"
            f"🌐 **International:** `{data.get('international_format', '-')}`\n"
            f"📶 **Local:** `{data.get('local_format', '-')}`\n"
            f"🏳️ **Country:** `{data.get('country_name', '-')}` (`{data.get('country_code', '-')}`)\n"
            f"📍 **Location:** `{data.get('location', '-')}`\n"
            f"📡 **Carrier:** `{data.get('carrier', '-')}`\n"
            f"📱 **Line Type:** `{data.get('line_type', '-')}`"
        )

        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton("✖️ Close", callback_data="close")]]
        )

        return message.reply_text(msg, reply_markup=buttons)

    except requests.exceptions.RequestException as e:
        return message.reply_text(f"⚠️ **Request failed:** `{e}`")
    except Exception as e:
        return message.reply_text(f"❌ **Error:** `{e}`")
