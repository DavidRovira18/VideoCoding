import subprocess
import os

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

def create_comparison(video1_path, video2_path, output_path):
    #Start getting the video width
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width', '-of', 'default=noprint_wrappers=1:nokey=1', video1_path]
    result = subprocess.run(cmd,stdout=subprocess.PIPE) # Returns the dimensions of the video in format width x height

    output_width = 2 * int(result.stdout)

    cmd = [
        '-i', video1_path,
        '-i', video2_path,
        '-filter_complex', f'[0:v]pad=iw*2:ih[int];[int][1:v]overlay=W/2:0[vid]',
        '-map', '[vid]',
        '-c:v', 'libx264',
        '-crf', '23',
        '-preset', 'medium',
        output_path
    ]

    ffmpeg_command(cmd)
