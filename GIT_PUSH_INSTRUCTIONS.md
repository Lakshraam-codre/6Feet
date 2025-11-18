# How to Push this Project to Your GitHub Repository

This document explains how to install Git (if needed), create a GitHub repo, and run the included `push_to_github.ps1` script to initialize, commit, and push the project.

## 1) Install Git for Windows (if not installed)

- Download and install Git for Windows: https://git-scm.com/download/win
- Use the default installer options (recommended)
- After installation, open a new PowerShell window

Verify installation:

```powershell
git --version
```

## 2) Create a new GitHub repository

1. Go to https://github.com and sign in.
2. Click the green **New** button (top-left) to create a new repository.
3. Name it (e.g., `agri-chatbot`).
4. Do NOT add a README, .gitignore, or license on GitHub (we already have these locally).
5. Create repository.
6. Copy the repository HTTPS URL (e.g. `https://github.com/yourusername/agri-chatbot.git`) or SSH URL.

## 3) Run the push script (interactive)

Open PowerShell in the project root (where `push_to_github.ps1` lives):

```powershell
cd C:\Users\laksh\OneDrive\Desktop\googleai
.\push_to_github.ps1
```

The script will:
- Check for Git
- Initialize the repo if necessary
- Ask for `user.name` and `user.email` if not configured
- Stage files and create a commit (you can enter your own message)
- Ask for the remote URL and push to `main`

If you prefer, run the same commands manually (non-interactive):

```powershell
cd C:\Users\laksh\OneDrive\Desktop\googleai
git init
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git add .
git commit -m "chore: initial commit"
git remote add origin https://github.com/yourusername/agri-chatbot.git
git branch -M main
git push -u origin main
```

## 4) Authentication notes

- If you use HTTPS, GitHub now requires a Personal Access Token (PAT) instead of your account password when pushing from the command line.
  - Create a PAT: https://github.com/settings/tokens
  - Scope: `repo` is sufficient for pushing.
  - When prompted for a password, paste the PAT.

- Alternatively, configure SSH keys and use the SSH repo URL (recommended for repeated pushes): https://docs.github.com/en/authentication/connecting-to-github-with-ssh

## 5) Troubleshooting

- `git` not recognized: close PowerShell and reopen after installing Git, or ensure Git was installed to PATH.
- Push fails with `403` or `authentication failed`: use a PAT or check SSH keys.
- Large files or LFS issues: check `.gitignore` and remove large files before committing.

## 6) After push

- Open the GitHub repo URL in your browser and verify files are present.
- Enable branch protection, add collaborators, or create releases as needed.


---

If you want, I can:
- Create the GitHub repo for you (requires a GitHub PAT with `repo` scope) and push automatically.
- Or walk you through each command interactively.

Which do you prefer?