from pyrogram import Client, filters  
import whois  
from Audify import app  


def get_domain_hosting_info(domain_name):  
    try:  
        domain_info = whois.whois(domain_name)  
        return domain_info  
    except whois.parser.PywhoisError as e:  
    from Audify.logger import LOGGER
    LOGGER(__name__).error(f"Error: {e}")  
    return None  


@app.on_message(filters.command("domain"))  
async def get_domain_info(client, message):  
    if len(message.command) > 1:  
        domain_name = message.text.split("/domain ", 1)[1]  
        domain_info = get_domain_hosting_info(domain_name)  

        if domain_info:  
            response = (
                "**🌐 Domain Information**\n\n"
                f"🔹 **Domain Name:** `{domain_info.domain_name}`\n"
                f"🏢 **Registrar:** `{domain_info.registrar}`\n"
                f"📅 **Creation Date:** `{domain_info.creation_date}`\n"
                f"📆 **Expiration Date:** `{domain_info.expiration_date}`"
            )  
        else:  
            response = "❌ Failed to retrieve domain hosting information."  

        await message.reply(response)  
    else:  
        await message.reply("⚠️ Please provide a domain name.\n\n**Example:** `/domain example.com`")
