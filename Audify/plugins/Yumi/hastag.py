import requests
from bs4 import BeautifulSoup as BSP
from Audify import app as Audify
from pyrogram import filters

url = "https://all-hashtag.com"

@Audify.on_message(filters.command("hastag"))
async def hastag(bot, message):
    try:
        text = message.text.split(' ', 1)[1]
    except IndexError:
        return await message.reply_text("❗ Example:\n\n`/hastag python`")

    data = dict(keyword=text, filter="top")
    
    try:
        res = requests.post(url, data=data, timeout=10).text
        soup = BSP(res, 'html.parser')
        hashtag_div = soup.find("div", {"class": "copy-hashtags"})

        if hashtag_div and hashtag_div.string:
            content = hashtag_div.string.strip()
        else:
            content = "❌ No hashtags found. The source website may have changed."

    except Exception as e:
        content = f"⚠️ An error occurred while fetching hashtags:\n`{e}`"

    await message.reply_text(
        f"🔖 **Top Hashtags for:** `{text}`\n\n"
        f"<pre>{content}</pre>",
        quote=True
    )


# Module Info
mod_name = "Hashtag"

help = """
🔖 **Hashtag Generator Help**

Generate top trending hashtags based on any keyword you enter.

**Usage:**
• `/hastag <keyword>` – Generates relevant hashtags.

💡 **Example:**  
`/hastag python`

This fetches the top 30+ hashtags related to your keyword.

**◆ Powered by ⤷ [AudifyBot](https://t.me/AudifyBot) ⚡**
"""
