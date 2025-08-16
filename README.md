# 🎵 Alphabot - Telegram Music Bot

A powerful Telegram music bot with support for multiple platforms including YouTube, Spotify, Apple Music, and more.

## 🚀 Railway Deployment

### Prerequisites
- Python 3.11+
- MongoDB database
- Telegram Bot Token
- Pyrogram API credentials

### 🆕 **NEW: Self-Hosted YouTube API (100% FREE!)**

Your bot now includes a **completely free, self-hosted YouTube download API** that runs on Railway alongside your bot!

**Benefits:**
- ✅ **100% FREE** forever
- ✅ **No rate limits**
- ✅ **No external dependencies**
- ✅ **Always available**
- ✅ **Faster downloads**
- ✅ **Better reliability**

### Environment Variables

#### Required Variables
```env
# Telegram API Credentials
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
OWNER_ID=your_user_id

# Bot Configuration
LOGGER_ID=your_log_channel_id
BOT_LOGS_CHANNEL=your_log_channel_id

# MongoDB
MONGO_DB_URI=your_mongodb_connection_string

# Railway Configuration
RAILWAY_URL=your_bot_railway_app_url

# YouTube API (NEW!)
API_BASE_URL=your_youtube_api_railway_app_url
```

#### Optional Variables
```env
# Spotify Configuration
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret

# String Sessions (for assistant accounts)
STRING_SESSION=your_session_string_1
STRING_SESSION2=your_session_string_2
STRING_SESSION3=your_session_string_3
STRING_SESSION4=your_session_string_4
STRING_SESSION5=your_session_string_5

# Duration Limits
DURATION_LIMIT=99999
SONG_DOWNLOAD_DURATION=99999
SONG_DOWNLOAD_DURATION_LIMIT=99999

# Auto-leave Settings
AUTO_LEAVING_ASSISTANT=True
ASSISTANT_LEAVE_TIME=9000

# Support Links
SUPPORT_CHANNEL=https://t.me/your_channel
SUPPORT_CHAT=https://t.me/your_group
SOURCE_CODE=https://github.com/your_username/your_repo
PRIVACY_LINK=https://your_privacy_policy_url

# File Size Limits
TG_AUDIO_FILESIZE_LIMIT=5242880000
TG_VIDEO_FILESIZE_LIMIT=5242880000

# Playlist Limits
PLAYLIST_FETCH_LIMIT=9999
```

### How to Get Required Values

#### 1. Telegram API Credentials
1. Go to [my.telegram.org](https://my.telegram.org)
2. Log in with your phone number
3. Go to "API development tools"
4. Create a new application
5. Copy `api_id` and `api_hash`

#### 2. Bot Token
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Create a new bot with `/newbot`
3. Copy the bot token

#### 3. Logger ID (LOGGER_ID)
1. Create a Telegram group/channel
2. Add your bot to it
3. Make the bot an admin
4. Send a message in the group
5. Forward that message to [@userinfobot](https://t.me/userinfobot)
6. Copy the chat ID (it will be negative for groups)

#### 4. Railway URLs
1. Deploy your bot on Railway
2. Deploy the YouTube API service on Railway (separate project)
3. Copy both URLs and set them as environment variables

### 🚀 **Deployment Steps (Updated)**

#### **Option 1: Automated Setup (Recommended)**
1. **Run the deployment script:**
   ```bash
   python deploy_to_railway.py
   ```
2. **Follow the automated instructions**

#### **Option 2: Manual Setup**
1. **Deploy YouTube API Service:**
   - Fork/Clone the `youtube_api/` folder to a **separate GitHub repository**
   - Deploy to Railway as a new project
   - Copy the generated URL

2. **Deploy Bot:**
   - Deploy your main bot repository to Railway
   - Set `API_BASE_URL` to your YouTube API URL
   - Set all other environment variables

3. **Test Your Bot:**
   - Send `/start` to your bot
   - Try playing a YouTube video
   - Check logs for any errors

### 🎯 **How It Works**

1. **User sends YouTube link** to your bot
2. **Bot sends request** to your self-hosted YouTube API
3. **API downloads and processes** the video/audio
4. **API returns processed file** to your bot
5. **Bot streams** the music to users
6. **If API fails**, bot automatically falls back to yt-dlp

### 📊 **Features**

- 🎵 **Multi-platform music support**
- 🎧 **High-quality audio streaming**
- 📱 **User-friendly interface**
- 🔒 **Secure and private**
- 🚀 **Fast and reliable**
- 🌐 **Multiple language support**
- 🆕 **Self-hosted YouTube API**
- 🔄 **Automatic fallback system**

### Supported Platforms

- YouTube (via self-hosted API + fallback)
- Spotify
- Apple Music
- SoundCloud
- Resso
- Telegram files

### Commands

- `/play` - Play music
- `/pause` - Pause music
- `/resume` - Resume music
- `/skip` - Skip to next track
- `/stop` - Stop music
- `/queue` - Show queue
- `/help` - Show help

### Support

- **Developer:** [@devforgekush](https://t.me/devforgekush)
- **Support Group:** [Join Here](https://t.me/devforgekush)
- **Source Code:** [GitHub](https://github.com/devforgekush/Alphabot)

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Developed with ❤️ by [@devforgekush](https://t.me/devforgekush)**
