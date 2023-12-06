import subprocess
import os
from comparison import create_comparison

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

def modify_video_res(
    file_path, width, height, output_path): # Modifies the resolution of a video using ffmpeg

    cmd = ["-i", f"{file_path}", "-vf", f"scale={width}:{height}", f"{output_path}"] # Command to change video resolution
    ffmpeg_command(cmd)

class VideoConverter:
    def __init__(self, input_path):
        self.input_path = input_path
        self.output_path = input_path.split(".")[0]


    def convert_2_vp9(self):
        output_file = self.output_path + '_vp9.mp4'
        cmd = [
            '-i', self.input_path,
            '-c:v', 'libvpx-vp9',
            output_file
        ]
        ffmpeg_command(cmd)

    def convert_2_h265(self):
        output_file = self.output_path + '_h265.mp4'
        cmd = [
            '-i', self.input_path,
            '-c:v', 'libx265',
            output_file
        ]
        ffmpeg_command(cmd)


    def perform_conversions(self):
        self.convert_2_vp9()
        self.convert_2_h265()

if __name__ == "__main__":

    if not os.path.exists("BigBuckBunny_720.mpeg"):
        modify_video_res("BigBuckBunny_trim.mpeg", 1280, 720, "BigBuckBunny_720.mpeg")

    if not os.path.exists("BigBuckBunny_480.mpeg"):
        modify_video_res("BigBuckBunny_trim.mpeg", 640, 480, "BigBuckBunny_480.mpeg")

    if not os.path.exists("BigBuckBunny_360.mpeg"):
        modify_video_res("BigBuckBunny_trim.mpeg", 360, 240, "BigBuckBunny_360.mpeg")

    if not os.path.exists("BigBuckBunny_160.mpeg"):
        modify_video_res("BigBuckBunny_trim.mpeg", 160, 120, "BigBuckBunny_160.mpeg")

    if not os.path.exists("BigBuckBunny_720_vp9.mp4") or not os.path.exists("BigBuckBunny_720_h265.mp4"):
        vc_720 = VideoConverter("BigBuckBunny_720.mpeg")
        vc_720.perform_conversions()

    if not os.path.exists("BigBuckBunny_480_vp9.mp4") or not os.path.exists("BigBuckBunny_480_h265.mp4"):
        vc_480 = VideoConverter("BigBuckBunny_480.mpeg")
        vc_480.perform_conversions()

    if not os.path.exists("BigBuckBunny_360_vp9.mp4") or not os.path.exists("BigBuckBunny_360_h265.mp4"):
        vc_360 = VideoConverter("BigBuckBunny_360.mpeg")
        vc_360.perform_conversions()

    if not os.path.exists("BigBuckBunny_160_vp9.mp4") or not os.path.exists("BigBuckBunny_160_h265.mp4"):
        vc_160 = VideoConverter("BigBuckBunny_160.mpeg")
        vc_160.perform_conversions()

    if not os.path.exists("BigBuckBunny_720_comparison.mp4"):
        create_comparison("BigBuckBunny_720_h265.mp4", "BigBuckBunny_720_vp9.mp4", "BigBuckBunny_720_comparison.mp4")




