# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import aiohttp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from Audify import app

API_URL = "https://graphql.anilist.co"

async def fetch_anilist(query: str, variables: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json={"query": query, "variables": variables}) as response:
            return await response.json()

# ─────────────────────────────────────────────

@app.on_message(filters.command("anime"))
async def anime_search(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("🌀 Usage: `/anime [anime name]`", quote=True)
    name = message.text.split(None, 1)[1]

    query = """
    query ($search: String) {
      Media(search: $search, type: ANIME) {
        title {
          romaji
          english
        }
        description(asHtml: false)
        episodes
        status
        genres
        averageScore
        siteUrl
        coverImage {
          large
        }
      }
    }
    """
    result = await fetch_anilist(query, {"search": name})
    data = result.get("data", {}).get("Media")

    if not data:
        return await message.reply("🚫 No anime found!", quote=True)

    desc = (data["description"] or "No description").replace("<br>", "").replace("\n", " ")
    if len(desc) > 700:
        desc = desc[:700] + "..."

    caption = (
        f"**🎌 {data['title']['romaji']} ({data['title'].get('english', 'N/A')})**\n\n"
        f"📝 **Description:** {desc}\n"
        f"🎬 **Episodes:** {data.get('episodes', 'N/A')}\n"
        f"📊 **Score:** {data.get('averageScore', 'N/A')}%\n"
        f"📺 **Status:** {data['status']}\n"
        f"🏷️ **Genres:** `{', '.join(data.get('genres', []))}`"
    )

    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🌐 View on AniList", url=data["siteUrl"])]]
    )

    await message.reply_photo(photo=data["coverImage"]["large"], caption=caption, reply_markup=buttons)

# ─────────────────────────────────────────────

@app.on_message(filters.command("manga"))
async def manga_search(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("📚 Usage: `/manga [manga name]`", quote=True)
    name = message.text.split(None, 1)[1]

    query = """
    query ($search: String) {
      Media(search: $search, type: MANGA) {
        title {
          romaji
          english
        }
        description(asHtml: false)
        chapters
        volumes
        status
        genres
        averageScore
        siteUrl
        coverImage {
          large
        }
      }
    }
    """
    result = await fetch_anilist(query, {"search": name})
    data = result.get("data", {}).get("Media")

    if not data:
        return await message.reply("🚫 No manga found!", quote=True)

    desc = (data["description"] or "No description").replace("<br>", "").replace("\n", " ")
    if len(desc) > 700:
        desc = desc[:700] + "..."

    caption = (
        f"**📚 {data['title']['romaji']} ({data['title'].get('english', 'N/A')})**\n\n"
        f"📝 **Description:** {desc}\n"
        f"📖 **Chapters:** {data.get('chapters', 'N/A')}\n"
        f"📦 **Volumes:** {data.get('volumes', 'N/A')}\n"
        f"📊 **Score:** {data.get('averageScore', 'N/A')}%\n"
        f"📺 **Status:** {data['status']}\n"
        f"🏷️ **Genres:** `{', '.join(data.get('genres', []))}`"
    )

    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🌐 View on AniList", url=data["siteUrl"])]]
    )

    await message.reply_photo(photo=data["coverImage"]["large"], caption=caption, reply_markup=buttons)

# ─────────────────────────────────────────────

@app.on_message(filters.command("character"))
async def character_search(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("👤 Usage: `/character [name]`", quote=True)
    name = message.text.split(None, 1)[1]

    query = """
    query ($search: String) {
      Character(search: $search) {
        name {
          full
          native
        }
        image {
          large
        }
        description
        siteUrl
      }
    }
    """
    result = await fetch_anilist(query, {"search": name})
    data = result.get("data", {}).get("Character")

    if not data:
        return await message.reply("🚫 No character found!", quote=True)

    desc = (data.get("description") or "No description").replace("<br>", "").replace("\n", " ")
    if len(desc) > 500:
        desc = desc[:500] + "..."

    caption = (
        f"**👤 {data['name']['full']} ({data['name']['native']})**\n\n"
        f"📝 {desc}"
    )

    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🌐 View on AniList", url=data["siteUrl"])]]
    )

    await message.reply_photo(photo=data["image"]["large"], caption=caption, reply_markup=buttons)

# ─────────────────────────────────────────────

@app.on_message(filters.command("gettags"))
async def get_tags(_, message: Message):
    tags = [
        "Action", "Adventure", "Comedy", "Drama", "Ecchi", "Fantasy", "Horror",
        "Mahou Shoujo", "Mecha", "Music", "Mystery", "Psychological", "Romance",
        "Sci-Fi", "Slice of Life", "Sports", "Supernatural", "Thriller"
    ]
    await message.reply("🏷️ **Available Genre Tags:**\n\n" + " | ".join(tags))

# ─────────────────────────────────────────────

@app.on_message(filters.command("browse"))
async def browse_anime(_, message: Message):
    query = """
    query {
      Page(perPage: 5) {
        media(sort: TRENDING_DESC, type: ANIME) {
          title {
            romaji
          }
          siteUrl
        }
      }
    }
    """
    result = await fetch_anilist(query, {})
    data = result.get("data", {}).get("Page", {}).get("media", [])

    if not data:
        return await message.reply("❌ Couldn't fetch trending anime.")

    text = "🔍 **Trending Anime:**\n\n"
    for i, item in enumerate(data, 1):
        text += f"{i}. [{item['title']['romaji']}]({item['siteUrl']})\n"

    await message.reply(text, disable_web_page_preview=True)

# ─────────────────────────────────────────────

@app.on_message(filters.command("airing"))
async def airing_schedule(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("📺 Usage: `/airing [anime]`", quote=True)
    name = message.text.split(None, 1)[1]

    query = """
    query ($search: String) {
      Media(search: $search, type: ANIME) {
        title {
          romaji
        }
        airingSchedule(notYetAired: true, perPage: 5) {
          nodes {
            episode
            airingAt
          }
        }
      }
    }
    """

    result = await fetch_anilist(query, {"search": name})
    media = result.get("data", {}).get("Media")

    if not media or not media.get("airingSchedule", {}).get("nodes"):
        return await message.reply("❌ No upcoming schedule found.", quote=True)

    from datetime import datetime
    text = f"📺 **Upcoming Episodes for {media['title']['romaji']}**\n\n"
    for ep in media["airingSchedule"]["nodes"]:
        air_time = datetime.utcfromtimestamp(ep["airingAt"]).strftime('%Y-%m-%d %H:%M UTC')
        text += f"• Episode {ep['episode']} airs at **{air_time}**\n"

    await message.reply(text)

# ─────────────────────────────────────────────

@app.on_message(filters.command("topanime"))
async def top_anime(_, message: Message):
    query = """
    query {
      Page(perPage: 5) {
        media(sort: SCORE_DESC, type: ANIME) {
          title {
            romaji
          }
          averageScore
          siteUrl
        }
      }
    }
    """
    result = await fetch_anilist(query, {})
    media = result.get("data", {}).get("Page", {}).get("media", [])

    if not media:
        return await message.reply("🏆 Couldn't fetch top anime!")

    text = "🏆 **Top Anime Rankings:**\n\n"
    for i, item in enumerate(media, 1):
        text += f"{i}. [{item['title']['romaji']}]({item['siteUrl']}) — {item['averageScore']}%\n"

    await message.reply(text, disable_web_page_preview=True)

# ─────────────────────────────────────────────

@app.on_message(filters.command("anisettings"))
async def ani_settings(_, message: Message):
    await message.reply("⚙️ No settings yet.\nSoon you’ll be able to personalize your anime experience!")
