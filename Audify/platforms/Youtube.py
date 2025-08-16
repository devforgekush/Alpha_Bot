# ---------------------------------------------------------
# Alphabot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Alphabot project.
# Unauthorized copying, distribution, or use is prohibited.
# Developed by @devforgekush. All rights reserved.
# ---------------------------------------------------------

import asyncio
import os
import re
import json
from typing import Union
import yt_dlp

from pyrogram.enums import MessageEntityType
from pyrogram.types import Message


from Audify.utils.database import is_on_off
from Audify.utils.formatters import time_to_seconds

import glob
import random
import logging
import requests
import time

from config import API_BASE_URL

MIN_FILE_SIZE = 51200

# Compatibility shim: some httpx versions changed AsyncClient signature and do not
# accept the `proxies` kwarg used by youtubesearchpython. Patch AsyncClient at
# runtime to silently drop unknown `proxies` kwarg so the search package works
# with multiple httpx versions without requiring environment reinstallation.
try:
    import httpx as _httpx
    _orig_async_init = getattr(_httpx.AsyncClient, "__init__", None)

    if _orig_async_init is not None:
        def _patched_asyncclient_init(self, *args, **kwargs):
            # Drop `proxies` if provided by downstream libraries that expect it
            kwargs.pop("proxies", None)
            return _orig_async_init(self, *args, **kwargs)

        # Replace only if not already patched
        if getattr(_httpx.AsyncClient, "__init__", None) is _orig_async_init:
            _httpx.AsyncClient.__init__ = _patched_asyncclient_init
except Exception:
    # Best-effort shim; failures here are non-fatal and will be logged elsewhere
    pass

# Import VideosSearch after applying the httpx shim so the search package
# sees the patched AsyncClient signature.
from youtubesearchpython.__future__ import VideosSearch

def extract_video_id(link: str) -> str:
    patterns = [
        r'youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=)([0-9A-Za-z_-]{11})',
        r'youtu\.be\/([0-9A-Za-z_-]{11})',
        r'youtube\.com\/(?:playlist\?list=[^&]+&v=|v\/)([0-9A-Za-z_-]{11})',
        r'youtube\.com\/(?:.*\?v=|.*\/)([0-9A-Za-z_-]{11})'
    ]

    for pattern in patterns:
        match = re.search(pattern, link)
        if match:
            return match.group(1)

    raise ValueError("Invalid YouTube link provided.")

async def api_dl(link: str) -> str | None:
    """Download using our self-hosted YouTube API"""
    if not API_BASE_URL:
        from Audify.logger import LOGGER
        LOGGER(__name__).warning("API_BASE_URL not set, falling back to yt-dlp")
        return await fallback_dl(link)
    
    try:
        # Extract video ID
        video_id = extract_video_id(link)
        file_path = os.path.join("downloads", f"{video_id}.mp3")

        # Check if already downloaded
        if os.path.exists(file_path):
            from Audify.logger import LOGGER
            LOGGER(__name__).info(f"Song {file_path} already exists. Skipping download ✅")
            return file_path

        # Start download via API
        download_response = requests.post(f"{API_BASE_URL}/download", json={
            "url": link,
            "format": "bestaudio",
            "quality": "192"
        }, timeout=10)

        if download_response.status_code != 200:
            from Audify.logger import LOGGER
            from Audify.logger import LOGGER
            # Log response body for debugging
            try:
                body = download_response.text
            except Exception:
                body = '<unreadable body>'
            LOGGER(__name__).error(f"Failed to start download. Status: {download_response.status_code} - {body}")
            return await fallback_dl(link)

        task_id = download_response.json().get("task_id")
        if not task_id:
            from Audify.logger import LOGGER
            LOGGER(__name__).error("No task ID received from API")
            return await fallback_dl(link)

        # Wait for download to complete
        max_wait = 300  # 5 minutes max
        wait_time = 0
        while wait_time < max_wait:
            status_response = requests.get(f"{API_BASE_URL}/status/{task_id}", timeout=10)
            if status_response.status_code == 200:
                status_data = status_response.json()
                if status_data.get("status") == "completed":
                    # Download completed, get the file
                    file_response = requests.get(f"{API_BASE_URL}/download/{task_id}", timeout=30)
                    if file_response.status_code == 200:
                        os.makedirs("downloads", exist_ok=True)
                        with open(file_path, 'wb') as f:
                            f.write(file_response.content)

                        # Check file size
                        file_size = os.path.getsize(file_path)
                        if file_size < MIN_FILE_SIZE:
                            from Audify.logger import LOGGER
                            LOGGER(__name__).warning(f"Downloaded file is too small ({file_size} bytes). Keeping file for inspection.")
                            # Keep the file for debugging instead of removing it immediately
                            return file_path

                        from Audify.logger import LOGGER
                        LOGGER(__name__).info(f"Song Downloaded Successfully via API ✅ {file_path} ({file_size} bytes)")
                        return file_path
                    else:
                        from Audify.logger import LOGGER
                        LOGGER(__name__).error(f"Failed to get file from API. Status: {file_response.status_code}")
                        return await fallback_dl(link)
                elif status_data.get("status") == "failed":
                    from Audify.logger import LOGGER
                    LOGGER(__name__).error(f"Download failed via API: {status_data.get('error')}")
                    return await fallback_dl(link)
                else:
                    # Still downloading, wait
                    await asyncio.sleep(2)
                    wait_time += 2
            else:
                from Audify.logger import LOGGER
                LOGGER(__name__).warning(f"Failed to check status. Status: {status_response.status_code}")
                await asyncio.sleep(2)
                wait_time += 2

        # Timeout reached
        from Audify.logger import LOGGER
        LOGGER(__name__).warning("Download timeout via API, falling back to yt-dlp")
        return await fallback_dl(link)

    except Exception as e:
        from Audify.logger import LOGGER
        LOGGER(__name__).error(f"❌ API download error: {e}")
        return await fallback_dl(link)

