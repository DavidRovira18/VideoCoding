import subprocess
import os
from yuv_histogram import extract_yuv_hist, package_video_hist


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

def trim_video(input_video, output_video, start, end):
    cmd_trim = ["-ss", start, "-to", end, "-i", input_video, "-c", "copy",
                output_video]  # Trim the first 9 seconds of the video
    ffmpeg_command(cmd_trim)
class BigBuckBunny:
    def show_mackroblocks_motion_vectors(self):
        cmd = ["-flags2", "+export_mvs", "-i", "BigBuckBunny_trim.mpeg", "-vf", "codecview=mv=pf+bf+bb", "BigBuckBunny_motion.mpeg"]
        ffmpeg_command(cmd)

    def create_BBB_container(self):
        input_video = "BigBuckBunny.mpeg"
        trimmed_video = "BigBuckBunny_trim50.mpeg"

        # Trim BBB 50-seconds
        trim_video(input_video, trimmed_video, "00:00:00", "00:00:50")

        # Audio MP3 mono track
        cmd_audio = ["-i", trimmed_video, "-ac", "1", "BBB_mono.mp3"]
        ffmpeg_command(cmd_audio)

        # Audio MP3 lower bit rate to 128kbps (previous 384kbps)
        cmd_low_bitrate = ["-i", trimmed_video, "-b:a", "128k", "BBB_128.mp3"]
        ffmpeg_command(cmd_low_bitrate)

        # Audio using aac codec
        cmd_aac = ["-i", trimmed_video, "-c:a", "aac", "BBB.aac"]
        ffmpeg_command(cmd_aac)

        # Package everything ina mp4 file
        cmd_mp4 = ["-i", trimmed_video, "-i", "BBB_mono.mp3", "-i", "BBB_128.mp3",
        "-i", "BBB.aac", "-map", "0:v", "-map", "1:a", "-map", "2:a",
        "-map", "3:a", "-c:v", "copy", "-c:a", "copy",
        "BigBuckBunny_packaged.mp4"]
        ffmpeg_command(cmd_mp4)

def read_MP4_tracks(file_path): # Prints the number of channels of an MP4 file
    process = subprocess.Popen(f"ffmpeg -i {file_path}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    channels = stderr.decode().count("Stream #0") # Count the number of streams the video have

    print(f"Number of streams in this MP4: {channels}")


if __name__ == "__main__":

    BBB = BigBuckBunny()

    if not os.path.exists("BigBuckBunny_trim.mpeg"): # If the trimmed video does not exist create it (to avoid creating it always and to not deliver the whole BBB.mpeg)
        trim_video("BigBuckBunny.mpeg","BigBuckBunny_trim.mpeg","00:00:00", "00:00:09")

    if not os.path.exists("BigBuckBunny_motion.mpeg"):
        BBB.show_mackroblocks_motion_vectors()

    if not os.path.exists("BigBuckBunny_packaged.mp4"):
        BBB.create_BBB_container()

    if os.path.exists("BigBuckBunny_packaged.mp4"):
        read_MP4_tracks("BigBuckBunny_packaged.mp4")

    if not os.path.exists("hist_BigBuckBunny_trim.mpeg"):
        extract_yuv_hist("BigBuckBunny_trim.mpeg")

    if not os.path.exists("BigBuckBunny_trim_hist_overlay.mpeg"):
        package_video_hist("BigBuckBunny_trim.mpeg")