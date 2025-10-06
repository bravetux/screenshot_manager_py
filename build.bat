@echo off
echo ================================================
echo Screenshot Manager - Build Executable
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo Building executable...
echo.

REM Run the build script
python build_exe.py

echo.
echo ================================================
echo Build process finished!
echo ================================================
echo.
pause
