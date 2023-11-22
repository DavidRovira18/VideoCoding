import subprocess
from tkinter import filedialog


def ffmpeg_command(
        commands):  # Executes a ffmpeg command when using a Python WSL interpreter
    try:
        result = subprocess.run(
            ["/usr/bin/ffmpeg"] + commands,  # FFMPEG path + commands
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"OUTPUT ERROR: {e.stderr}")
        return

