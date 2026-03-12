---
name: gog-linux-installer
description: Use when the user wants to install gogcli on a headless CentOS/RHEL 8 Linux server. This skill covers a Linux-first workflow that installs Homebrew, installs gog from the steipete tap, and completes Google OAuth on a server without a local browser UI.
---

# Gog Linux Installer

## Overview

This skill installs `gogcli` on a headless CentOS/RHEL 8 server with Homebrew.
Use it when the user wants a practical server workflow that:

- runs on Linux without a desktop UI
- installs Homebrew before installing `gog`
- handles Google OAuth from another machine through SSH port forwarding

## Workflow

### 1. Confirm the environment

Check the OS, current user, and the basic tools needed for bootstrap:

```bash
cat /etc/os-release
uname -a
whoami
sudo -V
curl --version
git --version
```

Interpretation:

- Continue when the machine is CentOS 8, RHEL 8, or a close equivalent.
- If `sudo`, `curl`, or `git` is missing, install them first.
- Prefer a non-root user for Homebrew installation.

Install missing prerequisites if needed:

```bash
sudo dnf install -y curl git tar
```

If `dnf` is unavailable, try:

```bash
sudo yum install -y curl git tar
```

### 2. Create or reuse a non-root user

If the server does not already have a suitable working user, create one and grant sudo access:

```bash
sudo useradd -m smartx
sudo usermod -aG wheel smartx
sudo passwd smartx
```

Notes:

- Do not hardcode a password in the skill workflow.
- If a suitable non-root user already exists, reuse it instead of creating `smartx`.

### 3. Switch to the working user

Use a login shell for the target user before installing Homebrew:

```bash
su - smartx
```

### 4. Install Homebrew

Run the official installer:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

On Linux, Homebrew normally installs to:

`/home/linuxbrew/.linuxbrew`

### 5. Load the Homebrew environment

Append the shell setup for future sessions and load it in the current shell:

```bash
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.bashrc
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
brew --version
```

If the user uses another shell, adapt the profile file instead of `.bashrc`.

### 6. Install gog from Homebrew

Install the tap package:

```bash
brew install steipete/tap/gogcli
```

Verify the binary is available:

```bash
which gog
gog version
gog --help
```

Successful verification means:

- `which gog` resolves to the Homebrew binary
- `gog version` prints version information
- `gog --help` shows top-level commands instead of failing

### 7. Optionally expose gog system-wide

If the user wants `root` or other accounts to call `gog` without loading the Homebrew shellenv, create a symlink:

```bash
sudo ln -sf /home/linuxbrew/.linuxbrew/bin/gog /usr/local/bin/gog
```

Only do this when the user actually wants a global path.

### 8. Configure Google OAuth credentials

Before adding an account, the user needs a Google OAuth desktop-app client.

Guide them through:

1. Open Google Cloud Console credentials.
2. Create or choose a project.
3. Enable the APIs they plan to use, such as Drive, Gmail, Calendar, Docs, or Sheets.
4. Configure the OAuth consent screen if required.
5. Create an OAuth client with application type `Desktop app`.
6. Download the client secret JSON file to the server.

Store the credentials with:

```bash
gog auth credentials /path/to/client_secret.json
```

### 9. Add the Google account on a headless server

Start the auth flow:

```bash
gog auth add yourname@smartx.com --services drive
```

Expected headless behavior:

- `gog` prints a Google authorization URL
- after login, Google redirects to `http://127.0.0.1:PORT/oauth2/callback?...`
- the server is waiting locally on that callback port

To complete the callback from another machine with a browser:

1. Run `gog auth add ...` on the server and copy the printed authorization URL.
2. Open the URL on your local machine and sign in to Google.
3. Note the callback URL and its `PORT`.
4. From your local machine, create an SSH tunnel to the Linux server:

```bash
ssh -L PORT:127.0.0.1:PORT user@server-host
```

5. With the tunnel still open, load the callback URL in the local browser so the request reaches the server.

If the user only needs a narrower scope, change the `--services` value accordingly.

### 10. Verify authentication

After auth succeeds, run a harmless command for the enabled service:

```bash
gog drive search "周报" --max 10
```

## Guidance

- Prefer executing the workflow instead of only describing it when the user asks you to install.
- Keep the explanation short unless the user asks for more detail.
- On Linux, default to the headless OAuth flow when the machine has no browser UI.
- If the user is already on a non-root working account, skip the user-creation step.
- If a command fails, report the exact blocker and continue with the narrowest fix.
- If Homebrew install fails because of missing build dependencies, install the missing packages first instead of switching workflows immediately.
