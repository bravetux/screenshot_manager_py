"""
Build script for Screenshot Manager application
Creates a standalone executable using PyInstaller
"""

import os
import sys
import subprocess
import shutil

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
        return True
    except ImportError:
        print("✗ PyInstaller is not installed")
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed successfully")
        return True

def create_icon():
    """Create an icon file for the executable"""
    try:
        from PIL import Image, ImageDraw
        
        # Create a simple camera icon
        img = Image.new('RGB', (256, 256), color=(30, 30, 46))
        draw = ImageDraw.Draw(img)
        
        # Scale up the camera design
        # Camera body
        draw.rectangle([40, 80, 216, 200], fill=(137, 180, 250), outline=(205, 214, 244), width=3)
        
        # Camera lens
        draw.ellipse([96, 112, 160, 176], fill=(24, 24, 37), outline=(205, 214, 244), width=3)
        
        # Inner lens
        draw.ellipse([110, 126, 146, 162], fill=(137, 180, 250), outline=(205, 214, 244), width=2)
        
        # Camera flash
        draw.rectangle([104, 56, 128, 80], fill=(246, 194, 135))
        
        # Viewfinder
        draw.rectangle([168, 96, 192, 112], fill=(24, 24, 37))
        
        # Save as ICO
        img.save('screenshot_icon.ico', format='ICO')
        print("✓ Icon file created: screenshot_icon.ico")
        return True
    except Exception as e:
        print(f"⚠ Could not create icon: {str(e)}")
        return False

def clean_build_folders():
    """Clean up previous build folders"""
    folders_to_clean = ['build', 'dist', '__pycache__']
    for folder in folders_to_clean:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"✓ Cleaned {folder} folder")

def build_executable():
    """Build the executable using PyInstaller"""
    print("\n" + "="*60)
    print("Building Screenshot Manager Executable")
    print("="*60 + "\n")
    
    # Check and install PyInstaller if needed
    if not check_pyinstaller():
        print("✗ Failed to install PyInstaller")
        return False
    
    # Create icon
    icon_created = create_icon()
    
    # Clean previous builds
    clean_build_folders()
    
    # PyInstaller command
    app_name = "ScreenshotManager"
    script_name = "screenshot_app.py"
    
    # Build command arguments
    pyinstaller_args = [
        'pyinstaller',
        '--onefile',  # Create a single executable
        '--windowed',  # Don't show console window
        '--name', app_name,
        '--clean',  # Clean PyInstaller cache
        '--noconfirm',  # Replace output directory without asking
    ]
    
    # Add icon if it was created
    if icon_created and os.path.exists('screenshot_icon.ico'):
        pyinstaller_args.extend(['--icon', 'screenshot_icon.ico'])
    
    # Add hidden imports for libraries that might not be detected
    hidden_imports = [
        'PIL._tkinter_finder',
        'pystray._win32',
        'keyboard',
    ]
    
    for imp in hidden_imports:
        pyinstaller_args.extend(['--hidden-import', imp])
    
    # Add the script to build
    pyinstaller_args.append(script_name)
    
    print("\nBuilding executable...")
    print(f"Command: {' '.join(pyinstaller_args)}\n")
    
    try:
        # Run PyInstaller
        result = subprocess.run(pyinstaller_args, check=True, capture_output=True, text=True)
        print(result.stdout)
        
        print("\n" + "="*60)
        print("✓ Build completed successfully!")
        print("="*60)
        print(f"\nExecutable location: dist\\{app_name}.exe")
        print(f"Size: {os.path.getsize(f'dist\\{app_name}.exe') / (1024*1024):.2f} MB")
        print("\nYou can now distribute the executable to any Windows machine.")
        print("No Python installation required on the target machine!")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print("\n" + "="*60)
        print("✗ Build failed!")
        print("="*60)
        print(f"\nError: {e}")
        if e.stderr:
            print(f"Details: {e.stderr}")
        return False

def create_readme_for_exe():
    """Create a README file for the executable distribution"""
    readme_content = """# Screenshot Manager - Portable Executable

## About
Screenshot Manager is a portable Windows application for capturing and managing screenshots.

## Features
- Capture screenshots with Ctrl+PrintScreen hotkey
- Automatic saving to C:\\Screenshot folder
- Preview and manage captured screenshots
- Rename and delete screenshots
- System tray integration
- Modern dark theme UI

## How to Use
1. Run ScreenshotManager.exe (No installation required!)
2. Press Ctrl+PrintScreen to capture a screenshot
3. View, rename, or delete screenshots from the interface
4. Minimize to system tray by closing the window
5. Right-click the tray icon to restore or exit

## Requirements
- Windows 7 or later
- No Python installation needed
- Administrator privileges recommended (for global hotkey)

## Important Notes
- Screenshots are saved to: C:\\Screenshot
- Filename format: ss_ddmmyyyy_hhmmss.png
- Run as Administrator for best hotkey functionality

## Troubleshooting
- If hotkey doesn't work: Run as Administrator
- If icon doesn't appear: Check system tray settings
- Antivirus warning: This is normal for PyInstaller executables

## Developer
Designed & Developed by Bravetux aka B.Vignesh Kumar
Email: ic19939@gmail.com

## Version
1.0 - Initial Release
"""
    
    try:
        with open('dist/README.txt', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("\n✓ README.txt created in dist folder")
    except Exception as e:
        print(f"\n⚠ Could not create README: {str(e)}")

def main():
    """Main build process"""
    # Check if we're in the correct directory
    if not os.path.exists('screenshot_app.py'):
        print("✗ Error: screenshot_app.py not found!")
        print("Please run this script from the project directory.")
        sys.exit(1)
    
    # Build the executable
    if build_executable():
        # Create README for distribution
        create_readme_for_exe()
        
        print("\n" + "="*60)
        print("Build Process Complete!")
        print("="*60)
        print("\nNext steps:")
        print("1. Test the executable: dist\\ScreenshotManager.exe")
        print("2. Distribute the dist folder to other Windows machines")
        print("3. Optionally create a ZIP file for easy distribution")
        
        # Ask if user wants to create a ZIP file
        try:
            response = input("\nCreate ZIP file for distribution? (y/n): ").lower()
            if response == 'y':
                create_distribution_zip()
        except:
            pass
    else:
        print("\n✗ Build failed. Please check the errors above.")
        sys.exit(1)

def create_distribution_zip():
    """Create a ZIP file for easy distribution"""
    try:
        import zipfile
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d")
        zip_filename = f"ScreenshotManager_v1.0_{timestamp}.zip"
        
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add executable
            zipf.write('dist/ScreenshotManager.exe', 'ScreenshotManager.exe')
            
            # Add README if it exists
            if os.path.exists('dist/README.txt'):
                zipf.write('dist/README.txt', 'README.txt')
        
        print(f"\n✓ Distribution ZIP created: {zip_filename}")
        print(f"Size: {os.path.getsize(zip_filename) / (1024*1024):.2f} MB")
        
    except Exception as e:
        print(f"\n⚠ Could not create ZIP file: {str(e)}")

if __name__ == "__main__":
    main()
