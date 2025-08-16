#!/usr/bin/env python3
"""
Test script to check available package versions
"""
import subprocess
import sys

def check_package_version(package_name):
    """Check if a package version is available"""
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'index', 'versions', package_name
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ {package_name} - Available versions:")
            print(result.stdout)
        else:
            print(f"❌ {package_name} - Error checking versions:")
            print(result.stderr)
    except Exception as e:
        print(f"❌ {package_name} - Exception: {e}")

def main():
    print("🔍 Checking available package versions...")
    print("=" * 50)
    
    packages_to_check = [
        "pytgcalls",
        "tgcalls",
        "pyrogram",
        "tgcrypto"
    ]
    
    for package in packages_to_check:
        check_package_version(package)
        print("-" * 30)

if __name__ == "__main__":
    main()
