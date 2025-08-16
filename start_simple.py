#!/usr/bin/env python3
"""
Simple start script for Railway deployment
"""
import sys
import os

# Set Python path
sys.path.insert(0, '/app')

# Ensure UTF-8 console output on Windows so logger emoji characters don't raise
# UnicodeEncodeError when printing to the default code page.
import os
os.environ.setdefault("PYTHONUTF8", "1")
try:
    # Reconfigure stdout/stderr to utf-8 when supported (Python 3.7+)
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    # If reconfigure isn't available, fall back to setting PYTHONIOENCODING
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")

# Try to import config from different locations
try:
    import config
    print("✅ Imported config from root directory")
except ImportError:
    try:
        from Audify import config
        print("✅ Imported config from Audify package")
    except ImportError:
        print("❌ Failed to import config from both locations")
        print("📁 Current directory:", os.getcwd())
        print("📁 Files in current directory:", os.listdir('.'))
        print("📁 Files in /app:", os.listdir('/app') if os.path.exists('/app') else "Cannot access /app")
        sys.exit(1)

# Now import and start the bot with a FloodWait-aware retry loop
# Ensure ffmpeg binary is available and set FFMPEG_BINARY so pytgcalls/ffmpeg
# based operations use the correct executable, especially on Railway where a
# system ffmpeg may not be present. imageio-ffmpeg provides a static binary.
try:
    import imageio_ffmpeg as _iioff
    ffpath = _iioff.get_ffmpeg_exe()
    if ffpath:
        os.environ.setdefault("FFMPEG_BINARY", ffpath)
        print(f"✅ FFMPEG_BINARY set to: {ffpath}")
except Exception as e:
    # Non-fatal: continue and let runtime errors surface if ffmpeg is actually missing
    print("⚠️ Could not configure imageio-ffmpeg (ffmpeg binary may be missing):", e)

from Audify.__main__ import init
import asyncio
import re
import time

print("🚀 Starting Audify Music Bot...")
max_retries = 5
attempt = 0
while True:
    try:
        asyncio.get_event_loop().run_until_complete(init())
        break
    except Exception as e:
        # Detect Telegram FloodWait (pyrogram raises a FloodWait error containing a required wait time)
        msg = str(e)
        if "FloodWait" in e.__class__.__name__ or "FLOOD_WAIT" in msg or "A wait of" in msg:
            # Try to extract the number of seconds from the message
            m = re.search(r"(\d+)\s*seconds", msg)
            if not m:
                m = re.search(r"(\d+)", msg)
            wait_seconds = int(m.group(1)) if m else 60
            # Add a small buffer
            wait_seconds = wait_seconds + 5
            attempt += 1
            print(f"⚠️ Telegram FloodWait detected — sleeping {wait_seconds}s (attempt {attempt}/{max_retries})...")
            time.sleep(wait_seconds)
            if attempt >= max_retries:
                print("❌ Exceeded max retry attempts. Exiting.")
                import traceback
                traceback.print_exc()
                sys.exit(1)
            # retry loop
            continue
        # Non-Flood error — print and exit
        print(f"❌ Failed to start bot: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
