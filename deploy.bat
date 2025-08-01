@echo off
setlocal

:: Deploy script for LearnAssist G-Assist Plugin
:: This script removes old plugin files and copies the new build to the G-Assist plugins directory

echo ========================================
echo LearnAssist Plugin Deployment Script
echo ========================================

set PLUGIN_DIR=%PROGRAMDATA%\NVIDIA Corporation\nvtopps\rise\plugins\learnassist
set SOURCE_DIR=%~dp0dist\learnassist

:: Check if source directory exists
if not exist "%SOURCE_DIR%" (
    echo ERROR: Source directory not found: %SOURCE_DIR%
    echo Please run build.bat first to create the plugin files.
    pause
    exit /b 1
)

:: Check if plugin directory exists and remove old version
if exist "%PLUGIN_DIR%" (
    echo Removing old LearnAssist plugin from: %PLUGIN_DIR%
    
    :: First, delete all files in the directory
    echo Deleting files in plugin directory...
    del /f /q "%PLUGIN_DIR%\*.*" >nul 2>&1
    
    :: Then remove any subdirectories
    for /d %%i in ("%PLUGIN_DIR%\*") do (
        echo Removing subdirectory: %%i
        rmdir /s /q "%%i" >nul 2>&1
    )
    
    :: Finally remove the main directory
    rmdir /q "%PLUGIN_DIR%"
    if %ERRORLEVEL% neq 0 (
        echo WARNING: Could not remove plugin directory completely.
        echo Attempting to continue with file deletion approach...
        :: Try alternative approach - just delete contents
        del /f /q "%PLUGIN_DIR%\*.*" >nul 2>&1
        for /d %%i in ("%PLUGIN_DIR%\*") do rmdir /s /q "%%i" >nul 2>&1
    )
    echo Old plugin files removed successfully.
) else (
    echo No existing plugin found to remove.
)

:: Create plugin directory
echo Creating plugin directory: %PLUGIN_DIR%
mkdir "%PLUGIN_DIR%"
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to create plugin directory.
    echo Make sure you have administrator privileges.
    pause
    exit /b 1
)

:: Copy new plugin files
echo Copying LearnAssist plugin files...
xcopy "%SOURCE_DIR%\*" "%PLUGIN_DIR%\" /E /Y
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to copy plugin files.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Deployment completed successfully!
echo ========================================
echo.
echo Plugin installed to: %PLUGIN_DIR%
echo.
echo Files copied:
dir "%PLUGIN_DIR%" /B
echo.
echo Next steps:
echo 1. Restart G-Assist if it's running
echo 2. Test the plugin with: /learnassist english what is noun?
echo 3. Check logs at: %%USERPROFILE%%\learnassist-plugin.log
echo.
pause