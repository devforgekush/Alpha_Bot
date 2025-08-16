import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
try:
    from telethon.sync import TelegramClient as TeleClient
    from telethon.sessions import StringSession as TeleString
except Exception:
    TeleClient = None
    TeleString = None
from Audify import app

API_ID = 29557063  # Replace with your default API ID
API_HASH = "98975771aa1190b5fbc993f976960260"  # Replace with your default API HASH

session_users = {}

# ---------------------- /sgen ---------------------- #

@app.on_message(filters.command("sgen"))
async def session_gen_menu(_, message: Message):
    buttons = [
        [
            InlineKeyboardButton("👤 Pyro User", callback_data="sgen_pyro_user"),
            InlineKeyboardButton("🤖 Pyro Bot", callback_data="sgen_pyro_bot")
        ],
        [
            InlineKeyboardButton("👤 Tele User", callback_data="sgen_tele_user"),
            InlineKeyboardButton("🤖 Tele Bot ❌", callback_data="sgen_tele_bot")
        ]
    ]
    await message.reply_text(
        "**🧬 Session Generator**\nChoose your session type:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ---------------------- Callbacks ---------------------- #

@app.on_callback_query(filters.regex("sgen_"))
async def on_sgen_cb(_, query):
    user_id = query.from_user.id
    cb = query.data

    await query.message.delete()

    if cb == "sgen_pyro_user":
        await query.message.reply("Send your **API ID** (number only):")
        session_users[user_id] = {"stage": "get_api_id", "type": "pyro_user"}
    elif cb == "sgen_pyro_bot":
        await query.message.reply("Send your **API ID** (number only):")
        session_users[user_id] = {"stage": "get_api_id", "type": "pyro_bot"}
    elif cb == "sgen_tele_user":
        await query.message.reply("Send your **API ID** (number only):")
        session_users[user_id] = {"stage": "get_api_id", "type": "tele_user"}
    elif cb == "sgen_tele_bot":
        await query.message.reply("❌ Telethon does not support Bot session generation.")

# ---------------------- Message Flow ---------------------- #

@app.on_message(filters.text & filters.private)
async def handle_input(_, message: Message):
    user_id = message.from_user.id
    text = message.text.strip()

    if user_id not in session_users:
        return

    data = session_users[user_id]
    stage = data["stage"]
    session_type = data["type"]

    # Cancel
    if text.lower() == "/cancel":
        session_users.pop(user_id)
        return await message.reply("❌ Cancelled.")

    # Handle API_ID
    if stage == "get_api_id":
        if not text.isdigit():
            return await message.reply("❗ Please enter a valid API ID (number only).")
        data["api_id"] = int(text)
        data["stage"] = "get_api_hash"
        return await message.reply("Now send your **API HASH**:")

    # Handle API_HASH
    if stage == "get_api_hash":
        if len(text) < 10:
            return await message.reply("❗ Invalid API_HASH.")
        data["api_hash"] = text

        if session_type == "pyro_bot":
            data["stage"] = "get_bot_token"
            return await message.reply("Send your **Bot Token**:")
        else:
            data["stage"] = "get_phone"
            return await message.reply("Send your **Phone Number** (with +):")

    # Handle Bot Token
    if stage == "get_bot_token":
        try:
            client = Client(
                name=str(user_id),
                api_id=data["api_id"],
                api_hash=data["api_hash"],
                bot_token=text,
                in_memory=True
            )
            await client.start()
            session = await client.export_session_string()
            await client.disconnect()
            session_users.pop(user_id)
            return await message.reply(f"✅ **Pyrogram Bot Session**:\n\n`{session}`")
        except Exception as e:
            session_users.pop(user_id)
            return await message.reply(f"❌ Failed:\n`{e}`")

    # Handle Phone
    if stage == "get_phone":
        data["phone"] = text
        await message.reply("📨 Sending OTP...")
        try:
            if "pyro" in session_type:
                client = Client(str(user_id), api_id=data["api_id"], api_hash=data["api_hash"], in_memory=True)
                await client.connect()
                sent = await client.send_code(text)
                data["client"] = client
                data["phone_code_hash"] = sent.phone_code_hash
                data["stage"] = "get_otp"
                await message.reply("✅ Now send the **OTP** as space-separated digits (e.g. `1 2 3 4 5`):")
            else:
                client = TeleClient(StringSession(), api_id=data["api_id"], api_hash=data["api_hash"])
                client.connect()
                sent = client.send_code_request(text)
                data["tele_client"] = client
                data["stage"] = "get_otp"
                await message.reply("✅ Now send the **OTP** as space-separated digits (e.g. `1 2 3 4 5`):")
        except Exception as e:
            session_users.pop(user_id)
            return await message.reply(f"❌ Error sending OTP:\n`{e}`")

    # Handle OTP
    if stage == "get_otp":
        otp_code = text.replace(" ", "")
        if not otp_code.isdigit():
            return await message.reply("❌ Invalid OTP format. Use: `1 2 3 4 5`")

        try:
            if "pyro" in session_type:
                await data["client"].sign_in(
                    phone_number=data["phone"],
                    phone_code_hash=data["phone_code_hash"],
                    phone_code=otp_code
                )
                session = await data["client"].export_session_string()
                await data["client"].disconnect()
                session_users.pop(user_id)
                return await message.reply(f"✅ **Pyrogram User Session**:\n\n`{session}`")

            else:
                client = data["tele_client"]
                client.sign_in(data["phone"], otp_code)
                session = client.session.save()
                client.disconnect()
                session_users.pop(user_id)
                return await message.reply(f"✅ **Telethon User Session**:\n\n`{session}`")

        except Exception as e:
            if "SESSION_PASSWORD_NEEDED" in str(e):
                data["stage"] = "get_password"
                return await message.reply("🔐 2FA is enabled. Please send your **Telegram password**.")
            session_users.pop(user_id)
            return await message.reply(f"❌ OTP Failed:\n`{e}`")

    # Handle 2FA Password
    if stage == "get_password":
        try:
            await data["client"].check_password(text)
            session = await data["client"].export_session_string()
            await data["client"].disconnect()
            session_users.pop(user_id)
            return await message.reply(f"✅ **Pyrogram User Session**:\n\n`{session}`")
        except Exception as e:
            session_users.pop(user_id)
            return await message.reply(f"❌ 2FA Failed:\n`{e}`")
