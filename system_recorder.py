"""
System audio recorder using BlackHole virtual audio device.
Records both system audio and microphone input.
"""
import subprocess
import threading
import time
from pathlib import Path
from datetime import datetime
from config import INPUT_DIR


def check_blackhole_installed():
    """Check if BlackHole audio device is available."""
    result = subprocess.run(
        ["system_profiler", "SPAudioDataType"],
        capture_output=True, text=True
    )
    return "BlackHole" in result.stdout


def get_blackhole_device():
    """Get the BlackHole device name."""
    result = subprocess.run(
        ["system_profiler", "SPAudioDataType"],
        capture_output=True, text=True
    )
    # Look for BlackHole 2ch or BlackHole 16ch
    if "BlackHole 2ch" in result.stdout:
        return "BlackHole 2ch"
    elif "BlackHole 16ch" in result.stdout:
        return "BlackHole 16ch"
    elif "BlackHole" in result.stdout:
        return "BlackHole"
    return None


def check_multi_output_exists():
    """Check if a Multi-Output Device is configured."""
    result = subprocess.run(
        ["system_profiler", "SPAudioDataType"],
        capture_output=True, text=True
    )
    return "Multi-Output Device" in result.stdout


class SystemRecorder:
    """Records system audio using ffmpeg and BlackHole."""
    
    def __init__(self):
        self.process = None
        self.is_recording = False
        self.output_file = None
        self.start_time = None
    
    def start_recording(self, filename=None):
        """Start recording system audio."""
        if self.is_recording:
            return False, "Already recording"
        
        blackhole_device = get_blackhole_device()
        if not blackhole_device:
            return False, "BlackHole not installed"
        
        # Generate filename
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d %H%M%S")
            filename = f"{timestamp}-system.m4a"
        
        self.output_file = INPUT_DIR / filename
        INPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # Record using ffmpeg from BlackHole device
        # Use avfoundation to capture from BlackHole
        self.process = subprocess.Popen([
            "ffmpeg",
            "-f", "avfoundation",
            "-i", f":{blackhole_device}",  # Audio only from BlackHole
            "-c:a", "aac",
            "-b:a", "128k",
            "-y",  # Overwrite output
            str(self.output_file)
        ], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        self.is_recording = True
        self.start_time = time.time()
        return True, str(self.output_file)
    
    def stop_recording(self):
        """Stop recording and return the output file path."""
        if not self.is_recording or not self.process:
            return None, "Not recording"
        
        # Send 'q' to ffmpeg to stop gracefully
        try:
            self.process.stdin.write(b'q')
            self.process.stdin.flush()
        except:
            pass
        
        # Wait for process to finish
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.terminate()
        
        self.is_recording = False
        duration = time.time() - self.start_time
        output = self.output_file
        
        self.process = None
        self.output_file = None
        self.start_time = None
        
        return output, f"Recorded {duration:.1f} seconds"
    
    def get_duration(self):
        """Get current recording duration in seconds."""
        if self.is_recording and self.start_time:
            return time.time() - self.start_time
        return 0


def show_blackhole_setup_instructions():
    """Return instructions for setting up BlackHole."""
    return """To record system audio, you need to set up BlackHole:

1. Install BlackHole:
   brew install blackhole-2ch

2. Create a Multi-Output Device:
   - Open "Audio MIDI Setup" (search in Spotlight)
   - Click "+" at bottom left → "Create Multi-Output Device"
   - Check both your speakers AND "BlackHole 2ch"
   - Right-click the Multi-Output Device → "Use This Device For Sound Output"

3. Now your system audio will go to both speakers AND BlackHole (for recording)

After setup, restart this app and try recording again."""


if __name__ == "__main__":
    # Test
    print(f"BlackHole installed: {check_blackhole_installed()}")
    print(f"BlackHole device: {get_blackhole_device()}")
    print(f"Multi-Output exists: {check_multi_output_exists()}")
