# 🎵 Alphabot YouTube API Service

A **100% FREE** self-hosted YouTube download API service for your Alphabot Music Bot.

## 🚀 **Deploy to Railway (FREE)**

### **Step 1: Deploy API Service**
1. **Fork/Clone** this `youtube_api` folder to a **separate GitHub repository**
2. **Deploy to Railway:**
   - Connect your GitHub repository
   - Railway will auto-detect it's a Python app
   - Deploy automatically

### **Step 2: Get Your API URL**
- Railway will give you a URL like: `https://your-app-name.railway.app`
- **Copy this URL** - you'll need it for your bot

### **Step 3: Update Your Bot**
- Set `API_BASE_URL=https://your-app-name.railway.app` in your bot's environment variables

## 🔧 **API Endpoints**

### **Health Check**
```
GET /health
```

### **Get Video Info**
```
POST /info
{
    "url": "https://youtube.com/watch?v=...",
    "format": "bestaudio"
}
```

### **Download Video**
```
POST /download
{
    "url": "https://youtube.com/watch?v=...",
    "format": "bestaudio",
    "quality": "192"
}
```

### **Check Download Status**
```
GET /status/{task_id}
```

### **Download File**
```
GET /download/{task_id}
```

## 📊 **Features**

- ✅ **100% FREE** forever
- ✅ **No rate limits**
- ✅ **Background downloads**
- ✅ **Progress tracking**
- ✅ **Auto-cleanup**
- ✅ **Multiple formats**
- ✅ **Quality control**

## 🎯 **Supported Formats**

- **Audio:** MP3, M4A, OGG
- **Video:** MP4, WebM, AVI
- **Quality:** 64k, 128k, 192k, 320k

## 🔒 **Security**

- **No authentication required** (for simplicity)
- **Rate limiting** built-in
- **File cleanup** after 1 hour
- **Error handling** for all requests

## 💡 **Usage Example**

```python
import requests

# Get video info
response = requests.post("https://your-api.railway.app/info", json={
    "url": "https://youtube.com/watch?v=dQw4w9WgXcQ"
})

# Start download
response = requests.post("https://your-api.railway.app/download", json={
    "url": "https://youtube.com/watch?v=dQw4w9WgXcQ",
    "format": "bestaudio",
    "quality": "192"
})

# Check status
task_id = response.json()["task_id"]
status = requests.get(f"https://your-api.railway.app/status/{task_id}")
```

## 🆘 **Need Help?**

- **Developer:** [@devforgekush](https://t.me/devforgekush)
- **Support:** [Join Here](https://t.me/devforgekush)

---

**Developed with ❤️ by [@devforgekush](https://t.me/devforgekush)**
