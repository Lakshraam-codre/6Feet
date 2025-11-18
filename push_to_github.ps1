# push_to_github.ps1
# Interactive PowerShell helper to initialize Git, commit, and push to a remote GitHub repository.
# Usage: Open PowerShell in project root (C:\Users\laksh\OneDrive\Desktop\googleai) and run:
#   ./push_to_github.ps1

function Check-Git {
    $git = Get-Command git -ErrorAction SilentlyContinue
    if (-not $git) {
        Write-Host "Git is not installed or not in PATH." -ForegroundColor Red
        Write-Host "Install Git for Windows: https://git-scm.com/download/win" -ForegroundColor Yellow
        return $false
    }
    return $true
}

if (-not (Check-Git)) { exit 1 }

# Ensure script runs from repository root
$projectRoot = Get-Location
Write-Host "Project root: $projectRoot"

# Init repo if needed
if (-not (Test-Path "$projectRoot\.git")) {
    Write-Host "No git repository found. Initializing..." -ForegroundColor Cyan
    git init
} else {
    Write-Host "Git repository already initialized." -ForegroundColor Green
}

# Configure user if not set
$userName = git config --global user.name
$userEmail = git config --global user.email
if (-not $userName) {
    $userName = Read-Host "Enter Git user.name (e.g. Your Name)"
    git config --global user.name "$userName"
}
if (-not $userEmail) {
    $userEmail = Read-Host "Enter Git user.email (e.g. you@example.com)"
    git config --global user.email "$userEmail"
}

# Show status
git status --porcelain

# Add files (respecting .gitignore)
Write-Host "Adding files to git (this respects .gitignore)..." -ForegroundColor Cyan
git add .

# Commit
$defaultMsg = "chore: initial commit - project files"
$msg = Read-Host "Commit message (press Enter for default: '$defaultMsg')"
if ([string]::IsNullOrWhiteSpace($msg)) { $msg = $defaultMsg }

git commit -m "$msg" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "No changes to commit or commit failed. Continuing..." -ForegroundColor Yellow
} else {
    Write-Host "Committed: $msg" -ForegroundColor Green
}

# Ask for remote URL
$remoteUrl = Read-Host "Enter remote URL (HTTPS or SSH) for your GitHub repo (leave blank to skip pushing)"
if (-not [string]::IsNullOrWhiteSpace($remoteUrl)) {
    # Add or set origin
    $existingRemote = git remote get-url origin 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Origin already exists. Updating origin to provided URL." -ForegroundColor Cyan
        git remote set-url origin $remoteUrl
    } else {
        Write-Host "Adding origin remote." -ForegroundColor Cyan
        git remote add origin $remoteUrl
    }

    # Ensure main branch
    git branch -M main 2>$null

    Write-Host "Pushing to origin main (you may be prompted for credentials)..." -ForegroundColor Cyan
    git push -u origin main
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Push succeeded." -ForegroundColor Green
    } else {
        Write-Host "Push failed. See git output above. If using HTTPS, ensure you provide a valid PAT when prompted, or configure SSH keys." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Skipping push. You can add a remote later with: git remote add origin <URL> and git push -u origin main" -ForegroundColor Yellow
}

Write-Host "Done. Repository is ready." -ForegroundColor Green
