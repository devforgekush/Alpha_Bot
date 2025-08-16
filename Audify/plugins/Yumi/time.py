from pyrogram import Client, filters
from pyrogram.types import Message
import requests
from Audify import app

API_KEY = "XF9QM375W294"
TIMEZONE_API_URL = "https://api.timezonedb.com/v2.1/list-time-zone"
GET_TIME_URL = "https://api.timezonedb.com/v2.1/get-time-zone"

@app.on_message(filters.command("time"))
async def get_city_time(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❗ Please provide a location.\n\nExample: `/time Tokyo`", quote=True)

    location_query = message.text.split(" ", 1)[1].lower()

    try:
        # Fetch timezone list
        response = requests.get(
            TIMEZONE_API_URL,
            params={"key": API_KEY, "format": "json"}
        )
        zones = response.json().get("zones", [])

        # Find matching zone
        matched_zone = next((zone["zoneName"] for zone in zones if location_query in zone["zoneName"].lower()), None)

        if not matched_zone:
            return await message.reply_text("❌ Location not found. Try a valid city or country name.", quote=True)

        # Get time for matched zone
        time_response = requests.get(
            GET_TIME_URL,
            params={"key": API_KEY, "format": "json", "by": "zone", "zone": matched_zone}
        ).json()

        if time_response["status"] != "OK":
            return await message.reply_text("⚠️ Failed to fetch time. Try again later.", quote=True)

        location_name = time_response["zoneName"]
        current_time = time_response["formatted"]
        abbreviation = time_response.get("abbreviation", "")
        gmt_offset = time_response.get("gmtOffset", 0) // 3600

        await message.reply_text(
            f"🕰️ **Current Time in `{location_name}`**\n"
            f"📅 `{current_time}`\n"
            f"🕓 UTC Offset: `GMT{'+' if gmt_offset >= 0 else ''}{gmt_offset}`\n"
            f"🧭 Abbreviation: `{abbreviation}`",
            quote=True
        )

    except Exception as e:
    from Audify.logger import LOGGER
    LOGGER(__name__).error(f"Error fetching time: {e}")
    await message.reply_text("⚠️ Something went wrong. Please try again later.", quote=True)
