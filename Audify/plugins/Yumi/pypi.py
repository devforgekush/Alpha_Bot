# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
from Audify import app

def get_pypi_info(package_name):
    try:
        api_url = f"https://pypi.org/pypi/{package_name}/json"
        response = requests.get(api_url)
        return response.json()
    except Exception as e:
    from Audify.logger import LOGGER
    LOGGER(__name__).error(f"Error fetching PyPI information: {e}")
        return None

@app.on_message(filters.command("pypi", prefixes="/"))
async def pypi_info_command(client, message):
    try:
        package_name = message.command[1]
        pypi_info = get_pypi_info(package_name)

        if pypi_info:
            name = pypi_info['info'].get('name', 'N/A')
            version = pypi_info['info'].get('version', 'N/A')
            summary = pypi_info['info'].get('summary', 'No description available.')
            homepage = pypi_info['info'].get('project_urls', {}).get('Homepage', f'https://pypi.org/project/{package_name}')

            info_message = (
                f"📦 <b>Package:</b> <code>{name}</code>\n"
                f"📌 <b>Latest Version:</b> <code>{version}</code>\n"
                f"📝 <b>Description:</b> {summary}\n"
                f"🌐 <b>Project URL:</b> <a href='{homepage}'>Visit Homepage</a>"
            )

            await client.send_message(
                message.chat.id,
                info_message,
                parse_mode=enums.ParseMode.HTML,
                disable_web_page_preview=True,
            )
        else:
            await client.send_message(message.chat.id, "❌ Failed to fetch information from PyPI.")
    except IndexError:
        await client.send_message(message.chat.id, "❗ Please provide a package name after the /pypi command.")
