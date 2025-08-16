#!/usr/bin/env python3
"""
Simple health check script for Railway deployment
"""
import os
import sys
import time
import requests
from threading import Thread

def health_check():
    """Simple health check function"""
    try:
        # Check if required environment variables are set
        required_vars = ['API_ID', 'API_HASH', 'BOT_TOKEN']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
            return False
            
        print("✅ Environment variables check passed")
        return True
        
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def ping_railway():
    """Ping Railway URL if configured"""
    railway_url = os.getenv('RAILWAY_URL')
    if not railway_url:
        print("ℹ️ RAILWAY_URL not configured, skipping ping")
        return
        
    def ping_loop():
        while True:
            try:
                response = requests.get(railway_url, timeout=10)
                if response.status_code == 200:
                    print("✅ Railway ping successful")
                else:
                    print(f"⚠️ Railway ping returned status {response.status_code}")
            except Exception as e:
                print(f"❌ Railway ping failed: {e}")
            time.sleep(300)  # Ping every 5 minutes
    
    Thread(target=ping_loop, daemon=True).start()

if __name__ == "__main__":
    print("🔍 Running health check...")
    if health_check():
        print("✅ Health check passed")
        ping_railway()
        sys.exit(0)
    else:
        print("❌ Health check failed")
        sys.exit(1)
