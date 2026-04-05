@echo off
setlocal

set "ROOT_DIR=%~dp0"
if "%RELEASE_VERSION%"=="" set "RELEASE_VERSION=dev"
set "ZIP_NAME=ULTRA_FORCE-windows-%RELEASE_VERSION%.zip"
set "SETUP_NAME=ULTRA_FORCE-windows-%RELEASE_VERSION%-setup.exe"
set "CHECKSUM_NAME=ULTRA_FORCE-windows-%RELEASE_VERSION%-sha256.txt"

call "%ROOT_DIR%build_web_app.bat"
if errorlevel 1 exit /b 1

echo [1/4] Packaging application folder
powershell -NoProfile -Command "if (Test-Path '%ROOT_DIR%dist\%ZIP_NAME%') { Remove-Item '%ROOT_DIR%dist\%ZIP_NAME%' -Force }"
if errorlevel 1 exit /b 1

echo [2/4] Creating ZIP archive with 7-Zip
7z a -tzip "%ROOT_DIR%dist\%ZIP_NAME%" "%ROOT_DIR%dist\ULTRA_FORCE\*" >nul
if errorlevel 1 exit /b 1

echo [3/4] Building Windows installer
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" (
  "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" "%ROOT_DIR%installer_windows.iss"
  if errorlevel 1 exit /b 1
)

echo [4/4] Writing checksums
powershell -NoProfile -Command "$files = @('%ROOT_DIR%dist\%ZIP_NAME%'); if (Test-Path '%ROOT_DIR%dist\%SETUP_NAME%') { $files += '%ROOT_DIR%dist\%SETUP_NAME%' }; Get-FileHash -Algorithm SHA256 $files | ForEach-Object { "" + $_.Hash.ToLower() + ' *' + [System.IO.Path]::GetFileName($_.Path) } | Set-Content '%ROOT_DIR%dist\%CHECKSUM_NAME%'"
if errorlevel 1 exit /b 1

echo.
echo Release ready:
echo   %ROOT_DIR%dist\%ZIP_NAME%
if exist "%ROOT_DIR%dist\%SETUP_NAME%" echo   %ROOT_DIR%dist\%SETUP_NAME%
echo   %ROOT_DIR%dist\%CHECKSUM_NAME%
endlocal
