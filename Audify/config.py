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

# Railway Configuration
RAILWAY_URL = getenv("RAILWAY_URL", None)

# API Configuration for YouTube downloads
API_KEY = getenv("API_KEY", None)
API_BASE_URL = getenv("API_BASE_URL", None)

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
