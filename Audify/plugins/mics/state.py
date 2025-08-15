# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import Client, filters
import pycountry
from Audify import app

@app.on_message(filters.command("getstates"))
def get_states(client, message):
    try:
        # Extract the country name from command
        country_name = message.text.split(' ', 1)[1].strip()

        # Try exact match
        country = pycountry.countries.get(name=country_name)

        # Fallback to partial match
        if not country:
            country = next((c for c in pycountry.countries if country_name.lower() in c.name.lower()), None)

        if not country:
            raise ValueError(f"❌ Country '{country_name}' not found.")

        # Get subdivisions/states
        subdivisions = pycountry.subdivisions.get(country_code=country.alpha_2)
        if not subdivisions:
            raise ValueError(f"ℹ️ No states or subdivisions found for '{country.name}'.")

        states_list = [sub.name for sub in subdivisions]
        formatted_states = "\n".join(f"• {state}" for state in states_list)

        reply = f"🌍 **States/Provinces of {country.name}:**\n\n{formatted_states}"
    except IndexError:
        reply = "❗ Please provide a country name.\n\n**Example:** `/getstates India`"
    except ValueError as ve:
        reply = str(ve)
    except Exception:
        reply = "⚠️ Something went wrong while fetching states. Please try again."

    message.reply_text(reply)
