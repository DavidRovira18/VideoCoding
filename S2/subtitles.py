import subprocess


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

def integrate_subtitles(video_file, subtitles_file): # Adds subtitles to the desired video file
    output_file = video_file.split(".")[0]
    output_file += "_srt.mpeg"
    cmd = ["-i", video_file, "-vf", f"subtitles={subtitles_file}", output_file]
    ffmpeg_command(cmd)