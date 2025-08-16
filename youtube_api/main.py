# ---------------------------------------------------------
# Alphabot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Alphabot project.
# Unauthorized copying, distribution, or use is prohibited.
# Developed by @devforgekush. All rights reserved.
# ---------------------------------------------------------

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
import yt_dlp
import asyncio
import os
import uuid
import aiofiles
import aiohttp
from typing import Optional, Dict, Any
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Alphabot YouTube API",
    description="Free YouTube download API for Alphabot Music Bot",
    version="1.0.0"
)

# Create downloads directory
os.makedirs("downloads", exist_ok=True)
os.makedirs("temp", exist_ok=True)

class VideoRequest(BaseModel):
    url: str
    format: Optional[str] = "bestaudio"  # bestaudio, best, worst
    quality: Optional[str] = "192"  # 192, 128, 64

class VideoInfo(BaseModel):
    url: str
    title: str
    duration: int
    thumbnail: str
    formats: list
    status: str

# Store active downloads
active_downloads: Dict[str, Dict[str, Any]] = {}

@app.get("/")
async def root():
    return {
        "message": "🎵 Alphabot YouTube API is running!",
        "status": "active",
        "developer": "@devforgekush",
        "endpoints": {
            "GET /info/{video_id}": "Get video information",
            "POST /download": "Download video/audio",
            "GET /status/{task_id}": "Check download status",
            "GET /health": "Health check"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Alphabot YouTube API"}

@app.post("/info")
async def get_video_info(request: VideoRequest):
    """Get video information without downloading"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(request.url, download=False)
            
            return {
                "status": "success",
                "video_id": info.get('id'),
                "title": info.get('title'),
                "duration": info.get('duration'),
                "thumbnail": info.get('thumbnail'),
                "formats": [
                    {
                        "format_id": f.get('format_id'),
                        "ext": f.get('ext'),
                        "filesize": f.get('filesize'),
                        "quality": f.get('quality'),
                        "vcodec": f.get('vcodec'),
                        "acodec": f.get('acodec')
                    }
                    for f in info.get('formats', [])
                    if f.get('acodec') != 'none'  # Audio formats only
                ],
                "uploader": info.get('uploader'),
                "view_count": info.get('view_count')
            }
    except Exception as e:
        logger.error(f"Error getting video info: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to get video info: {str(e)}")

@app.post("/download")
async def download_video(request: VideoRequest, background_tasks: BackgroundTasks):
    """Download video/audio file"""
    try:
        # Generate unique task ID
        task_id = str(uuid.uuid4())
        
        # Create task info
        task_info = {
            "id": task_id,
            "url": request.url,
            "format": request.format,
            "status": "starting",
            "progress": 0,
            "file_path": None,
            "error": None
        }
        
        active_downloads[task_id] = task_info
        
        # Start download in background
        background_tasks.add_task(download_task, task_id, request)
        
        return {
            "status": "started",
            "task_id": task_id,
            "message": "Download started. Use /status/{task_id} to check progress."
        }
        
    except Exception as e:
        logger.error(f"Error starting download: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to start download: {str(e)}")

async def download_task(task_id: str, request: VideoRequest):
    """Background download task"""
    try:
        task_info = active_downloads[task_id]
        task_info["status"] = "downloading"
        
        # Configure yt-dlp options
        ydl_opts = {
            'format': f'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio' if request.format == "bestaudio" else request.format,
            'outtmpl': f'downloads/{task_id}.%(ext)s',
            'progress_hooks': [lambda d: progress_hook(task_id, d)],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': request.quality,
            }] if request.format == "bestaudio" else [],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(request.url, download=True)
            
            # Find the downloaded file
            downloaded_file = None
            for file in os.listdir("downloads"):
                if file.startswith(task_id):
                    downloaded_file = file
                    break
            
            if downloaded_file:
                file_path = os.path.join("downloads", downloaded_file)
                task_info["status"] = "completed"
                task_info["file_path"] = file_path
                task_info["progress"] = 100
                task_info["title"] = info.get('title', 'Unknown')
                task_info["duration"] = info.get('duration', 0)
                
                logger.info(f"Download completed for task {task_id}: {file_path}")
            else:
                raise Exception("Downloaded file not found")
                
    except Exception as e:
        logger.error(f"Download error for task {task_id}: {str(e)}")
        task_info = active_downloads[task_id]
        task_info["status"] = "failed"
        task_info["error"] = str(e)

def progress_hook(task_id: str, d: Dict[str, Any]):
    """Update download progress"""
    if task_id in active_downloads:
        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes']:
                progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
                active_downloads[task_id]["progress"] = round(progress, 1)
        elif d['status'] == 'finished':
            active_downloads[task_id]["progress"] = 100

@app.get("/status/{task_id}")
async def get_download_status(task_id: str):
    """Get download status and progress"""
    if task_id not in active_downloads:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_info = active_downloads[task_id]
    
    # Clean up completed/failed tasks after 1 hour
    if task_info["status"] in ["completed", "failed"]:
        # Schedule cleanup
        asyncio.create_task(cleanup_task(task_id))
    
    return task_info

@app.get("/download/{task_id}")
async def get_downloaded_file(task_id: str):
    """Download the completed file"""
    if task_id not in active_downloads:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_info = active_downloads[task_id]
    
    if task_info["status"] != "completed":
        raise HTTPException(status_code=400, detail="Download not completed yet")
    
    if not task_info["file_path"] or not os.path.exists(task_info["file_path"]):
        raise HTTPException(status_code=404, detail="File not found")
    
    filename = os.path.basename(task_info["file_path"])
    return FileResponse(
        task_info["file_path"],
        filename=filename,
        media_type="audio/mpeg"
    )

async def cleanup_task(task_id: str):
    """Clean up completed task after delay"""
    await asyncio.sleep(3600)  # 1 hour
    
    if task_id in active_downloads:
        task_info = active_downloads[task_id]
        
        # Remove file if it exists
        if task_info["file_path"] and os.path.exists(task_info["file_path"]):
            try:
                os.remove(task_info["file_path"])
                logger.info(f"Cleaned up file: {task_info['file_path']}")
            except:
                pass
        
        # Remove task info
        del active_downloads[task_id]
        logger.info(f"Cleaned up task: {task_id}")

@app.get("/stats")
async def get_stats():
    """Get API statistics"""
    return {
        "active_downloads": len(active_downloads),
        "downloads_dir_size": get_dir_size("downloads"),
        "temp_dir_size": get_dir_size("temp"),
        "total_tasks": len(active_downloads)
    }

def get_dir_size(directory: str) -> int:
    """Get directory size in bytes"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
    except:
        pass
    return total_size

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
