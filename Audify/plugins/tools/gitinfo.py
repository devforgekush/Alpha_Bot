# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import aiohttp
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from Audify import app
from config import SUPPORT_CHAT


@app.on_message(filters.command(["github", "git"]))
async def github(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "📦 Usage: <code>/git &lt;github_username&gt;</code>", parse_mode=ParseMode.HTML
        )

    username = message.text.split(None, 1)[1]
    url = f"https://api.github.com/users/{username}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 404:
                return await message.reply_text("❌ GitHub user not found.")
            data = await response.json()

    try:
        html_url = data.get("html_url", "N/A")
        name = data.get("name", "N/A")
        company = data.get("company", "N/A")
        bio = data.get("bio", "N/A")
        created_at = data.get("created_at", "N/A")
        avatar_url = data.get("avatar_url")
        blog = data.get("blog", "N/A")
        location = data.get("location", "N/A")
        public_repos = data.get("public_repos", 0)
        followers = data.get("followers", 0)
        following = data.get("following", 0)

        caption = f"""<b>👤 GitHub Info of {name}</b>

<b>Username:</b> <code>{username}</code>
<b>Bio:</b> {bio}
<b>Profile:</b> <a href="{html_url}">Click Here</a>
<b>Company:</b> {company}
<b>Blog:</b> {blog}
<b>Location:</b> {location}
<b>Created on:</b> {created_at}
<b>Repositories:</b> {public_repos}
<b>Followers:</b> {followers}
<b>Following:</b> {following}"""

    except Exception:
        return await message.reply_text("⚠️ Failed to parse GitHub data.")

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 Support", url=SUPPORT_CHAY)],
        [InlineKeyboardButton("❌ Close", callback_data="close")]
    ])

    await message.reply_photo(
        photo=avatar_url,
        caption=caption,
        reply_markup=buttons,
        parse_mode=ParseMode.HTML
    )


@app.on_callback_query(filters.regex("close_gitinfo"))
async def close_gitinfo(_, query):
    try:
        await query.message.delete()
    except:
        await query.answer("⚠️ I can't delete this message.", show_alert=True)
