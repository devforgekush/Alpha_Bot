# ---------------------------------------------------------
# Alphabot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Alphabot project.
# Unauthorized copying, distribution, or use is prohibited.
# Developed by @devforgekush. All rights reserved.
# ---------------------------------------------------------

import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Telegram API Credentials
API_ID = int(getenv("API_ID", "0"))
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")
OWNER_ID = int(getenv("OWNER_ID", "0"))

# Music API Configs
API_BASE_URL = getenv("API_URL", "http://deadlinetech.site") #API Config ~
API_KEY = getenv("API_KEY", None)
DOWNLOADS_DIR = "downloads"

# Basic Bot Configs
OWNER_USERNAME = getenv("OWNER_USERNAME", "Nikchil") #Replace With Yours ~
BOT_USERNAME = getenv("BOT_USERNAME", "AlphabotMusicBot") #Replace With Yours ~
BOT_NAME = getenv("BOT_NAME", "Alphabot") #Replace With Yours ~
ASSUSERNAME = getenv("ASSUSERNAME", "AlphabotAssistant") #Replace With Yours ~
LOGGER_ID = int(getenv("LOGGER_ID", "-1002723963783")) #Replace With Yours ~
BOT_LOGS_CHANNEL = int(getenv("BOT_LOGS_CHANNEL", "-1002731989493")) #Replace With Yours ~

# MongoDB
MONGO_DB_URI = getenv("MONGO_DB_URI", None)

# Duration
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", "99999"))
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION", "99999"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "99999"))
DURATION_LIMIT = DURATION_LIMIT_MIN * 60

# Auto-leave
AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", "True")
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", "9000"))

# Spotify
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "")

# Heroku (if used)
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME", None)
HEROKU_API_KEY = getenv("HEROKU_API_KEY", None)

# GitHub Upstream
UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/devforgekush/Alphabot",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv(
    "GIT_TOKEN", None
)  # Fill this variable if your upstream repository is private

# Support
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/devforgekush")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/devforgekush")
SOURCE_CODE = getenv("SOURCE_CODE", "https://github.com/devforgekush/Alphabot")
PRIVACY_LINK = getenv("PRIVACY_LINK", "https://telegra.ph/Privacy-Policy-for-Alphabot-Music--Management-08-02-2")

# Playlist
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "9999"))

# File Size Limits
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "5242880000"))  # ~5GB
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "5242880000"))

# String Sessions (for assistant accounts)
STRING1 = getenv("STRING_SESSION")
STRING2 = getenv("STRING_SESSION2")
STRING3 = getenv("STRING_SESSION3")
STRING4 = getenv("STRING_SESSION4")
STRING5 = getenv("STRING_SESSION5")
STRING6 = getenv("STRING_SESSION6")
STRING7 = getenv("STRING_SESSION7")

# Pyrogram Filter for Banned Users (empty list for now)
BANNED_USERS = filters.user([])

# Runtime Dicts (used in other modules)
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

# Image URLs
FAILED = "https://graph.org/file/40581c7048b1ee71209a2-3fc027862ecf64213d.jpg"


START_IMG_URL = getenv(
    "START_IMG_URL", "https://files.catbox.moe/6icik4.jpg"
)
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://graph.org//file/389a372e8ae039320ca6c.png"
)
PLAYLIST_IMG_URL = "https://graph.org/file/181aa7849a10b02c987af-3ed7c406488afb8389.png"
STATS_IMG_URL = "https://files.catbox.moe/5c6l8t.jpg"
TELEGRAM_AUDIO_URL = "https://graph.org/file/58423ce08560e7b078893-dee03d11a8d2d8dc37.jpg"
TELEGRAM_VIDEO_URL = "https://graph.org/file/33afb16c7189bceacefe0-74995e839947523d17.jpg"
STREAM_IMG_URL = "https://graph.org/file/355049c9d40478b2890e2-1c8825760a341234a3.jpg"
SOUNCLOUD_IMG_URL = "https://graph.org/file/fd1bdb1d8e19d40a3c241-8a83b57c5ba39ce6ad.jpg"
YOUTUBE_IMG_URL = "https://graph.org/file/4984f01e60e4c3a33f13f-e8406f1d5fda98cec6.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://graph.org/file/82d9fe1362c4f08071186-d835e3fbe0be49644b.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://graph.org/file/b201e5be7cd9716393f04-87eae1b7cfa3c6f7d5.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://graph.org/file/b18477171fc292a9d76f5-d8fe58ae744f447e44.jpg"

# Helper Function
def time_to_seconds(time: str) -> int:
    return sum(int(x) * 60**i for i, x in enumerate(reversed(time.split(":"))))

# URL Validations
if SUPPORT_CHANNEL and not re.match(r"(?:http|https)://", SUPPORT_CHANNEL):
    raise SystemExit("[ERROR] - SUPPORT_CHANNEL must start with http:// or https://")

if SUPPORT_CHAT and not re.match(r"(?:http|https)://", SUPPORT_CHAT):
    raise SystemExit("[ERROR] - SUPPORT_CHAT must start with http:// or https://")

if SOURCE_CODE and not re.match(r"(?:http|https)://", SOURCE_CODE):
    raise SystemExit("[ERROR] - SOURCE_CODE must start with http:// or https://")
