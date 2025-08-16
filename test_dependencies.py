#!/usr/bin/env python3
"""
Comprehensive test script to check all dependencies
"""
import sys
import importlib

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        module = importlib.import_module(module_name)
        version = getattr(module, '__version__', 'Unknown')
        print(f"✅ {module_name} - Import successful (version: {version})")
        return True
    except ImportError as e:
        print(f"❌ {module_name} - Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ {module_name} - Unexpected error: {e}")
        return False

def main():
    print("🔍 Testing all dependencies...")
    print("=" * 50)
    
    # Core dependencies
    core_modules = [
        'pyrogram',
        'tgcrypto',
        'motor',
        'aiofiles',
        'aiohttp',
        'requests',
        'uvloop',
        'psutil',
        'PIL',
        'yt_dlp',
        'gtts',
        'pydub',
        'git',
        'heroku3',
        'python-dotenv',
        'youtubesearchpython',
        'bs4',
        'spotipy'
    ]
    
    # Voice dependencies
    voice_modules = [
        'pytgcalls',
        'tgcalls'
    ]
    
    # Additional dependencies
    additional_modules = [
        'numpy',
        'pandas',
        'speedtest_cli',
        'SpeechRecognition',
        'telegraph',
        'telethon'
    ]
    
    failed_imports = []
    
    print("📦 Testing core dependencies...")
    for module in core_modules:
        if not test_import(module):
            failed_imports.append(module)
    
    print("\n🎵 Testing voice dependencies...")
    for module in voice_modules:
        if not test_import(module):
            failed_imports.append(module)
            print(f"   ⚠️ {module} is optional - voice features will be disabled")
    
    print("\n🔧 Testing additional dependencies...")
    for module in additional_modules:
        if not test_import(module):
            failed_imports.append(module)
            print(f"   ⚠️ {module} is optional - some features may be limited")
    
    print("=" * 50)
    print("📊 Test Results:")
    
    if not failed_imports:
        print("🎉 All dependencies imported successfully!")
        return True
    else:
        print(f"❌ Failed imports: {', '.join(failed_imports)}")
        
        # Check if critical dependencies failed
        critical_failed = [m for m in failed_imports if m in core_modules]
        if critical_failed:
            print(f"💥 Critical failures: {', '.join(critical_failed)}")
            return False
        else:
            print("⚠️ Only optional dependencies failed - bot should still work")
            return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
