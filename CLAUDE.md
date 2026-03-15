# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

- **Build:** `uv run build` — generates images and packages the app into `roku_app.zip`
- **Deploy:** `uv run deploy <roku-url> <password>` — deploys to a Roku device via HTTP Digest auth (`rokudev` / password)

No lint or test infrastructure exists in this project.

## Architecture

This is a Roku SceneGraph channel (streaming app for Roku TVs) written in BrightScript with XML component definitions. It browses and streams media from a backend server at a hardcoded URL/API key in `source/config.brs`.

### Request & Data Flow

1. `source/main.brs` launches the channel, creates the SceneGraph screen, and enters a message loop waiting for `roSGScreenEvent` close.
2. `components/SimpleVideoScene.xml` + `.brs` is the main scene. On `init()` it starts `FetchFilesTask` with `path=""` (root), then observes four fields: `fetcher.status`, `fileList.itemSelected`, `video.state`, and `warning.buttonSelected`.
3. `components/FetchFilesTask.xml` is a Task component (background thread) that GETs `{serverUrl}/objects/{path}/` with a Bearer token, parses the JSON array, sorts dirs before files, and writes results to `entries`/`status` fields.
4. When `fetcher.status` changes to `"done"`, `onFetchStatus()` builds a ContentNode tree and binds it to the MarkupList. Each row is rendered by `components/FileListItem.xml` + `.brs`.
5. On item selection, directories re-run `FetchFilesTask` with the new path; files call `playVideo()` which sets a ContentNode on the Video node with Bearer auth headers and `control = "play"`.
6. Back key: exits video player if playing, navigates to parent directory via string-parsed path, or exits the channel if at root.

### Key Patterns

- **SceneGraph observer pattern:** field changes on nodes trigger named BrightScript callbacks (`observeField`). This is the primary async mechanism — no promises or callbacks in the traditional sense.
- **Task threading:** `FetchFilesTask` sets `m.top.functionName = "fetchFiles"` in `init()`. Setting `control = "RUN"` on the task node starts it in a background thread; results are written to interface fields observed by the main thread.
- **ContentNode tree for lists:** `populateList()` dynamically creates a ContentNode tree where `TITLE` and `HDGRIDPOSTERURL` are the conventional field names read by `FileListItem`.
- **Navigation state:** there is no explicit path stack — `goToPath()` replaces the current path, and `getParentPath()` parses the string to go up.

### Build System

`build.py` runs three generators before zipping:
1. `generate_icons()` — renders Tabler icons (folder, video, audio, file) as white PNGs via `pytablericons`
2. `generate_placeholders()` — renders channel poster and splash screen images with text
3. `generate_logo()` — renders "Media Browser" white text on transparent PNG for the Overhang `logoUri`

The zip excludes `.git`, `.venv`, `__pycache__`, `.pyc` files, and the build/deploy scripts themselves.
