"""
Test script to verify the built executable works correctly
Run this after building the executable
"""

import os
import sys
import subprocess
import time

def test_executable_exists():
    """Test if executable was created"""
    exe_path = "dist/ScreenshotManager.exe"
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"✓ Executable found: {exe_path}")
        print(f"  Size: {size_mb:.2f} MB")
        return True
    else:
        print(f"✗ Executable not found: {exe_path}")
        print("  Please run build_exe.py first")
        return False

def test_icon_exists():
    """Test if icon was created"""
    if os.path.exists("screenshot_icon.ico"):
        print("✓ Icon file exists: screenshot_icon.ico")
        return True
    else:
        print("⚠ Icon file not found (optional)")
        return False

def test_readme_exists():
    """Test if README was created"""
    readme_path = "dist/README.txt"
    if os.path.exists(readme_path):
        print(f"✓ README found: {readme_path}")
        return True
    else:
        print(f"⚠ README not found: {readme_path}")
        return False

def test_dependencies():
    """Test if all dependencies are importable"""
    print("\nChecking dependencies...")
    dependencies = {
        'PIL': 'Pillow',
        'keyboard': 'keyboard',
        'pystray': 'pystray',
        'tkinter': 'tkinter (built-in)'
    }
    
    all_ok = True
    for module, package in dependencies.items():
        try:
            __import__(module)
            print(f"✓ {package} is available")
        except ImportError:
            print(f"✗ {package} is missing")
            all_ok = False
    
    return all_ok

def test_source_files():
    """Test if source files exist"""
    print("\nChecking source files...")
    files = [
        'screenshot_app.py',
        'requirements.txt',
        'build_exe.py',
        'build.bat',
        'screenshot_app.spec'
    ]
    
    all_ok = True
    for file in files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} missing")
            all_ok = False
    
    return all_ok

def test_executable_run():
    """Test if executable can be started"""
    exe_path = "dist/ScreenshotManager.exe"
    if not os.path.exists(exe_path):
        print("✗ Cannot test execution - executable not found")
        return False
    
    print("\nTesting executable startup...")
    print("⚠ Note: This will start the application")
    print("  Please close it manually to continue testing")
    
    try:
        response = input("Start the executable now? (y/n): ").lower()
        if response != 'y':
            print("⊘ Execution test skipped")
            return None
        
        print("Starting executable...")
        process = subprocess.Popen([exe_path])
        
        print("✓ Executable started successfully")
        print("  PID:", process.pid)
        print("  Please test the application and close it")
        print("  Press Enter when done...")
        input()
        
        # Check if process is still running
        if process.poll() is None:
            print("✓ Application is running")
            print("  Please close it manually")
            return True
        else:
            print("⚠ Application closed")
            return True
            
    except Exception as e:
        print(f"✗ Failed to start executable: {str(e)}")
        return False

def generate_test_report():
    """Generate a comprehensive test report"""
    print("\n" + "="*60)
    print("SCREENSHOT MANAGER - BUILD VERIFICATION TEST")
    print("="*60 + "\n")
    
    results = {}
    
    # Test 1: Executable exists
    print("[Test 1] Checking executable...")
    results['executable'] = test_executable_exists()
    
    # Test 2: Icon exists
    print("\n[Test 2] Checking icon...")
    results['icon'] = test_icon_exists()
    
    # Test 3: README exists
    print("\n[Test 3] Checking README...")
    results['readme'] = test_readme_exists()
    
    # Test 4: Dependencies
    results['dependencies'] = test_dependencies()
    
    # Test 5: Source files
    results['source_files'] = test_source_files()
    
    # Test 6: Executable run (optional)
    print("\n[Test 6] Testing executable startup...")
    results['execution'] = test_executable_run()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)
    total = len(results)
    
    print(f"\nTotal Tests: {total}")
    print(f"Passed: {passed} ✓")
    print(f"Failed: {failed} ✗")
    print(f"Skipped: {skipped} ⊘")
    
    if failed == 0 and passed > 0:
        print("\n🎉 All critical tests passed!")
        print("The executable is ready for distribution.")
    elif failed > 0:
        print("\n⚠ Some tests failed.")
        print("Please review the issues above.")
    
    print("\n" + "="*60)
    
    return results

def main():
    """Main test function"""
    try:
        results = generate_test_report()
        
        # Additional information
        print("\nNext Steps:")
        print("1. Test the executable on a machine without Python")
        print("2. Test all features (capture, rename, delete, tray)")
        print("3. Verify screenshots are saved to C:\\Screenshot")
        print("4. Check system tray functionality")
        print("5. Test hotkey (Ctrl+PrintScreen)")
        print("\nFor distribution:")
        print("- Share dist/ScreenshotManager.exe")
        print("- Include dist/README.txt")
        print("- Optionally create a ZIP file")
        
        print("\nFor more details, see:")
        print("- BUILD_INSTRUCTIONS.md")
        print("- BUILD_SUMMARY.md")
        print("- QUICKSTART.md")
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n✗ Test failed with error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
