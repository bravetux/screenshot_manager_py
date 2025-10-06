# Quick Start Guide - Screenshot Manager

## For Developers (Building from Source)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python screenshot_app.py
```

### Step 3: Build Executable (Optional)
```bash
build.bat
```
or
```bash
python build_exe.py
```

The executable will be in the `dist` folder.

---

## For End Users (Using the Executable)

### Step 1: Extract and Run
1. Extract the ZIP file to any folder
2. Double-click `ScreenshotManager.exe`
3. (Optional) Run as Administrator for best hotkey performance

### Step 2: Capture Screenshots
- Press **Ctrl + PrintScreen** anywhere to capture
- Screenshots are saved to: `C:\Screenshot`
- Filename format: `ss_ddmmyyyy_hhmmss.png`

### Step 3: Manage Screenshots
- View list of screenshots in the left panel
- Click any screenshot to preview it
- Use buttons to:
  - 🔄 Refresh - Update the file list
  - ✏️ Rename - Change screenshot name
  - 🗑️ Delete - Remove screenshot
  - 📁 Open Folder - View in File Explorer

### Step 4: System Tray
- Close window to minimize to system tray (app keeps running)
- Right-click tray icon to:
  - **Restore** - Bring window back
  - **Exit** - Close application completely

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl + PrintScreen | Capture screenshot |

---

## First Time Setup

1. **Allow Firewall** (if prompted)
   - Click "Allow access" when Windows Firewall asks

2. **Antivirus Warning** (may occur)
   - This is normal for PyInstaller executables
   - Add to whitelist/exceptions if needed

3. **Administrator Rights** (recommended)
   - Right-click executable → "Run as administrator"
   - Ensures global hotkey works everywhere

---

## Troubleshooting

### Hotkey not working?
✅ Run as Administrator  
✅ Check if another app uses Ctrl+PrintScreen  
✅ Try clicking on another window first, then press hotkey

### App not starting?
✅ Install Visual C++ Redistributable:  
   https://aka.ms/vs/17/release/vc_redist.x64.exe

### System tray icon not appearing?
✅ Check Windows system tray settings  
✅ Look in "Hidden icons" (arrow near clock)

### Antivirus blocking?
✅ This is a false positive (common with PyInstaller)  
✅ Add exception in your antivirus software

---

## Support

**Developer:** Bravetux aka B.Vignesh Kumar  
**Email:** ic19939@gmail.com  
**Version:** 1.0

---

## Tips & Tricks

💡 **Tip 1:** Keep the app minimized in system tray for quick access

💡 **Tip 2:** Rename screenshots immediately after capture for better organization

💡 **Tip 3:** Create shortcuts to different screenshot categories using folders

💡 **Tip 4:** Double-click a screenshot filename to preview it

💡 **Tip 5:** The app creates C:\Screenshot folder automatically on first run

---

Enjoy using Screenshot Manager! 📸
