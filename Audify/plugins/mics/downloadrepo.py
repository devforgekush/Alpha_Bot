# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from Audify import app
import git
import shutil
import os

# ── /downloadrepo ─────────────────────────────
@app.on_message(filters.command("downloadrepo"))
async def download_repo(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**Usage:** `/downloadrepo <GitHub Repo URL>`\n\n"
            "Example:\n`/downloadrepo https://github.com/username/repo.git`"
        )

    repo_url = message.command[1]
    status = await message.reply("📥 Cloning and zipping repository...")

    zip_path = await clone_and_zip(repo_url)

    if zip_path:
        try:
            await message.reply_document(
                document=zip_path,
                caption="✅ Repository cloned and zipped successfully!",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("✖ Close", callback_data="close")]]
                )
            )
        except Exception as e:
            await status.edit(f"⚠️ Error while sending file: `{e}`")
        finally:
            if os.path.exists(zip_path):
                os.remove(zip_path)
    else:
        await status.edit("❌ Failed to clone the repository. Make sure the URL is valid.")


# ── Clone and Zip GitHub Repository ─────────────────────
async def clone_and_zip(repo_url: str) -> str | None:
    try:
        repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
        repo_path = f"temp_{repo_name}"

        # Clone the repository
        git.Repo.clone_from(repo_url, repo_path)

        # Zip the cloned repo
        zip_path = shutil.make_archive(repo_path, "zip", repo_path)
        return zip_path
    except Exception as e:
    from Audify.logger import LOGGER
    LOGGER(__name__).error(f"[DOWNLOADREPO ERROR] - {e}")
        return None
    finally:
        # Clean the temp directory if it exists
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
