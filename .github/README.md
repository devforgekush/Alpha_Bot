# Railway Deployment Guide for Audify Music Bot

## 🚀 Quick Setup

### 1. Environment Variables Required

Add these environment variables in your Railway project dashboard:

#### **Essential Variables:**
```
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
BOT_TOKEN=your_bot_token
LOGGER_ID=-1001234567890
MONGO_DB_URI=your_mongodb_connection_string
OWNER_ID=your_telegram_user_id
STRING_SESSION=your_pyrogram_session_string
```

#### **Optional Variables:**
```
RAILWAY_URL=https://your-app-name-production.up.railway.app
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
API_KEY=your_music_api_key
BOT_USERNAME=your_bot_username
BOT_NAME=your_bot_name
```

### 2. LOGGER_ID Configuration

#### **How to Get LOGGER_ID:**
1. Add @userinfobot to your log group/channel
2. Send any message
3. Copy the chat ID (negative number like `-1001234567890`)

#### **Bot Permissions Required:**
- **Administrator** role in the log group/channel
- **Send Messages** permission
- **Read Messages** permission

### 3. RAILWAY_URL for Pinger

#### **Purpose:**
- Keeps your bot alive on Railway
- Prevents sleep mode after 15 minutes of inactivity
- Sends HTTP requests every 12 minutes

#### **How to Set:**
1. Deploy your bot first
2. Copy the public URL from Railway dashboard
3. Add as `RAILWAY_URL` environment variable
4. Redeploy to activate pinger

### 4. Deployment Steps

1. **Connect Repository:**
   - Link your GitHub repo to Railway
   - Railway will auto-detect Python project

2. **Set Environment Variables:**
   - Add all required variables
   - Ensure `LOGGER_ID` is correct

3. **Deploy:**
   - Railway will use `Procfile` and `start` script
   - Bot will start automatically

4. **Monitor Logs:**
   - Check Railway logs for any errors
   - Verify bot startup messages

### 5. Troubleshooting

#### **Startup Log Error:**
```
❌ Failed to send startup log.
➡️ Ensure the bot is added to the specified log group or channel.
```

**Solutions:**
- Verify `LOGGER_ID` is correct
- Ensure bot is added to the group/channel
- Check bot has admin permissions
- Verify group/channel is not deleted

#### **Pinger Issues:**
- Set `RAILWAY_URL` correctly
- Check Railway logs for pinger messages
- Ensure app URL is accessible

#### **Import Errors:**
- All dependencies are in `requirements.txt`
- Railway will install them automatically
- Check logs for specific import failures

### 6. Monitoring

#### **Railway Dashboard:**
- Monitor app status
- Check resource usage
- View deployment logs

#### **Bot Logs:**
- Check Telegram log group
- Monitor Railway console logs
- Verify pinger is working

### 7. Performance Tips

- **Keep LOGGER_ID configured** for monitoring
- **Use dedicated log group** (not main support group)
- **Monitor Railway logs** regularly
- **Set up external monitoring** as backup

## 🔧 Support

If you encounter issues:
1. Check Railway logs first
2. Verify all environment variables
3. Ensure bot permissions are correct
4. Check Telegram group/channel status


## � Credits

Developed and maintained by [@devforgekush](https://t.me/devforgekush)

Special thanks to all contributors and the Telegram music bot community.

If you use this guide or bot, please star the repo and give credit!

---

- Bot will continue running even if logging fails
- Pinger only works when `RAILWAY_URL` is set
- All errors are logged for debugging
- Bot gracefully handles missing configurations
