# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import requests
from pyrogram import Client, filters
from Audify import app

RANDOM_USER_API = "https://randomuser.me/api/"

@app.on_message(filters.command("fake", prefixes="/"))
async def generate_fake_user_by_country(client, message):
    # Check if user provided a country code
    if len(message.command) < 2:
        return await message.reply_text("⚠️ Please provide a country code.\n\n💡 Example: `/fake us`")

    country_code = message.command[1].lower()
    
    try:
        response = requests.get(f'{RANDOM_USER_API}?nat={country_code}')
        if response.status_code == 200:
            user_info = response.json()['results'][0]

            first_name = user_info['name']['first']
            last_name = user_info['name']['last']
            email = user_info['email']
            country = user_info['location']['country']
            state = user_info['location']['state']
            city = user_info['location']['city']
            street = user_info['location']['street']['name']
            zip_code = user_info['location']['postcode']

            await message.reply_text(
                f"👤 **Name:** `{first_name} {last_name}`\n"
                f"📧 **Email:** `{email}`\n"
                f"🌍 **Country:** `{country}`\n"
                f"🏙️ **State:** `{state}`\n"
                f"🏘️ **City:** `{city}`\n"
                f"📍 **Street:** `{street}`\n"
                f"🔢 **Zip Code:** `{zip_code}`"
            )
        else:
            await message.reply_text("❌ Failed to fetch fake user data. Try a valid 2-letter country code (like `us`, `gb`, `in`).")

    except Exception as e:
        await message.reply_text(f"❌ Error: `{str(e)}`")