async def fallback_dl(link: str) -> str | None:
    """Fallback to yt-dlp if API fails"""
    try:
        from Audify.logger import LOGGER
        LOGGER(__name__).info("Using yt-dlp fallback for download")
        
        video_id = extract_video_id(link)
        file_path = os.path.join("downloads", f"{video_id}.mp3")

        # Check if already downloaded
        if os.path.exists(file_path):
            return file_path

        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio',
            'outtmpl': file_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            # Keep original downloaded file for debugging (-k)
            'keepvideo': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        # Check file size
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            if file_size < MIN_FILE_SIZE:
                os.remove(file_path)
                return None
            return file_path
        return None

    except Exception as e:
        from Audify.logger import LOGGER
        LOGGER(__name__).error(f"❌ Fallback download error: {e}")
        return None

async def get_video_info(link: str) -> dict | None:
    """Get video information using our API or fallback"""
    if not API_BASE_URL:
        return await fallback_get_info(link)
    
    try:
        response = requests.post(f"{API_BASE_URL}/info", json={
            "url": link,
            "format": "bestaudio"
        }, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return {
                "title": data.get("title"),
                "duration": data.get("duration"),
                "thumbnail": data.get("thumbnail"),
                "uploader": data.get("uploader"),
                "view_count": data.get("view_count")
            }
        else:
            return await fallback_get_info(link)

    except Exception as e:
        from Audify.logger import LOGGER
        LOGGER(__name__).error(f"❌ API info error: {e}")
        return await fallback_get_info(link)

async def fallback_get_info(link: str) -> dict | None:
    """Fallback to yt-dlp for video info"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            return {
                "title": info.get('title'),
                "duration": info.get('duration'),
                "thumbnail": info.get('thumbnail'),
                "uploader": info.get('uploader'),
                "view_count": info.get('view_count')
            }
    except Exception as e:
        from Audify.logger import LOGGER
        LOGGER(__name__).error(f"❌ Fallback info error: {e}")
        return None





def cookie_txt_file():
    # Use os.path to be platform-independent and ensure the cookies folder exists
    folder_path = os.path.join(os.getcwd(), "cookies")
    os.makedirs(folder_path, exist_ok=True)
    logs_path = os.path.join(folder_path, "logs.csv")

    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
    if not txt_files:
        # No cookie files available — log and return None so callers can fall back
        from Audify.logger import LOGGER
        LOGGER(__name__).warning("No cookie .txt files found in cookies/; continuing without cookies")
        return None

    chosen = random.choice(txt_files)
    # Record which cookie file was chosen for debugging
    try:
        with open(logs_path, "a", encoding="utf-8") as file:
            file.write(f"Chosen cookie file: {chosen}\n")
    except Exception:
        pass

    # Return absolute path (yt-dlp accepts this directly)
    return os.path.abspath(chosen)



    async def check_file_size(link):
    async def get_format_info(link):
        # Build command arguments safely and include cookies only if available
        c = cookie_txt_file()
        args = ["yt-dlp"]
        if c:
            args += ["--cookies", c]
        args += ["-J", link]
        proc = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            from Audify.logger import LOGGER
            LOGGER(__name__).error(f'Error:\n{stderr.decode()}')
            return None
        return json.loads(stdout.decode())

    def parse_size(formats):
        total_size = 0
        for format in formats:
            if 'filesize' in format:
                total_size += format['filesize']
        return total_size

    info = await get_format_info(link)
    if info is None:
        return None
    
    formats = info.get('formats', [])
    if not formats:
        from Audify.logger import LOGGER
        LOGGER(__name__).error("No formats found.")
        return None
    
    total_size = parse_size(formats)
    return total_size

async def shell_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, errorz = await proc.communicate()
    if errorz:
        if "unavailable videos are hidden" in (errorz.decode("utf-8")).lower():
            return out.decode("utf-8")
        else:
            return errorz.decode("utf-8")
    return out.decode("utf-8")


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if re.search(self.regex, link):
            return True
        else:
            return False

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        text = ""
        offset = None
        length = None
        for message in messages:
            if offset:
                break
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        offset, length = entity.offset, entity.length
                        break
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        if offset in (None,):
            return None
        return text[offset : offset + length]

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            vidid = result["id"]
            if str(duration_min) == "None":
                duration_sec = 0
            else:
                duration_sec = int(time_to_seconds(duration_min))
        return title, duration_min, duration_sec, thumbnail, vidid

    async def title(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
        return title

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            duration = result["duration"]
        return duration

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        return thumbnail

    async def video(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        # Build command arguments safely and include cookies only if available
        c = cookie_txt_file()
        args = ["yt-dlp"]
        if c:
            args += ["--cookies", c]
        args += ["-g", "-f", "best[height<=?720][width<=?1280]", f"{link}"]
        proc = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if stdout:
            return 1, stdout.decode().split("\n")[0]
        else:
            return 0, stderr.decode()

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if videoid:
            link = self.listbase + link
        if "&" in link:
            link = link.split("&")[0]
        playlist = await shell_cmd(
            (lambda: (f"yt-dlp -i --get-id --flat-playlist --cookies {c} --playlist-end {limit} --skip-download {link}") if (c:=cookie_txt_file()) else f"yt-dlp -i --get-id --flat-playlist --playlist-end {limit} --skip-download {link}")() 
        )
        try:
            result = playlist.split("\n")
            for key in result:
                if key == "":
                    result.remove(key)
        except:
            result = []
        return result

    async def track(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            vidid = result["id"]
            yturl = result["link"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        track_details = {
            "title": title,
            "link": yturl,
            "vidid": vidid,
            "duration_min": duration_min,
            "thumb": thumbnail,
        }
        return track_details, vidid

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        c = cookie_txt_file()
        ytdl_opts = {"quiet": True}
        if c:
            ytdl_opts["cookiefile"] = c
        ydl = yt_dlp.YoutubeDL(ytdl_opts)
        with ydl:
            formats_available = []
            r = ydl.extract_info(link, download=False)
            for format in r["formats"]:
                try:
                    str(format["format"])
                except:
                    continue
                if not "dash" in str(format["format"]).lower():
                    try:
                        format["format"]
                        format["filesize"]
                        format["format_id"]
                        format["ext"]
                        format["format_note"]
                    except:
                        continue
                    formats_available.append(
                        {
                            "format": format["format"],
                            "filesize": format["filesize"],
                            "format_id": format["format_id"],
                            "ext": format["ext"],
                            "format_note": format["format_note"],
                            "yturl": link,
                        }
                    )
        return formats_available, link

    async def slider(
        self,
        link: str,
        query_type: int,
        videoid: Union[bool, str] = None,
    ):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        a = VideosSearch(link, limit=10)
        result = (await a.next()).get("result")
        title = result[query_type]["title"]
        duration_min = result[query_type]["duration"]
        vidid = result[query_type]["id"]
        thumbnail = result[query_type]["thumbnails"][0]["url"].split("?")[0]
        return title, duration_min, thumbnail, vidid

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> str:
        if videoid:
            link = self.base + link
        loop = asyncio.get_running_loop()
        
        def audio_dl():
            try:
                sexid = extract_video_id(link)
                # api_dl is async; run it synchronously here because this function
                # executes inside a thread via run_in_executor
                # Pass the original link to api_dl (not the extracted id).
                # Passing only the id caused extract_video_id inside api_dl to fail.
                from Audify.logger import LOGGER
                LOGGER(__name__).debug(f"Attempting API download for link: {link} (id: {sexid})")
                path = asyncio.run(api_dl(link))
                if path:
                    return path
                else:
                    from Audify.logger import LOGGER
                    LOGGER(__name__).warning("API download returned None. Falling back to yt-dlp.")
            except Exception as e:
                from Audify.logger import LOGGER
                LOGGER(__name__).error(f"API failed: {e}. Falling back to yt-dlp.")

            # yt-dlp fallback
            ydl_optssx = {
                "format": "bestaudio/best",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                **({"cookiefile": cookie_txt_file()} if cookie_txt_file() else {}),
                "no_warnings": True,
            }

            try:
                x = yt_dlp.YoutubeDL(ydl_optssx)
                info = x.extract_info(link, False)
                xyz = os.path.join("downloads", f"{info['id']}.{info['ext']}")
                if os.path.exists(xyz):
                    return xyz
                x.download([link])
                return xyz
            except Exception as e:
                from Audify.logger import LOGGER
                LOGGER(__name__).error(f"yt-dlp failed: {e}")
                return None

        def video_dl():
            ydl_optssx = {
                "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                **({"cookiefile": cookie_txt_file()} if cookie_txt_file() else {}),
                "no_warnings": True,
            }
            x = yt_dlp.YoutubeDL(ydl_optssx)
            info = x.extract_info(link, False)
            xyz = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if os.path.exists(xyz):
                return xyz
            x.download([link])
            return xyz

        def song_video_dl():
            formats = f"{format_id}+140"
            fpath = f"downloads/{title}"
            ydl_optssx = {
                "format": formats,
                "outtmpl": fpath,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                **({"cookiefile": cookie_txt_file()} if cookie_txt_file() else {}),
                "prefer_ffmpeg": True,
                "merge_output_format": "mp4",
            }
            x = yt_dlp.YoutubeDL(ydl_optssx)
            x.download([link])

        def song_audio_dl():
            fpath = f"downloads/{title}.%(ext)s"
            ydl_optssx = {
                "format": format_id,
                "outtmpl": fpath,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                **({"cookiefile": cookie_txt_file()} if cookie_txt_file() else {}),
                "prefer_ffmpeg": True,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }
            x = yt_dlp.YoutubeDL(ydl_optssx)
            x.download([link])

        if songvideo:
            await loop.run_in_executor(None, song_video_dl)
            fpath = f"downloads/{title}.mp4"
            return fpath
        elif songaudio:
            await loop.run_in_executor(None, song_audio_dl)
            fpath = f"downloads/{title}.mp3"
            return fpath
        elif video:
            if await is_on_off(1):
                direct = True
                downloaded_file = await loop.run_in_executor(None, video_dl)
            else:
                # Build command arguments safely and include cookies only if available
                c = cookie_txt_file()
                args = ["yt-dlp"]
                if c:
                    args += ["--cookies", c]
                args += ["-g", "-f", "best[height<=?720][width<=?1280]", f"{link}"]
                proc = await asyncio.create_subprocess_exec(
                    *args,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await proc.communicate()
                if stdout:
                    downloaded_file = stdout.decode().split("\n")[0]
                    direct = False
                else:
                   file_size = await check_file_size(link)
                   if not file_size:
                     from Audify.logger import LOGGER
                     LOGGER(__name__).error("None file Size")
                     return
                   total_size_mb = file_size / (1024 * 1024)
                   if total_size_mb > 250:
                     from Audify.logger import LOGGER
                     LOGGER(__name__).error(f"File size {total_size_mb:.2f} MB exceeds the 100MB limit.")
                     return None
                   direct = True
                   downloaded_file = await loop.run_in_executor(None, video_dl)
        else:
            direct = True
            downloaded_file = await loop.run_in_executor(None, audio_dl)
        return downloaded_file, direct
