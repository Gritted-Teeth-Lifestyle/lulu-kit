# Lulu Kit Installer
param()

$HOME_DIR = $env:USERPROFILE
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host ""
Write-Host "  Lulu Kit Installer" -ForegroundColor Magenta
Write-Host "  Installing for: $HOME_DIR" -ForegroundColor Cyan
Write-Host ""

# Create all directories
$dirs = @(
    "$HOME_DIR\.claude\skills\king-claude",
    "$HOME_DIR\.claude\skills\dispatch",
    "$HOME_DIR\.claude\skills\vision",
    "$HOME_DIR\.claude\skills\hearing",
    "$HOME_DIR\.claude\skills\file-organizer",
    "$HOME_DIR\.claude\skills\iphonetest",
    "$HOME_DIR\.claude\commands",
    "$HOME_DIR\claude-vision"
)
foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}
Write-Host "  Directories created." -ForegroundColor Green

# Install and patch skill files (use .Replace() not -replace to avoid regex backslash issues)
function Install-Skill($src, $dest) {
    $content = [System.IO.File]::ReadAllText($src)
    $content = $content.Replace("<HOME>", $HOME_DIR)
    [System.IO.File]::WriteAllText($dest, $content, [System.Text.Encoding]::UTF8)
}

Install-Skill "$SCRIPT_DIR\skills\king-claude\SKILL.md" "$HOME_DIR\.claude\skills\king-claude\SKILL.md"
Install-Skill "$SCRIPT_DIR\skills\dispatch\skill.md" "$HOME_DIR\.claude\skills\dispatch\skill.md"
Install-Skill "$SCRIPT_DIR\skills\vision\skill.md" "$HOME_DIR\.claude\skills\vision\skill.md"
Install-Skill "$SCRIPT_DIR\skills\hearing\SKILL.md" "$HOME_DIR\.claude\skills\hearing\SKILL.md"
Install-Skill "$SCRIPT_DIR\skills\file-organizer\SKILL.md" "$HOME_DIR\.claude\skills\file-organizer\SKILL.md"
Install-Skill "$SCRIPT_DIR\skills\iphonetest\skill.md" "$HOME_DIR\.claude\skills\iphonetest\skill.md"
Install-Skill "$SCRIPT_DIR\skills\iphonetest\iphonetest.py" "$HOME_DIR\.claude\skills\iphonetest\iphonetest.py"
Install-Skill "$SCRIPT_DIR\commands\javascript.md" "$HOME_DIR\.claude\commands\javascript.md"
Install-Skill "$SCRIPT_DIR\commands\p5-ui.md" "$HOME_DIR\.claude\commands\p5-ui.md"
Install-Skill "$SCRIPT_DIR\commands\plugin.md" "$HOME_DIR\.claude\commands\plugin.md"
Write-Host "  Skills installed." -ForegroundColor Green

# Copy vision tools
foreach ($f in @("winvision.py","browser.py","audio.py","alert.py")) {
    Copy-Item "$SCRIPT_DIR\vision-tools\$f" "$HOME_DIR\claude-vision\$f" -Force
}
Write-Host "  Vision tools installed." -ForegroundColor Green

# Python deps
Write-Host "  Installing Python dependencies..." -ForegroundColor Yellow
pip install -r "$SCRIPT_DIR\vision-tools\requirements.txt" --quiet
playwright install chromium
Write-Host "  Python deps done." -ForegroundColor Green

Write-Host ""
Write-Host "  =====================================" -ForegroundColor Cyan
Write-Host "    LULU KIT INSTALLED SUCCESSFULLY   " -ForegroundColor Cyan
Write-Host "  =====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Next steps:" -ForegroundColor White
Write-Host "  1. Open: GLOBAL_CLAUDE.md in this folder" -ForegroundColor White
Write-Host "  2. Copy its contents into: $HOME_DIR\.claude\CLAUDE.md" -ForegroundColor Yellow
Write-Host "     (Create the file if it doesn't exist)" -ForegroundColor Gray
Write-Host "  3. Open Claude Code and type: /king-claude" -ForegroundColor White
Write-Host "  4. Emperor Lelouch will take the throne." -ForegroundColor Magenta
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
