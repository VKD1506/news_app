$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

$buildVenv = Join-Path $root ".build-venv"
$buildPython = Join-Path $buildVenv "Scripts\python.exe"

if (-not (Test-Path $buildPython)) {
    py -3.12 -m venv $buildVenv
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to create the Python 3.12 build environment."
    }
}

& $buildPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    throw "Failed to upgrade pip in the build environment."
}

& $buildPython -m pip install -r requirements.txt pyinstaller
if ($LASTEXITCODE -ne 0) {
    throw "Failed to install build dependencies."
}

& $buildPython -m PyInstaller `
  --noconfirm `
  --clean `
  --name NewsApp `
  --onefile `
  --add-data "templates;templates" `
  --add-data "static;static" `
  launcher.py
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller build failed."
}

Write-Host ""
Write-Host "Build complete. Executable created at dist\NewsApp.exe"
