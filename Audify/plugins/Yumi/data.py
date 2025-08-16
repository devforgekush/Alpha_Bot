from pyrogram import Client, filters
from Audify import app
from pyrogram.types import Message

# faker is optional — guard import and disable command if unavailable
try:
    from faker import Faker
    fake = Faker()
except Exception:
    fake = None


@app.on_message(filters.command("data"))
async def generate_info(client: Client, message: Message):
    if not fake:
        return await message.reply_text("⚠️ Feature unavailable: missing dependency 'faker'.")
    name = fake.name()
    address = fake.address()
    country = fake.country()
    phone_number = fake.phone_number()
    email = fake.email()
    city = fake.city()
    state = fake.state()
    zipcode = fake.zipcode()

    info_message = (
        f"📇 **Full Name:** `{name}`\n"
        f"🏠 **Address:** `{address}`\n"
        f"🌍 **Country:** `{country}`\n"
        f"📞 **Phone Number:** `{phone_number}`\n"
        f"📧 **Email:** `{email}`\n"
        f"🏙️ **City:** `{city}`\n"
        f"🗺️ **State:** `{state}`\n"
        f"🔢 **Zip Code:** `{zipcode}`"
    )

    await message.reply_text(info_message)
