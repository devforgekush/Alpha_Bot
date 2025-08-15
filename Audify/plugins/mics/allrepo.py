# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import requests
from pyrogram import filters
from pyrogram.types import Message
from Audify import app


def chunk_string(text: str, size: int = 4000):
    """Split long text into chunks safe for Telegram messages."""
    return [text[i:i + size] for i in range(0, len(text), size)]


def get_all_repository_info(username: str):
    """Fetch all public repositories of a GitHub user."""
    url = f"https://api.github.com/users/{username}/repos"
    headers = {"Accept": "application/vnd.github+json"}
    response = requests.get(url, headers=headers)

    if response.status_code == 404:
        return None, "❌ GitHub user not found."
    elif response.status_code != 200:
        return None, f"⚠️ GitHub API error: {response.status_code}"

    repos = response.json()
    if not repos:
        return None, "ℹ️ No public repositories found."

    info = "\n\n".join([
        f"🔹 **{repo['name']}**\n"
        f"📜 {repo['description'] or 'No description'}\n"
        f"⭐ Stars: `{repo['stargazers_count']}` | 🍴 Forks: `{repo['forks_count']}`\n"
        f"🔗 [Visit Repo]({repo['html_url']})"
        for repo in repos
    ])

    return info, None


@app.on_message(filters.command("allrepo"))
async def allrepo_handler(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text("❖ Usage:\n`/allrepo <github_username>`", disable_web_page_preview=True)

    username = message.command[1]
    msg = await message.reply("🔍 Fetching repositories...")

    data, error = get_all_repository_info(username)
    if error:
        return await msg.edit(error)

    chunks = chunk_string(data)
    await msg.delete()
    for part in chunks:
        await message.reply_text(part, disable_web_page_preview=True)
