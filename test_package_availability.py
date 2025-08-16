#!/usr/bin/env python3
"""
Test script to check package availability and versions
"""
import subprocess
import sys

def check_package_availability(package_name):
    """Check if a package is available and what versions exist"""
    try:
        # Try to get package info
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'index', 'versions', package_name
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ {package_name} - Available")
            # Extract version info if available
            lines = result.stdout.split('\n')
            for line in lines:
                if 'LATEST:' in line or 'versions:' in line:
                    print(f"   {line.strip()}")
        else:
            print(f"❌ {package_name} - Not available")
            print(f"   Error: {result.stderr.strip()}")
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {package_name} - Timeout checking availability")
    except Exception as e:
        print(f"❌ {package_name} - Error: {e}")

def main():
    print("🔍 Checking package availability...")
    print("=" * 50)
    
    packages_to_check = [
        "youtube-search-python",
        "youtubesearchpython", 
        "pytgcalls",
        "tgcalls",
        "pyrogram",
        "tgcrypto",
        "motor",
        "aiofiles",
        "aiohttp",
        "requests",
        "uvloop",
        "psutil",
        "Pillow",
        "yt-dlp",
        "gtts",
        "pydub",
        "gitpython",
        "heroku3",
        "beautifulsoup4",
        "spotipy"
    ]
    
    for package in packages_to_check:
        check_package_availability(package)
        print("-" * 30)

if __name__ == "__main__":
    main()
