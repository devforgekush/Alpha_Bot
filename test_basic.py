#!/usr/bin/env python3
"""
Test script to check if bot can run with basic requirements
"""
import sys
import importlib

def test_imports():
    """Test if essential modules can be imported"""
    essential_modules = [
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
        'pydub'
    ]
    
    failed_imports = []
    
    for module in essential_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module} - Import successful")
        except ImportError as e:
            print(f"❌ {module} - Import failed: {e}")
            failed_imports.append(module)
    
    return failed_imports

def test_pytgcalls():
    """Test pytgcalls import specifically"""
    try:
        import pytgcalls
        print(f"✅ pytgcalls - Import successful (version: {pytgcalls.__version__})")
        return True
    except ImportError as e:
        print(f"❌ pytgcalls - Import failed: {e}")
        return False

def main():
    print("🔍 Testing basic requirements...")
    print("=" * 50)
    
    # Test basic imports
    failed_basic = test_imports()
    
    print("\n" + "=" * 50)
    print("🔍 Testing pytgcalls...")
    
    # Test pytgcalls
    pytgcalls_works = test_pytgcalls()
    
    print("\n" + "=" * 50)
    print("📊 Summary:")
    
    if not failed_basic:
        print("✅ All basic imports successful")
    else:
        print(f"❌ Failed basic imports: {', '.join(failed_basic)}")
    
    if pytgcalls_works:
        print("✅ pytgcalls import successful")
    else:
        print("❌ pytgcalls import failed")
        print("💡 Bot may work without pytgcalls (voice features disabled)")
    
    print("\n🎵 Test completed!")

if __name__ == "__main__":
    main()
