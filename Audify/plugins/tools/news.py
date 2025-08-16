import requests
from bs4 import BeautifulSoup
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from Audify import app

# --- /news Command: Fetch general or keyword-based news headlines ---
@app.on_message(filters.command("news"))
async def fetch_news(_, message: Message):
    query = " ".join(message.command[1:]) or "latest"
    await message.reply_chat_action(ChatAction.TYPING)

    try:
        url = f"https://www.bing.com/news/search?q={query}&FORM=HDRSC6"
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        results = soup.find_all("a", class_="title", limit=5)

        if not results:
            return await message.reply_text("❌ No news found for your query.")

        news_msg = f"🗞 **Top News Results for:** `{query}`\n\n"
        for i, result in enumerate(results, 1):
            title = result.text.strip()
            link = result['href']
            news_msg += f"• [{title}]({link})\n"

        await message.reply_text(news_msg, disable_web_page_preview=True)

    except Exception as e:
        await message.reply_text("⚠️ Failed to fetch news. Try again later.")


# --- /bing Command: Perform a basic web search ---
@app.on_message(filters.command("bing"))
async def bing_search(_, message: Message):
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply_text("❗ Usage: `/bing [query]`", quote=True)

    await message.reply_chat_action(ChatAction.TYPING)
    try:
        url = f"https://www.bing.com/search?q={query}"
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        results = soup.find_all("li", class_="b_algo", limit=5)

        if not results:
            return await message.reply_text("❌ No results found.")

        text = f"🔎 **Bing Results for:** `{query}`\n\n"
        for result in results:
            title = result.find("a").text
            link = result.find("a")["href"]
            text += f"• [{title}]({link})\n"

        await message.reply_text(text, disable_web_page_preview=True)

    except Exception:
        await message.reply_text("⚠️ Failed to search Bing. Please try again.")


# --- /img Command: Perform image search using Bing Images ---
@app.on_message(filters.command("img"))
async def image_search(_, message: Message):
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply_text("❗ Usage: `/img [query]`", quote=True)

    await message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
    try:
        url = f"https://www.bing.com/images/search?q={query}"
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        images = soup.find_all("a", class_="iusc", limit=5)

        if not images:
            return await message.reply_text("❌ No images found.")

        image_links = []
        for img in images:
            m = img.get("m")
            if m and "murl" in m:
                link = eval(m)["murl"]
                image_links.append(link)

        if not image_links:
            return await message.reply_text("⚠️ Couldn’t fetch image URLs.")

        for link in image_links[:3]:
            await app.send_photo(message.chat.id, photo=link)

    except Exception:
        await message.reply_text("⚠️ Image search failed. Please try again.")
