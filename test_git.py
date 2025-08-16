#!/usr/bin/env python3
"""
Test script to verify gitpython import
"""
import sys

def test_git_import():
    """Test if gitpython can be imported"""
    try:
        from git import Repo
        print("✅ gitpython import successful")
        print(f"   GitPython version: {Repo.__version__ if hasattr(Repo, '__version__') else 'Unknown'}")
        return True
    except ImportError as e:
        print(f"❌ gitpython import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error importing gitpython: {e}")
        return False

def test_git_command():
    """Test if git command is available"""
    import subprocess
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Git command available: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Git command failed: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ Git command not found in PATH")
        return False
    except Exception as e:
        print(f"❌ Error testing git command: {e}")
        return False

def main():
    print("🔍 Testing gitpython and git command...")
    print("=" * 50)
    
    git_import_ok = test_git_import()
    git_command_ok = test_git_command()
    
    print("=" * 50)
    print("📊 Test Results:")
    print(f"GitPython import: {'✅ PASS' if git_import_ok else '❌ FAIL'}")
    print(f"Git command: {'✅ PASS' if git_command_ok else '❌ FAIL'}")
    
    if git_import_ok and git_command_ok:
        print("\n🎉 All git tests passed!")
        return True
    else:
        print("\n💥 Some git tests failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
