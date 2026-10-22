@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
echo ================================================
echo Upload Lab_10 files to GitHub
echo ================================================

where git >nul 2>nul
if errorlevel 1 (
  echo ERROR: Git is not installed or not in PATH.
  echo Install Git for Windows, then run this file again.
  pause
  exit /b 1
)

git rev-parse --show-toplevel >nul 2>nul
if errorlevel 1 (
  echo ERROR: This folder is not inside a cloned Git repository.
  echo First clone your GitHub repository, then copy this Lab_10 folder into it.
  echo Run this file from the Lab_10 folder inside that repository.
  pause
  exit /b 1
)

echo.
echo Staging all regular project files...
git add -A -- .
if errorlevel 1 goto failed

echo Force-adding hidden configuration files that some upload dialogs skip...
git add -f -- .env.example .gitignore .dockerignore .github/workflows/ci.yml
if errorlevel 1 goto failed

echo.
echo Files staged for upload:
git status --short

echo.
set /p CONFIRM=Commit and push these files to GitHub? (Y/N):
if /I not "%CONFIRM%"=="Y" (
  echo Cancelled. Files are staged locally but not pushed.
  pause
  exit /b 0
)

git commit -m "Add Lab 10 book catalog project"
if errorlevel 1 (
  echo Commit did not complete. Check whether there are changes to commit.
  pause
  exit /b 1
)
git push
if errorlevel 1 goto failed

echo.
echo Push completed. Check your GitHub repository in the browser.
pause
exit /b 0

:failed
echo.
echo An error occurred. Read the message above, fix it, and run this file again.
pause
exit /b 1
