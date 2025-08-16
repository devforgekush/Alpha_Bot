# ---------------------------------------------------------
# Alphabot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Alphabot project.
# Unauthorized copying, distribution, or use is prohibited.
# Developed by @devforgekush. All rights reserved.
# ---------------------------------------------------------

import os
import shutil
import subprocess
import sys

def print_banner():
    print("🎵" * 50)
    print("🚀 ALPHABOT RAILWAY DEPLOYMENT SCRIPT")
    print("🎵" * 50)
    print()

def check_requirements():
    """Check if required tools are installed"""
    print("🔍 Checking requirements...")
    
    # Check if git is installed
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        print("✅ Git is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git is not installed. Please install Git first.")
        return False
    
    # Check if Python is installed
    try:
        subprocess.run([sys.executable, "--version"], check=True, capture_output=True)
        print("✅ Python is installed")
    except:
        print("❌ Python is not installed. Please install Python first.")
        return False
    
    return True

def create_api_repo():
    """Create a separate repository for the YouTube API"""
    print("\n📁 Creating YouTube API repository...")
    
    api_dir = "youtube_api"
    if not os.path.exists(api_dir):
        print("❌ YouTube API directory not found!")
        return False
    
    # Create a new git repository for the API
    try:
        os.chdir(api_dir)
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit: Alphabot YouTube API"], check=True, capture_output=True)
        print("✅ YouTube API repository created")
        os.chdir("..")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating API repository: {e}")
        os.chdir("..")
        return False

def create_bot_repo():
    """Create a separate repository for the bot"""
    print("\n🤖 Creating Bot repository...")
    
    # Create a new git repository for the bot (excluding API)
    try:
        # Remove API directory from bot repo
        if os.path.exists("youtube_api"):
            shutil.rmtree("youtube_api")
        
        # Remove deployment script
        if os.path.exists("deploy_to_railway.py"):
            os.remove("deploy_to_railway.py")
        
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Update: Alphabot with API integration"], check=True, capture_output=True)
        print("✅ Bot repository updated")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error updating bot repository: {e}")
        return False

def print_deployment_steps():
    """Print step-by-step deployment instructions"""
    print("\n" + "="*60)
    print("🚀 DEPLOYMENT INSTRUCTIONS")
    print("="*60)
    
    print("\n📋 STEP 1: Deploy YouTube API Service")
    print("1. Go to https://railway.app")
    print("2. Sign in with GitHub")
    print("3. Click 'New Project' → 'Deploy from GitHub repo'")
    print("4. Select your YouTube API repository")
    print("5. Railway will auto-deploy")
    print("6. Copy the generated URL (e.g., https://your-api.railway.app)")
    
    print("\n📋 STEP 2: Deploy Bot")
    print("1. In Railway, create another 'New Project'")
    print("2. Select your Bot repository")
    print("3. Add environment variables:")
    print("   - API_ID=your_api_id")
    print("   - API_HASH=your_api_hash")
    print("   - BOT_TOKEN=your_bot_token")
    print("   - OWNER_ID=your_user_id")
    print("   - LOGGER_ID=your_log_channel_id")
    print("   - MONGO_DB_URI=your_mongodb_uri")
    print("   - API_BASE_URL=https://your-api.railway.app")
    print("   - RAILWAY_URL=https://your-bot.railway.app")
    
    print("\n📋 STEP 3: Test Your Bot")
    print("1. Send /start to your bot")
    print("2. Try playing a YouTube video")
    print("3. Check logs for any errors")
    
    print("\n💡 TIPS:")
    print("- Both services run on Railway for FREE")
    print("- API service handles YouTube downloads")
    print("- Bot service handles Telegram interactions")
    print("- If API fails, bot falls back to yt-dlp")

def main():
    print_banner()
    
    if not check_requirements():
        print("\n❌ Requirements not met. Please install missing tools.")
        return
    
    print("\n🎯 This script will help you deploy Alphabot to Railway!")
    print("You'll need to deploy TWO services:")
    print("1. 🎵 YouTube API Service (for downloads)")
    print("2. 🤖 Bot Service (for Telegram)")
    
    input("\nPress Enter to continue...")
    
    # Create repositories
    if not create_api_repo():
        print("❌ Failed to create API repository")
        return
    
    if not create_bot_repo():
        print("❌ Failed to update bot repository")
        return
    
    print_deployment_steps()
    
    print("\n🎉 Setup complete! Follow the steps above to deploy.")
    print("\n📞 Need help? Contact @devforgekush on Telegram")

if __name__ == "__main__":
    main()
