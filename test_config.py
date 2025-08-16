#!/usr/bin/env python3
"""
Test script to check if config.py can be imported
"""
import sys
import os

def test_config_import():
    """Test if config.py can be imported"""
    print("🔍 Testing config.py import...")
    print(f"📁 Current working directory: {os.getcwd()}")
    print(f"🐍 Python path: {sys.path}")
    
    # Check if config.py exists
    config_files = []
    for path in sys.path:
        config_path = os.path.join(path, "config.py")
        if os.path.exists(config_path):
            config_files.append(config_path)
            print(f"✅ Found config.py at: {config_path}")
    
    if not config_files:
        print("❌ config.py not found in any Python path!")
        return False
    
    # Try to import config
    try:
        import config
        print("✅ Successfully imported config module")
        print(f"📋 Config module location: {config.__file__}")
        return True
    except ImportError as e:
        print(f"❌ Failed to import config: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error importing config: {e}")
        return False

def test_environment():
    """Test environment variables"""
    print("\n🔍 Testing environment variables...")
    required_vars = ['API_ID', 'API_HASH', 'BOT_TOKEN']
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var} = {value[:10]}..." if len(value) > 10 else f"✅ {var} = {value}")
        else:
            print(f"❌ {var} not set")

if __name__ == "__main__":
    print("🚀 Starting config test...")
    print("=" * 50)
    
    success = test_config_import()
    test_environment()
    
    print("=" * 50)
    if success:
        print("✅ Config test passed!")
    else:
        print("❌ Config test failed!")
        sys.exit(1)
