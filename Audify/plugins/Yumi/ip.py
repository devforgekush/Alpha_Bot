from pyrogram import Client, filters
import requests
from Audify import app

@app.on_message(filters.command(["ip"]))
async def ip_info(_, message):
    if len(message.command) != 2:
        return await message.reply_text(
            "📍 **Usage:** `/ip <IP-Address>`\n\n"
            "Example: `/ip 8.8.8.8`"
        )

    ip_address = message.command[1]
    info = get_ip_info(ip_address)

    if info:
        await message.reply_text(info)
    else:
        await message.reply_text("❌ **Unable to fetch information for the provided IP address.**")


def get_ip_info(ip_address):
    try:
        api_url = f"http://ip-api.com/json/{ip_address}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success":
                info = (
                    f"🌐 **IP Address:** `{data['query']}`\n"
                    f"🏳️ **Country:** `{data['country']}`\n"
                    f"🏙️ **City:** `{data['city']}`\n"
                    f"📡 **ISP:** `{data['isp']}`\n"
                    f"🌍 **Region:** `{data['regionName']}`\n"
                    f"🧭 **Coordinates:** `{data['lat']}, {data['lon']}`"
                )
                return info
    except Exception as e:
        from Audify.logger import LOGGER
        LOGGER(__name__).error(f"Error fetching IP information: {e}")
        return None
