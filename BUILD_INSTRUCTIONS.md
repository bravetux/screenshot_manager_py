# Building Screenshot Manager Executable

This guide explains how to build a portable Windows executable from the Python source code.

## Prerequisites

- Windows OS (7 or later)
- Python 3.8 or higher installed
- Internet connection (for downloading dependencies)

## Quick Build (Recommended)

### Method 1: Using the Build Script

1. Open Command Prompt or PowerShell in the project directory
2. Run the batch file:
   ```batch
   build.bat
   ```
3. The script will:
   - Check Python installation
   - Install PyInstaller if needed
   - Create application icon
   - Build the executable
   - Generate README file

### Method 2: Using Python Script Directly

```bash
python build_exe.py
```

This will create a single executable file in the `dist` folder.

## Manual Build

If you prefer to build manually:

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Pillow (Image processing)
- keyboard (Global hotkey support)
- pystray (System tray integration)
- PyInstaller (Executable builder)

### Step 2: Create Icon (Optional)

Run this to create the application icon:
```bash
python -c "from build_exe import create_icon; create_icon()"
```

### Step 3: Build with PyInstaller

**Option A - Using the spec file (Recommended):**
```bash
pyinstaller screenshot_app.spec
```

**Option B - Direct command:**
```bash
pyinstaller --onefile --windowed --name ScreenshotManager --icon screenshot_icon.ico --hidden-import PIL._tkinter_finder --hidden-import pystray._win32 --hidden-import keyboard screenshot_app.py
```

## Build Output

After successful build:

```
dist/
├── ScreenshotManager.exe   # Main executable (portable)
└── README.txt              # User documentation
```

### File Sizes (Approximate)
- Executable: ~25-35 MB (includes Python runtime and all dependencies)
- ZIP Distribution: ~15-20 MB (compressed)

## Distribution

### Creating Distribution Package

The build script will offer to create a ZIP file containing:
- ScreenshotManager.exe
- README.txt

You can distribute this ZIP file to any Windows machine without Python installed.

### Manual ZIP Creation

```bash
# Create a distribution folder
mkdir ScreenshotManager_Distribution
copy dist\ScreenshotManager.exe ScreenshotManager_Distribution\
copy dist\README.txt ScreenshotManager_Distribution\

# Compress to ZIP (use any ZIP tool)
```

## Testing the Executable

1. Navigate to `dist` folder
2. Run `ScreenshotManager.exe`
3. Test all features:
   - Screenshot capture (Ctrl+PrintScreen)
   - File list and preview
   - Rename/Delete operations
   - System tray minimize/restore
   - Exit functionality

## Troubleshooting

### Build Errors

**Error: PyInstaller not found**
```bash
pip install pyinstaller
```

**Error: Module not found during build**
- Add the module to `hiddenimports` in `screenshot_app.spec`
- Or use `--hidden-import module_name` flag

**Error: Icon file not found**
- Run `python build_exe.py` which creates the icon automatically
- Or remove `--icon` parameter from PyInstaller command

### Runtime Issues

**Antivirus Warnings**
- This is common with PyInstaller executables
- The executable is safe - you can whitelist it
- Consider code signing certificate for production distribution

**Slow Startup**
- First run unpacks files to temp directory (normal)
- Subsequent runs are faster

**Missing DLL Errors**
- Install Visual C++ Redistributable
- Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe

## Build Optimization

### Reduce Executable Size

1. **Use UPX Compression** (included in spec file):
   - Download UPX from: https://upx.github.io/
   - Place in PATH or PyInstaller directory

2. **Exclude Unnecessary Modules**:
   Edit `screenshot_app.spec` and add to `excludes`:
   ```python
   excludes=['matplotlib', 'numpy', 'pandas', 'scipy']
   ```

3. **Use `--onedir` instead of `--onefile`**:
   - Creates a folder with executable and dependencies
   - Faster startup time
   - Larger distribution size

## Advanced Options

### Creating Installer (Optional)

Use NSIS or Inno Setup to create a professional installer:

**NSIS Example:**
```nsis
Name "Screenshot Manager"
OutFile "ScreenshotManager_Setup.exe"
InstallDir "$PROGRAMFILES\ScreenshotManager"
RequestExecutionLevel admin

Section "Install"
    SetOutPath "$INSTDIR"
    File "dist\ScreenshotManager.exe"
    CreateShortcut "$DESKTOP\Screenshot Manager.lnk" "$INSTDIR\ScreenshotManager.exe"
SectionEnd
```

### Code Signing (Professional Distribution)

1. Obtain a code signing certificate
2. Use `signtool.exe`:
   ```bash
   signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com dist\ScreenshotManager.exe
   ```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build Executable

on: [push, pull_request]

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: python build_exe.py
      - uses: actions/upload-artifact@v2
        with:
          name: ScreenshotManager
          path: dist/ScreenshotManager.exe
```

## Version Information

To add version info to the executable:

1. Create `version_info.txt`:
```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [StringStruct(u'CompanyName', u'Bravetux'),
           StringStruct(u'FileDescription', u'Screenshot Manager'),
           StringStruct(u'FileVersion', u'1.0.0.0'),
           StringStruct(u'InternalName', u'ScreenshotManager'),
           StringStruct(u'LegalCopyright', u'Copyright (c) 2025 Bravetux'),
           StringStruct(u'OriginalFilename', u'ScreenshotManager.exe'),
           StringStruct(u'ProductName', u'Screenshot Manager'),
           StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

2. Add to PyInstaller command:
```bash
--version-file version_info.txt
```

## Support

For build issues or questions:
- Email: ic19939@gmail.com
- Check PyInstaller docs: https://pyinstaller.org/

## License

Designed & Developed by Bravetux aka B.Vignesh Kumar
