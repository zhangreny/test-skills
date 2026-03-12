---
name: gog-windows-install
description: Use when the user wants to install or build gogcli on Windows. This skill covers a Windows-first workflow that requires git and Go, explicitly avoids make, and verifies the resulting gog.exe binary.
---

# Gog Windows Install

## Overview

This skill installs and builds `gogcli` on Windows with a minimal toolchain.
Use it when the user wants a practical Windows setup that relies on `git` and `go` only and does not require `make`.

## When To Use It

- The user asks how to install `gog`, `gogcli`, or "Google CLI" on Windows and means the `steipete/gogcli` project.
- The user wants you to carry out the install instead of just describing it.
- The machine is Windows and either lacks `make` or the user wants to avoid installing it.

## Workflow

### 1. Confirm prerequisites

Check these tools first:

```powershell
git --version
go version
```

Interpretation:

- If `git` exists, keep going.
- If `go` is missing, install Go with `winget`.
- Do not install `make` unless the user explicitly asks for it.

Install Go if needed:

```powershell
winget install -e --id GoLang.Go --accept-source-agreements --accept-package-agreements
```

After installing Go, prefer using the full path once so the current session does not depend on a fresh shell:

```powershell
& 'C:\Program Files\Go\bin\go.exe' version
```

### 2. Clone the repository

Clone the upstream repo into the current workspace unless the user asked for another location:

```powershell
git clone https://github.com/steipete/gogcli.git
```

If the target directory already exists, inspect it before doing anything destructive. Prefer reusing the existing clone instead of deleting it.

### 3. Build without make

The repo README may say `make`, but on Windows you can use the equivalent `go build` directly. This is the default path for this skill.

From the repo root, build `cmd/gog` into `bin/gog.exe`:

```powershell
$ErrorActionPreference='Stop'
$env:PATH = 'C:\Program Files\Go\bin;' + $env:PATH
$version = (git describe --tags --always --dirty 2>$null)
if (-not $version) { $version = 'dev' }
$commit = (git rev-parse --short=12 HEAD 2>$null)
$date = [DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ')
New-Item -ItemType Directory -Force -Path '.\bin' | Out-Null
& 'C:\Program Files\Go\bin\go.exe' build -ldflags "-X github.com/steipete/gogcli/internal/cmd.version=$version -X github.com/steipete/gogcli/internal/cmd.commit=$commit -X github.com/steipete/gogcli/internal/cmd.date=$date" -o '.\bin\gog.exe' ./cmd/gog
```

Notes:

- This intentionally replaces `make`.
- `go build` will download Go dependencies on first run.
- Use `C:\Program Files\Go\bin\go.exe` if the shell has not picked up the new PATH yet.

### 4. Verify the binary

Run:

```powershell
.\bin\gog.exe version
.\bin\gog.exe --help
```

Successful verification means:

- `version` prints a version string and commit metadata.
- `--help` prints top-level commands instead of an error.

### 5. Hand off the next step

Once install and build succeed, tell the user where the binary is:

`<repo>\bin\gog.exe`

### 6. Configure Google OAuth credentials

Before adding an account, the user needs a Google OAuth desktop-app client.

Guide them through:

1. Open Google Cloud Console credentials.
2. Create or choose a project.
3. Enable the APIs they plan to use, such as Drive, Gmail, Calendar, Docs, or Sheets.
4. Configure the OAuth consent screen if required.
5. Create an OAuth client with application type `Desktop app`.
6. Download the client secret JSON file.

Store the credentials with:

```powershell
.\bin\gog.exe auth credentials C:\path\to\client_secret.json
```

### 7. Add the Google account

On Windows, treat browser-based OAuth as the default flow because the machine normally has a UI.

Run:

```powershell
.\bin\gog.exe auth add you@gmail.com
```

If the user only needs a narrower permission set, they may add flags such as:

```powershell
.\bin\gog.exe auth add you@gmail.com --services drive
.\bin\gog.exe auth add you@gmail.com --readonly
```

Expected Windows behavior:

- `gog` opens the system browser, or prints a URL to open.
- The user signs in and approves access in the browser.
- The callback completes locally on the same Windows machine.
- No SSH tunnel is needed for the normal Windows flow.

### 8. Verify authentication

After auth succeeds, verify with a harmless command for the service the user enabled:

```powershell
gog drive search "周报" --max 10
```

## Guidance

- Prefer executing the workflow instead of only describing it when the user asks you to install.
- Keep the explanation short unless the user asks for more detail.
- If `winget` is unavailable, explain that Go still needs to be installed and ask whether to use another package manager or manual MSI install.
- On Windows, default to normal browser OAuth first. Do not lead with headless Linux-style SSH tunnel guidance unless the environment is clearly non-UI.
- If a command fails, report the exact blocker and continue with the narrowest fix.
