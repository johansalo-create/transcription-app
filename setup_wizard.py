"""
First-launch setup wizard for Transcription app.
Checks dependencies and downloads the Whisper model.
"""
import os
import sys
import subprocess
import urllib.request
import rumps
from pathlib import Path
from config import MODEL_PATH, MODEL_URL, MODEL_DIR, WHISPER_CMD


def check_homebrew():
    """Check if Homebrew is installed."""
    return subprocess.run(["which", "brew"], capture_output=True).returncode == 0


def check_ffmpeg():
    """Check if ffmpeg is installed."""
    return subprocess.run(["which", "ffmpeg"], capture_output=True).returncode == 0


def check_whisper():
    """Check if whisper-cli is installed."""
    return WHISPER_CMD is not None


def check_model():
    """Check if the Whisper model is downloaded."""
    return MODEL_PATH.exists() and MODEL_PATH.stat().st_size > 100_000_000


def download_model(progress_callback=None):
    """Download the Whisper model."""
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    
    def report_progress(block_num, block_size, total_size):
        if progress_callback and total_size > 0:
            percent = min(100, block_num * block_size * 100 // total_size)
            progress_callback(percent)
    
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH, reporthook=report_progress)


def run_setup():
    """Run the setup wizard and return True if setup is complete."""
    issues = []
    
    if not check_ffmpeg():
        issues.append("ffmpeg")
    
    if not check_whisper():
        issues.append("whisper-cli")
    
    if issues:
        msg = f"Missing dependencies: {', '.join(issues)}\n\n"
        msg += "Install them with Homebrew:\n"
        msg += "brew install ffmpeg whisper-cpp"
        
        response = rumps.alert(
            title="Setup Required",
            message=msg,
            ok="Open Terminal",
            cancel="Quit"
        )
        
        if response == 1:  # OK clicked
            # Open Terminal with install command
            script = 'tell application "Terminal" to do script "brew install ffmpeg whisper-cpp"'
            subprocess.run(["osascript", "-e", script])
        return False
    
    if not check_model():
        response = rumps.alert(
            title="Download Whisper Model",
            message="The Whisper speech recognition model needs to be downloaded (~1.5 GB).\n\nThis only happens once.",
            ok="Download",
            cancel="Quit"
        )
        
        if response == 1:  # OK clicked
            # Show downloading notification
            rumps.notification(
                "Transcription",
                "Downloading Model",
                "This may take a few minutes..."
            )
            
            try:
                download_model()
                rumps.notification(
                    "Transcription",
                    "Download Complete",
                    "Whisper model is ready!"
                )
            except Exception as e:
                rumps.alert(
                    title="Download Failed",
                    message=f"Error downloading model: {e}\n\nPlease check your internet connection and try again."
                )
                return False
        else:
            return False
    
    return True


if __name__ == "__main__":
    # Test the setup
    print(f"Homebrew: {check_homebrew()}")
    print(f"ffmpeg: {check_ffmpeg()}")
    print(f"whisper-cli: {check_whisper()} ({WHISPER_CMD})")
    print(f"Model: {check_model()} ({MODEL_PATH})")
