# Media Browser

A Roku channel for browsing and streaming media from a [SimpleFileServer](https://github.com/dazn/SimpleFileServer) backend over your local network.

## Features

- Browse a remote media library as a hierarchical file tree
- Type-appropriate icons for folders, video, audio, and other files
- Plays video and audio natively via the Roku media player (mp4, mkv, hls, dash, mp3, mka, mks)

## Requirements

- A Roku device with **Developer Mode** enabled
- A running SimpleFileServer instance accessible on the local network
- Python 3 + [uv](https://github.com/astral-sh/uv) (for building and deploying)

## Configuration

Before building, edit `source/config.brs` to set your server address and API key:

```brightscript
function getServerUrl() as String
    return "http://192.168.3.10:6567"   ' ← your server IP and port
end function

function getApiKey() as String
    return "your-api-key-here"
end function
```

## Installation

**1. Enable Developer Mode on the Roku device**

On the Roku remote, press: Home ×3, Up ×2, Right, Left, Right, Left, Right. Follow the prompts to set a developer password.

**2. Install dependencies**

```bash
uv sync
```

**3. Build**

```bash
uv run build
```

This generates `roku_app.zip`.

**4. Deploy**

```bash
uv run deploy http://<roku-ip> <developer-password>
```

The channel will appear in the Roku channel list immediately.

## Backend API

The channel expects the server to expose:

```
GET /objects/{path}/
Authorization: Bearer {apiKey}
```

Response: a JSON array of objects with `name`, `path`, `type` (`"file"` or `"directory"`), and `streamFormat` (`mp4`, `mkv`, `hls`, `dash`, `mp3`, `mka`, `mks`).

Files are streamed directly from:

```
GET /objects/{path}
Authorization: Bearer {apiKey}
```
