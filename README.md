# Transcription

A macOS menu bar app that automatically transcribes your Voice Memos using Whisper AI.

## Features

- **Automatic transcription** - Watches your Voice Memos folder and transcribes new recordings
- **System audio recording** - Record Teams/Zoom calls and other system audio for transcription
- **Multi-language support** - Auto-detect, Swedish, or English
- **Web interface** - Browse and search all transcripts at http://localhost:5051
- **Multi-select copy** - Select multiple transcripts and copy them all at once
- **Menu bar access** - Quick access to recent transcripts from the menu bar

## Requirements

- macOS 12.0 or later
- [Homebrew](https://brew.sh)

## Installation

### 1. Install dependencies

```bash
brew install ffmpeg whisper-cpp
```

### 2. Install Python packages

```bash
pip3 install -r requirements.txt
```

### 3. Run the app

```bash
python3 transcription_app.py
```

On first launch, the app will download the Whisper model (~1.5 GB).

## Usage

1. Click the 🎙️ icon in your menu bar
2. Click "Start Service" to begin watching for new Voice Memos
3. Record a voice memo on your iPhone (syncs via iCloud)
4. The transcript appears automatically in the web UI

### Language Setting

Select your preferred language from the menu:
- **Auto** - Automatically detect the language
- **Svenska** - Force Swedish transcription
- **English** - Force English transcription

### Web Interface

Open http://localhost:5051 to:
- Search all transcripts
- Sort by recording date or transcription date
- Select multiple transcripts and copy them together

### System Audio Recording (for Teams/Zoom calls)

To record system audio (e.g., from video calls), you need to set up BlackHole:

1. **Install BlackHole:**
   ```bash
   brew install blackhole-2ch
   ```

2. **Create a Multi-Output Device:**
   - Open "Audio MIDI Setup" (search in Spotlight)
   - Click "+" at bottom left → "Create Multi-Output Device"
   - Check both your speakers AND "BlackHole 2ch"
   - Right-click the Multi-Output Device → "Use This Device For Sound Output"

3. **Record:**
   - Click "Record System Audio" in the menu bar app
   - The icon changes to 🔴 while recording
   - Click "Stop Recording" when done
   - The recording is automatically transcribed

## Data Storage

All data is stored in `~/Library/Application Support/Transcription/`:
- `transcripts/` - Text files of transcriptions
- `db/` - SQLite database
- `models/` - Whisper model files
- `input/` - Drop folder for manual audio files

## Building the App Bundle

To create a standalone .app:

```bash
pip3 install py2app
python3 setup.py py2app
```

The app will be created in the `dist/` folder.

## License

MIT
