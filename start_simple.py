#!/usr/bin/env python3
"""
Simple start script for Railway deployment
"""
import sys
import os

# Set Python path
sys.path.insert(0, '/app')

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

# Now import and start the bot
try:
    from Audify.__main__ import init
    import asyncio
    
    print("🚀 Starting Audify Music Bot...")
    asyncio.get_event_loop().run_until_complete(init())
except Exception as e:
    print(f"❌ Failed to start bot: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
