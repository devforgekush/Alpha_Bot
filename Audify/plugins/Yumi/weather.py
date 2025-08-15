# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import requests
from urllib.parse import quote_plus
from Audify import app

# Your OpenWeatherMap API key
OPENWEATHER_API_KEY = "b5d6369c0cdb98a0bc6b7d582377d853"

@app.on_message(filters.command("weather"))
async def fetch_weather(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "🌤️ Please provide a location.\n\nExample: `/weather delhi`"
        )

    city_input = message.text.split(maxsplit=1)[1].strip()
    city_encoded = quote_plus(city_input.lower())

    api_url = (
        f"http://api.openweathermap.org/data/2.5/weather?"
        f"q={city_encoded}&appid={OPENWEATHER_API_KEY}&units=metric"
    )

    try:
        response = requests.get(api_url)
        data = response.json()
    except Exception as e:
        return await message.reply_text(f"❌ Failed to fetch weather.\n`{e}`")

    if data.get("cod") != 200:
        return await message.reply_text(f"❌ Couldn't find weather for `{city_input}`.")

    city = data["name"]
    country = data["sys"]["country"]
    temperature = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    weather_desc = data["weather"][0]["description"].title()
    icon_code = data["weather"][0]["icon"]
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@4x.png"

    caption = (
        f"🌍 <b>Weather in {city}, {country}</b>\n\n"
        f"🌤️ <b>Condition:</b> <code>{weather_desc}</code>\n"
        f"🌡️ <b>Temperature:</b> <code>{temperature}°C</code>\n"
        f"🧣 <b>Feels Like:</b> <code>{feels_like}°C</code>\n"
        f"💧 <b>Humidity:</b> <code>{humidity}%</code>\n"
        f"💨 <b>Wind:</b> <code>{wind_speed} m/s</code>"
    )

    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("❌ Close", callback_data="close")]]
    )

    await message.reply_photo(
        photo=icon_url,
        caption=caption,
        reply_markup=buttons,
        parse_mode=ParseMode.HTML
    )
