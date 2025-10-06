# Screenshot Manager Application

A Python-based screenshot manager with Tkinter GUI that captures screenshots on PrintScreen key press.

## Features

- **Global Hotkey**: Press Ctrl+PrintScreen to capture the entire screen
- **Automatic Storage**: Screenshots saved to `C:\Screenshot` folder
- **Filename Format**: `ss_ddmmyyyy_hhmmss.png` (e.g., ss_04102025_143025.png)
- **File Management**: 
  - View list of all screenshots
  - Preview screenshots in the application
  - Rename screenshots
  - Delete screenshots
  - Open folder in File Explorer
- **System Tray Integration**: 
  - Minimize to system tray
  - Restore from system tray
  - Exit from system tray menu

## Installation

1. Install Python 3.8 or higher

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running from Source

1. Run the application:
```bash
python screenshot_app.py
```

### Running Portable Executable

1. Build the executable (see Building section below)
2. Run `ScreenshotManager.exe` from the `dist` folder
3. No Python installation required!

### Using the Application

1. Press **Ctrl+PrintScreen** key combination anywhere to capture a screenshot

3. The screenshot will be automatically saved to `C:\Screenshot` folder

4. Use the GUI to:
   - View all screenshots in the list
   - Select a screenshot to preview it
   - Rename selected screenshots
   - Delete unwanted screenshots
   - Open the screenshot folder

5. Close or minimize the window to send the app to system tray

6. Right-click the system tray icon to:
   - Restore the application
   - Exit the application

## Requirements

- Windows OS (uses `os.startfile` for opening folders)
- Python 3.8+
- Pillow (PIL)
- keyboard
- pystray

## Notes

- The application needs to run with administrator privileges for the global hotkey to work properly
- Screenshots are saved in PNG format
- The preview automatically scales images to fit the preview pane

## Building Executable

### Quick Build

Simply run:
```bash
build.bat
```

Or:
```bash
python build_exe.py
```

This will create a portable `ScreenshotManager.exe` in the `dist` folder.

### Distribution

The executable can be distributed to any Windows machine without Python installed.
See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) for detailed build options.

## Troubleshooting

### Development Mode

If the Ctrl+PrintScreen hotkey doesn't work:
- Run the application as Administrator
- Check if another application is blocking the hotkey
- Ensure the keyboard library is properly installed

### Executable Mode

If issues occur with the executable:
- Run as Administrator for hotkey functionality
- Check antivirus software (may flag PyInstaller executables)
- Ensure Visual C++ Redistributable is installed

## File Structure

```
screenshot_app.py        - Main application file
requirements.txt         - Python dependencies
build_exe.py             - Build script for creating executable
build.bat                - Quick build batch file
screenshot_app.spec      - PyInstaller specification file
BUILD_INSTRUCTIONS.md    - Detailed build documentation
README.md               - This file
```

## Developer

Designed & Developed by **Bravetux** aka **B.Vignesh Kumar**  
Email: ic19939@gmail.com

Version: 1.0
