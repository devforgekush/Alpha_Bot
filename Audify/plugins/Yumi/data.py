# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import Client, filters
from faker import Faker
from Audify import app
from pyrogram.types import Message

# Create a Faker instance
fake = Faker()

# Generate person info command handler
@app.on_message(filters.command("data"))
async def generate_info(client: Client, message: Message):
    # Generate fake data
    name = fake.name()
    address = fake.address()
    country = fake.country()
    phone_number = fake.phone_number()
    email = fake.email()
    city = fake.city()
    state = fake.state()
    zipcode = fake.zipcode()

    # Create a message with the fake data
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

    # Send the fake data to the user
    await message.reply_text(info_message)
