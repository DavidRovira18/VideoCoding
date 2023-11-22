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

def extract_yuv_hist(video_file): # Creates a video file with the YUV histogram of the input video file
    cmd = ["-i", video_file, "-vf", "histogram", f"hist_{video_file}"]
    ffmpeg_command(cmd)

def package_video_hist(video_file): # Creates a video container with the YUV histogram overlay in the input video file
    output_file = video_file.split(".")[0]
    output_file += "_hist_overlay.mpeg"
    cmd = ["-i", video_file, "-vf", "split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay", output_file]
    ffmpeg_command(cmd)