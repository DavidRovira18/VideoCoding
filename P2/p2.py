from typing import List, Any
from tkinter import filedialog
import subprocess
import numpy as np
import sys
sys.path.append('../P1')
from rgb_yuv import DCT, show_dct_menu, run_dct_menu, menu_dct_forward, menu_dct_inverse

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

def mp4_2_mpeg(
        file_path="", output_path=""): # Converts an mp4 video to a mpeg one.

    if file_path == "":

        file_path = filedialog.askopenfilename(title="Select a video",
                                           filetypes=[("MP4 Video", "*.mp4")])

    if file_path:
        if output_path == "":
            output_path = filedialog.asksaveasfilename(title="Save here",
                                                   filetypes=[("MPEG Video", "*.mpeg")])

        cmd = ["-i", f"{file_path}", f"{output_path}"]
        ffmpeg_command(cmd)

def video_info(): # Save the info of a video in a txt file
    file_path = filedialog.askopenfilename(title="Select a video",
                                           filetypes=[("Video", "*.mp4 *.mpeg")])

    if file_path:
        output_path = filedialog.asksaveasfilename(title="Save here",
                                                   filetypes=[("TXT File", "*.txt")])

        process = subprocess.Popen( f"ffmpeg -i {file_path}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        with open(f"{output_path}", "w") as info:
            info.write(stderr.decode()) # Error because ffmpeg returns an error if we dont give an output video path.

def modify_video_res(
        width, height): # Modifies the resolution of a video using ffmpeg
    file_path = filedialog.askopenfilename(title="Select a video",
                                           filetypes=[("Video", "*.mp4 .*mpeg")])

    if file_path:
        output_path = filedialog.asksaveasfilename(title="Save here",
                                                       filetypes=[("Video", "*.mp4 *.mpeg")])

        cmd = ["-i", f"{file_path}", "-vf", f"scale={width}:{height}", f"{output_path}"] # Command to change video resolution
        ffmpeg_command(cmd)

def modify_video_chroma_sub(
        chroma_sub_option): # Modifies the video chroma subsampling with the desired one
    file_path = filedialog.askopenfilename(title="Select a video",
                                           filetypes=[("Video", "*.mp4 .*mpeg")])

    if file_path:
        output_path = filedialog.asksaveasfilename(title="Save here",
                                                   filetypes=[("Video", "*.mp4 *.mpeg")])

        if chroma_sub_option == 1:
            chroma_sub = "yuv420p"
        elif chroma_sub_option == 2:
            chroma_sub = "yuv422p"
        else:
            chroma_sub = "yuv444p"
        cmd = ["-i", f"{file_path}", "-pix_fmt", f"{chroma_sub}", f"{output_path}"]
        ffmpeg_command(cmd)

def video_info_from_txt(): # Reads the info from a txt file created with the video_info method
    file_path = filedialog.askopenfilename(title="Select a video info file",
                                           filetypes=[("TXT File", "*.txt")])
    if file_path:
        with open(file_path, "r") as text_file:
            info = text_file.read()

        start = info.find("Metadata:") # Word where the video info starts
        end = info.find("At") # Word where the video info ends
        if start != -1 and end != -1:
            valuable_info = info[start:end].strip()
            print(valuable_info)
        else:
            print("Info TXT has not the correct format, make sure you create the file using the option number 2")



def show_menu():
    print("Video P2 David Rovira :)")
    print("1. Convert MP4 Video to MPEG")
    print("2. Save Video Info to TXT File")
    print("3. Modify Video Resolution")
    print("4. Modify Chroma Subsampling of a Video")
    print("5. Read Video Info from TXT File")
    print("6. DCT Class")

def menu_video_resolution():
    try:
        width = int(input("Enter the width: "))
        height = int(input("Enter the height: "))
        reduce_image_size(width, height)
    except:
        print('Not a valid input for width and/or height')

def menu_chroma_video():
    print("1. 4:2:0")
    print("2. 4:2:2")
    print("3. 4:4:4")

    try:
        chroma_sub = int(input("Choose the desired chroma subsampling from the above options: "))
        modify_video_chroma_sub(chroma_sub)
    except:
        print('Not a valid input for chroma subsampling')

def run_app():
    exit_app = False
    dct = DCT()
    while not exit_app:
        show_menu()

        option = input("Select an option: ")
        try:
            option = int(option)
        except:
            option = option

        if option == 0:
            print("Peace out! :)")
            exit_app = True

        elif option == 1:
            mp4_2_mpeg()

        elif option == 2:
            video_info()

        elif option == 3:
            menu_video_resolution()

        elif option == 4:
            menu_chroma_video()

        elif option == 5:
            video_info_from_txt()

        elif option == 6:
            run_dct_menu(dct)

        else:
            print("Wrong option :(")

if __name__ == "__main__":
    run_app()