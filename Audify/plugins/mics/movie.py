# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import filters
from pyrogram.types import Message
from Audify import app
import requests

# TMDb API Key (keep this secure)
TMDB_API_KEY = "23c3b139c6d59ebb608fe6d5b974d888"


@app.on_message(filters.command("movie"))
async def movie_command(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "🎬 <b>Please provide a movie name.</b>\n\n"
            "Usage: <code>/movie Inception</code>"
        )

    query = " ".join(message.command[1:])
    try:
        info = get_movie_info(query)
        await message.reply_text(info if info else "❌ <b>Could not retrieve movie details.</b>")
    except Exception as e:
        await message.reply_text(f"❌ <b>Error:</b> <code>{str(e)}</code>")


def get_movie_info(movie_name: str) -> str:
    search_url = "https://api.themoviedb.org/3/search/movie"
    search_params = {
        "api_key": TMDB_API_KEY,
        "query": movie_name,
    }

    res = requests.get(search_url, params=search_params)
    if res.status_code != 200:
        return "❌ <b>Failed to connect to TMDb API.</b>"

    results = res.json().get("results")
    if not results:
        return "❌ <b>No results found for that movie name.</b>"

    movie = results[0]
    movie_id = movie["id"]

    # Get detailed movie info
    detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    detail_res = requests.get(detail_url, params={"api_key": TMDB_API_KEY})
    details = detail_res.json()

    # Get cast
    cast_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    cast_res = requests.get(cast_url, params={"api_key": TMDB_API_KEY})
    cast_data = cast_res.json()
    cast_list = cast_data.get("cast", [])
    actors = ", ".join([actor["name"] for actor in cast_list[:5]]) or "N/A"

    # Extract fields
    title = details.get("title", "N/A")
    release_date = details.get("release_date", "N/A")
    overview = details.get("overview", "N/A")
    vote = details.get("vote_average", "N/A")
    revenue = details.get("revenue", "N/A")

    # Format the response
    return (
        f"🎬 <b>Title:</b> {title}\n"
        f"📆 <b>Release Date:</b> {release_date}\n"
        f"📝 <b>Overview:</b>\n{overview}\n\n"
        f"⭐ <b>Rating:</b> {vote}/10\n"
        f"🎭 <b>Cast:</b> {actors}\n"
        f"💰 <b>Box Office:</b> ${revenue:,}\n"
    )
