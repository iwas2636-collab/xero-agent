@echo off
REM GitHub Integration Script for PDD Projects
REM Automates the complete GitHub setup process

echo.
echo =====================================
echo   PDD GitHub Integration Setup
echo =====================================
echo.

REM Check if we're in a PDD project directory
if not exist "start-universal.bat" (
    echo Error: Not in a PDD project directory
    echo Please run this from your PDD project root folder
    pause
    exit /b 1
)

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if Git is available
git --version >nul 2>&1
if errorlevel 1 (
    echo Error: Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com
    pause
    exit /b 1
)

echo Git and Python are available, starting integration...
echo.

REM Install required dependencies
echo Installing GitHub integration dependencies...
pip install requests >nul 2>&1

REM Run the GitHub integrator
echo.
echo Starting automated GitHub integration...
echo Follow the prompts to complete the setup.
echo.

python scripts\github_integrator.py

if errorlevel 1 (
    echo.
    echo GitHub integration encountered an error.
    echo Please check the output above for details.
) else (
    echo.
    echo ========================================
    echo   GitHub Integration Complete!
    echo ========================================
    echo.
    echo Your PDD project is now on GitHub with:
    echo   - Version control with Git
    echo   - GitHub Actions CI/CD
    echo   - Issue and PR templates
    echo   - PHR validation workflow
    echo   - Security scanning
    echo.
    echo Next steps:
    echo   1. Visit your repository on GitHub
    echo   2. Enable branch protection (optional)
    echo   3. Set up GitHub Pages (optional)
    echo   4. Invite collaborators (optional)
    echo.
)

echo.
pause