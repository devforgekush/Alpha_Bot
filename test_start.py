#!/usr/bin/env python3
"""
Test script to verify the start process
"""
import sys
import os

def test_imports():
    """Test all necessary imports"""
    print("🔍 Testing imports...")
    
    # Test config import
    try:
        import config
        print("✅ config imported successfully")
    except ImportError as e:
        print(f"❌ config import failed: {e}")
        return False
    
    # Test Audify imports
    try:
        from Audify import LOGGER, app, userbot
        print("✅ Audify core modules imported successfully")
    except ImportError as e:
        print(f"❌ Audify imports failed: {e}")
        return False
    
    # Test call module
    try:
        from Audify.core.call import Audify
        print("✅ Audify call module imported successfully")
    except ImportError as e:
        print(f"❌ Audify call import failed: {e}")
        return False
    
    return True

def test_environment():
    """Test environment variables"""
    print("\n🔍 Testing environment variables...")
    required_vars = ['API_ID', 'API_HASH', 'BOT_TOKEN']
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var} = {value[:10]}..." if len(value) > 10 else f"✅ {var} = {value}")
        else:
            print(f"❌ {var} not set")
            missing_vars.append(var)
    
    return len(missing_vars) == 0

def main():
    print("🚀 Starting comprehensive test...")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test environment
    env_ok = test_environment()
    
    print("=" * 50)
    print("📊 Test Results:")
    print(f"Imports: {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"Environment: {'✅ PASS' if env_ok else '❌ FAIL'}")
    
    if imports_ok and env_ok:
        print("\n🎉 All tests passed! Bot should start successfully.")
        return True
    else:
        print("\n💥 Some tests failed. Check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
