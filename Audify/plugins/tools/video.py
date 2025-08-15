from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Audify import app
from Audify.platforms.Youtube import extract_video_id
from youtubesearchpython.__future__ import VideosSearch
import os
import requests
import yt_dlp

def duration_to_seconds(duration_str):
    parts = duration_str.split(":")
    seconds = 0
    for i in range(len(parts)):
        seconds += int(parts[-(i + 1)]) * (60 ** i)
    return seconds

def sanitize_filename(title: str):
    return "".join(c if c.isalnum() or c in " ._-()" else "_" for c in title)

@app.on_message(filters.command(["video"]))
async def video_handler(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❗ Provide a video name or YouTube link.")
    
    query = " ".join(message.command[1:])
    status = await message.reply_text("🔍 Searching for video...")

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
            title = sanitize_filename(results[0]["title"])
            thumbnail_url = results[0]["thumbnails"][0]["url"]
            duration_text = results[0].get("duration", None)
            if duration_text:
                duration = duration_to_seconds(duration_text)
        except Exception as e:
            return await status.edit(f"❌ YouTube search failed.\nError: `{e}`")

    await status.edit("📥 Downloading video...")

    try:
        ydl_opts = {
            "format": "(bestvideo[height<=720][ext=mp4])+bestaudio[ext=m4a]",
            "outtmpl": f"downloads/{video_id}.%(ext)s",
            "geo_bypass": True,
            "nocheckcertificate": True,
            "quiet": True,
            "cookiefile": "cookies/cookies.txt",
            "no_warnings": True,
            "prefer_ffmpeg": True,
            "merge_output_format": "mp4",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            filename = f"{info['id']}.{info['ext']}"
            filepath = os.path.join("downloads", filename)

            if not os.path.exists(filepath):
                ydl.download([link])

        if not title:
            title = sanitize_filename(info.get("title", f"yt-video-{video_id}"))
        if not duration:
            duration = int(info.get("duration", 0))

    except Exception as e:
        return await status.edit(f"❌ Download failed. Video may be age-restricted or blocked.\n\n`{e}`")

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

    caption = (
        f"📹 <b>Video</b> : <b>{title}</b>\n\n"
        f"⏱️ <b>Duration</b> : {duration // 60} minutes {duration % 60:02d} seconds\n\n"
        f"🙋 <b>Requested by</b> : {message.from_user.mention}"
    )
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("📺 Watch on YouTube", url=link)]])

    try:
        await message.reply_video(
            video=filepath,
            caption=caption,
            thumb=thumb_path,
            width=1280,
            height=720,
            duration=duration,
            reply_markup=buttons
        )
    except Exception as e:
        await status.edit(f"❌ Failed to send video: `{e}`")
    else:
        await status.delete()

    # Cleanup
    try:
        os.remove(filepath)
        if thumb_path:
            os.remove(thumb_path)
    except:
        pass
