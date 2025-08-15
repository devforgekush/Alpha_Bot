# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import os
import shutil
import requests
import yt_dlp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Audify import app
from config import BOT_LOGS_CHANNEL
from Audify.platforms.Youtube import extract_video_id, api_dl
from youtubesearchpython.__future__ import VideosSearch


def duration_to_seconds(duration_str: str) -> int:
    parts = duration_str.split(":")
    seconds = 0
    for i in range(len(parts)):
        seconds += int(parts[-(i + 1)]) * (60 ** i)
    return seconds


@app.on_message(filters.command(["song", "music"]))
async def song_handler(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❗ Provide a song name or YouTube link.")
    
    query = " ".join(message.command[1:])
    status = await message.reply_text("🔍 Searching for audio...")

    duration = 0
    try:
        video_id = extract_video_id(query)
        link = f"https://youtu.be/{video_id}"
        title = None
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    except:
        try:
            results = (await VideosSearch(query, limit=1).next())["result"]
            if not results:
                return await status.edit("❌ No results found.")
            video_id = results[0]["id"]
            link = results[0]["link"]
            title = results[0]["title"].strip().replace("/", "-").replace("\\", "-")
            thumbnail_url = results[0]["thumbnails"][0]["url"]
            duration_text = results[0].get("duration", None)
            if duration_text and ":" in duration_text:
                duration = duration_to_seconds(duration_text)
        except Exception as e:
            return await status.edit(f"❌ YouTube search failed.\nError: `{e}`")

    await status.edit("🎧 Downloading audio...")

    # Sanitize title
    if title:
        title = "".join(c if c.isalnum() or c in " ._-()" else "_" for c in title)

    new_filename = f"{title or video_id}.mp3"
    download_path = os.path.join("downloads", new_filename)
    os.makedirs("downloads", exist_ok=True)

    try:
        original_file_path = api_dl(video_id)
        if original_file_path:
            shutil.move(original_file_path, download_path)
        else:
            raise Exception("API returned nothing.")
    except Exception:
        await status.edit("⚠️ API failed, trying fallback method with cookies...")
        try:
            ydl_opts = {
                "format": "bestaudio[ext=m4a]/bestaudio/best",
                "outtmpl": download_path,
                "quiet": True,
                "nocheckcertificate": True,
                "cookies": "cookies/example.txt"
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=True)
                if not title:
                    title = info.get("title", f"yt-audio-{video_id}")
                    title = "".join(c if c.isalnum() or c in " ._-()" else "_" for c in title)
                    new_filename = f"{title}.mp3"
                    new_path = os.path.join("downloads", new_filename)
                    os.rename(download_path, new_path)
                    download_path = new_path
                if not duration:
                    duration = int(info.get("duration", 0))
        except Exception as ydl_err:
            return await status.edit(f"❌ Both API and fallback failed.\nError: `{ydl_err}`")

    # Download thumbnail
    thumb_path = None
    try:
        thumb_response = requests.get(thumbnail_url, stream=True)
        if thumb_response.status_code == 200:
            thumb_path = os.path.join("downloads", f"{video_id}_thumb.jpg")
            with open(thumb_path, "wb") as f:
                for chunk in thumb_response.iter_content(1024):
                    f.write(chunk)
    except:
        pass

    # Final caption and buttons
    caption = (
        f"🎶 <b>Track</b> : <b>{title}</b>\n\n"
        f"⏱️ <b>Duration</b> : {duration // 60} minutes {duration % 60:02d} seconds\n\n"
        f"🙋 <b>Requested by</b> : {message.from_user.mention}"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📺 Watch on YouTube", url=link)]
    ])

    try:
        # Send to user (group or PM)
        await message.reply_audio(
            audio=download_path,
            caption=caption,
            thumb=thumb_path,
            title=title,
            performer="YouTube",
            duration=duration,
            reply_markup=buttons
        )

        # ✅ Try logging to BOT_LOGS_CHANNEL
        try:
            await app.send_audio(
                chat_id=BOT_LOGS_CHANNEL,
                audio=download_path,
                caption=caption,
                thumb=thumb_path,
                title=title,
                performer="YouTube",
                duration=duration,
                reply_markup=buttons
            )
        except Exception as log_err:
            from Audify.logger import LOGGER
            LOGGER(__name__).error(f"[LOG ERROR] Could not send to BOT_LOGS_CHANNEL: {log_err}")

    except Exception as e:
        await status.edit(f"❌ Failed to send audio: `{e}`")
    else:
        await status.delete()

    # Cleanup
    try:
        os.remove(download_path)
        if thumb_path:
            os.remove(thumb_path)
    except:
        pass
