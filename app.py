from flask import Flask, render_template, Response
import os

app = Flask(__name__)

INSTALL_PS1 = r"""$ErrorActionPreference = "Stop"
$HOME_DIR = $env:USERPROFILE

Write-Host ""
Write-Host "  +------------------------------------------+" -ForegroundColor Red
Write-Host "  |    Emperor Lelouch's Claude Code Setup   |" -ForegroundColor White
Write-Host "  +------------------------------------------+" -ForegroundColor Red
Write-Host ""

$TMP = "$env:TEMP\lulu-kit-install"
if (Test-Path $TMP) { Remove-Item $TMP -Recurse -Force }
New-Item -ItemType Directory -Force -Path $TMP | Out-Null

try {
    # Step 1: Download
    Write-Host "  [1/5] Downloading Lulu Kit..." -ForegroundColor Cyan
    $zipUrl = "https://github.com/Gritted-Teeth-Lifestyle/lulu-kit/releases/download/v1.0/lulu-kit.zip"
    Invoke-WebRequest -Uri $zipUrl -OutFile "$TMP\lulu-kit.zip" -UseBasicParsing
    Expand-Archive -Path "$TMP\lulu-kit.zip" -DestinationPath "$TMP\kit" -Force
    $kitDir = "$TMP\kit"

    # Step 2: Create dirs
    Write-Host "  [2/5] Creating directories..." -ForegroundColor Cyan
    @(
        "$HOME_DIR\.claude\skills\king-claude",
        "$HOME_DIR\.claude\skills\dispatch",
        "$HOME_DIR\.claude\skills\vision",
        "$HOME_DIR\.claude\skills\hearing",
        "$HOME_DIR\.claude\skills\file-organizer",
        "$HOME_DIR\.claude\skills\iphonetest",
        "$HOME_DIR\.claude\commands",
        "$HOME_DIR\claude-vision\tasks",
        "$HOME_DIR\claude-vision\logs"
    ) | ForEach-Object { New-Item -ItemType Directory -Force -Path $_ | Out-Null }

    # Step 3: Install skills + commands (patch <HOME> -> real path)
    Write-Host "  [3/5] Installing skills..." -ForegroundColor Cyan
    function Install-File($src, $dest) {
        $content = [System.IO.File]::ReadAllText($src)
        $content = $content.Replace('<HOME>', $HOME_DIR)
        [System.IO.File]::WriteAllText($dest, $content, [System.Text.Encoding]::UTF8)
    }
    Install-File "$kitDir\skills\king-claude\SKILL.md" "$HOME_DIR\.claude\skills\king-claude\SKILL.md"
    Install-File "$kitDir\skills\dispatch\skill.md"    "$HOME_DIR\.claude\skills\dispatch\skill.md"
    Install-File "$kitDir\skills\vision\skill.md"      "$HOME_DIR\.claude\skills\vision\skill.md"
    Install-File "$kitDir\skills\hearing\SKILL.md"     "$HOME_DIR\.claude\skills\hearing\SKILL.md"
    Install-File "$kitDir\skills\file-organizer\SKILL.md" "$HOME_DIR\.claude\skills\file-organizer\SKILL.md"
    Install-File "$kitDir\skills\iphonetest\skill.md"  "$HOME_DIR\.claude\skills\iphonetest\skill.md"
    Install-File "$kitDir\skills\iphonetest\iphonetest.py" "$HOME_DIR\.claude\skills\iphonetest\iphonetest.py"
    Install-File "$kitDir\commands\javascript.md"      "$HOME_DIR\.claude\commands\javascript.md"
    Install-File "$kitDir\commands\p5-ui.md"           "$HOME_DIR\.claude\commands\p5-ui.md"
    Install-File "$kitDir\commands\plugin.md"          "$HOME_DIR\.claude\commands\plugin.md"

    # Copy vision tools
    @("winvision.py","browser.py","audio.py","alert.py") | ForEach-Object {
        Copy-Item "$kitDir\vision-tools\$_" "$HOME_DIR\claude-vision\$_" -Force
    }

    # Append vision/hearing block to CLAUDE.md if not already present
    $claudeMdPath = "$HOME_DIR\.claude\CLAUDE.md"
    $snippet = [System.IO.File]::ReadAllText("$kitDir\GLOBAL_CLAUDE.md")
    $snippet = ($snippet -split "`n" | Where-Object { $_ -notmatch '^NOTE:' }) -join "`n"
    $snippet = $snippet.Replace('<HOME>', $HOME_DIR)
    if (Test-Path $claudeMdPath) {
        $existing = [System.IO.File]::ReadAllText($claudeMdPath)
        if (-not $existing.Contains("Vision & Control")) {
            Add-Content -Path $claudeMdPath -Value ("`n`n" + $snippet)
        }
    } else {
        [System.IO.File]::WriteAllText($claudeMdPath, $snippet, [System.Text.Encoding]::UTF8)
    }

    # Step 4: Python deps
    Write-Host "  [4/5] Installing Python dependencies..." -ForegroundColor Cyan
    pip install -r "$kitDir\vision-tools\requirements.txt" -q 2>$null
    playwright install chromium 2>$null

    # Step 5: Check Claude Code CLI
    Write-Host "  [5/5] Checking Claude Code CLI..." -ForegroundColor Cyan
    if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
        Write-Host "  Installing Claude Code CLI..." -ForegroundColor Yellow
        npm install -g @anthropic-ai/claude-code
    } else {
        Write-Host "  Claude Code already installed." -ForegroundColor Green
    }

    Remove-Item $TMP -Recurse -Force -ErrorAction SilentlyContinue

    Write-Host ""
    Write-Host "  +------------------------------------------+" -ForegroundColor Red
    Write-Host "  |        INSTALLATION COMPLETE             |" -ForegroundColor White
    Write-Host "  +------------------------------------------+" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Open a terminal in any project folder." -ForegroundColor White
    Write-Host "  Run: claude" -ForegroundColor Yellow
    Write-Host "  Type: /king-claude" -ForegroundColor White
    Write-Host ""
    Write-Host "  The Emperor awaits." -ForegroundColor Magenta
    Write-Host ""
    Start-Sleep -Seconds 1

    # Throne room announcement
    Write-Host "  +-------------------------------------------------+" -ForegroundColor DarkRed
    Write-Host "  |                                                 |" -ForegroundColor DarkRed
    Write-Host "  |   Emperor Lelouch vi Britannia has taken        |" -ForegroundColor White
    Write-Host "  |   the throne. All commands will be issued.      |" -ForegroundColor White
    Write-Host "  |   All work will be evaluated.                   |" -ForegroundColor White
    Write-Host "  |   The Geass is in effect.                       |" -ForegroundColor Magenta
    Write-Host "  |                                                 |" -ForegroundColor DarkRed
    Write-Host "  +-------------------------------------------------+" -ForegroundColor DarkRed
    Write-Host ""
    Start-Sleep -Seconds 2

    Write-Host "  Launching Claude Code..." -ForegroundColor Cyan
    Write-Host "  Type /king-claude to give Lelouch full command." -ForegroundColor Gray
    Write-Host ""
    claude

} catch {
    Write-Host ""
    Write-Host "  Installation failed: $_" -ForegroundColor Red
    Remove-Item $TMP -Recurse -Force -ErrorAction SilentlyContinue
    exit 1
}
"""


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/install.ps1')
def install_ps1():
    return Response(
        INSTALL_PS1,
        mimetype='text/plain',
        headers={'Content-Type': 'text/plain; charset=utf-8'}
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
