from flask import Flask, render_template, Response
import io, zipfile, os

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
    Write-Host "  [1/4] Downloading Lulu Kit..." -ForegroundColor Cyan
    $zipUrl = "https://lulu-kit-production.up.railway.app/lulu-kit.zip"
    Invoke-WebRequest -Uri $zipUrl -OutFile "$TMP\lulu-kit.zip" -UseBasicParsing
    Expand-Archive -Path "$TMP\lulu-kit.zip" -DestinationPath "$TMP\kit" -Force
    $kitDir = "$TMP\kit"

    # Step 2: Create dirs
    Write-Host "  [2/4] Creating directories..." -ForegroundColor Cyan
    @(
        "$HOME_DIR\.claude\skills\king-claude",
        "$HOME_DIR\.claude\skills\dispatch",
        "$HOME_DIR\.claude\skills\vision",
        "$HOME_DIR\.claude\skills\hearing",
        "$HOME_DIR\.claude\skills\file-organizer",
        "$HOME_DIR\.claude\skills\iphonetest",
        "$HOME_DIR\.claude\skills\gmail-signature",
        "$HOME_DIR\.claude\skills\ioi-proposal-server",
        "$HOME_DIR\.claude\skills\pmp-package",
        "$HOME_DIR\.claude\skills\video-translator",
        "$HOME_DIR\.claude\skills\resume-builder",
        "$HOME_DIR\.claude\commands",
        "$HOME_DIR\claude-vision\tasks",
        "$HOME_DIR\claude-vision\logs"
    ) | ForEach-Object { New-Item -ItemType Directory -Force -Path $_ | Out-Null }

    # Step 3: Install skills + commands (patch <HOME> -> real path)
    Write-Host "  [3/4] Installing skills..." -ForegroundColor Cyan
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
    Install-File "$kitDir\skills\gmail-signature\skill.md"     "$HOME_DIR\.claude\skills\gmail-signature\skill.md"
    Install-File "$kitDir\skills\ioi-proposal-server\skill.md" "$HOME_DIR\.claude\skills\ioi-proposal-server\skill.md"
    Install-File "$kitDir\skills\pmp-package\skill.md"         "$HOME_DIR\.claude\skills\pmp-package\skill.md"
    Install-File "$kitDir\skills\video-translator\skill.md"    "$HOME_DIR\.claude\skills\video-translator\skill.md"
    Install-File "$kitDir\skills\resume-builder\skill.md"      "$HOME_DIR\.claude\skills\resume-builder\skill.md"
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
    Write-Host "  [4/4] Installing Python dependencies..." -ForegroundColor Cyan
    pip install -r "$kitDir\vision-tools\requirements.txt" -q 2>$null
    playwright install chromium 2>$null

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

    Write-Host "  To begin:" -ForegroundColor Cyan
    Write-Host "  1. Open PowerShell in your project folder" -ForegroundColor White
    Write-Host "  2. Run: claude" -ForegroundColor Yellow
    Write-Host "  3. Type: /king-claude" -ForegroundColor White
    Write-Host ""

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


@app.route('/lulu-kit.zip')
def lulu_kit_zip():
    base = os.path.dirname(os.path.abspath(__file__))
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        dirs_to_pack = [
            'skills',
            'commands',
            'vision-tools',
        ]
        files_to_pack = [
            'GLOBAL_CLAUDE.md',
            'install.ps1',
        ]
        for d in dirs_to_pack:
            d_path = os.path.join(base, d)
            if os.path.isdir(d_path):
                for root, _, files in os.walk(d_path):
                    for f in files:
                        full = os.path.join(root, f)
                        arcname = os.path.relpath(full, base)
                        zf.write(full, arcname)
        for f in files_to_pack:
            full = os.path.join(base, f)
            if os.path.isfile(full):
                zf.write(full, f)
    buf.seek(0)
    return Response(
        buf.read(),
        mimetype='application/zip',
        headers={'Content-Disposition': 'attachment; filename="lulu-kit.zip"'}
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
