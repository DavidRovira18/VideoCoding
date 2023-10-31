from typing import List, Any
from tkinter import filedialog
import subprocess
import numpy as np


# TRANSLATOR FROM RGB TO YUV
def rgb_2_yuv(
        color_rgb):
    # Following the YUV to RGB conversion formulas from computer language
    # https://www.computerlanguage.com/results.php?definition=YUV%2FRGB+conversion+formulas
    r, g, b = color_rgb
    Y = 0.299 * r + 0.587 * g + 0.114 * b
    U = - 0.147 * r - 0.289 * g + 0.436 * b
    V = 0.615 * r - 0.515 * g - 0.1 * b
    color_yuv = [Y, U, V]
    return color_yuv


def yuv_2_rgb(
        color_yuv):
    # Following the YUV to RGB conversion formulas from computer language
    # https://www.computerlanguage.com/results.php?definition=YUV%2FRGB+conversion+formulas
    y, u, v = color_yuv
    R = y + 1.140 * v
    G = y - 0.395 * u - 0.581 * v
    B = y + 2.032 * u
    color_rgb = [R, G, B]
    return color_rgb


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


# USE FFMPEG TO REDUCE IMAGE SIZE
def reduce_image_size(scale_x, scale_y):
    file_path = filedialog.askopenfilename(title="Select an image",
                                           filetypes=[("Images", "*.jpg *.png *.jpeg")])
    # Open a file dialog to select the image to reduce size
    if file_path:
        output_path = filedialog.asksaveasfilename(title="Save here",
                                                   filetypes=[("JPEG Image", "*jpeg")])
        # Open a file dialog to select the path and name of the saved image
        output_path += ".jpeg"
        cmd = ["-i", f"{file_path}", "-vf", f"scale={scale_x}:{scale_y}", "-q:v", "2", f"{output_path}"]
        ffmpeg_command(cmd)


# READ THE BYTES OF A JPEG FILE IN SERPENTINE
def serpentine():
    file_path = filedialog.askopenfilename(title="Select an image",
                                           filetypes=[("JPEG Images", "*.jpeg")])
    if file_path:
        with open(file_path, 'rb') as data:
            image_data = data.read()


# IMAGE TO BLACK AND WHITE
def image_2_bw(comp_level=51):
    file_path = filedialog.askopenfilename(title="Select an image",
                                           filetypes=[("JPEG Images", "*.jpeg")])
    # Open a file dialog to select the image to convert to black and white
    if file_path:
        output_path = filedialog.asksaveasfilename(title="Save here",
                                                   filetypes=[("JPEG Image", "*jpeg")])
        # Open a file dialog to select the path and name of the saved b/w image
        output_path += ".jpeg"
        cmd = ["-i", f"{file_path}", "-vf", "format=gray", "-q:v", f"{comp_level}", f"{output_path}"]
        ffmpeg_command(cmd)


# RUN LENGTH ENCODING
def run_len_encoding(bytes_seq):
    run_len = ""
    repetitions = 1

    for i in range(1, len(bytes_seq)):
        if bytes_seq[i] == bytes_seq[i - 1]:  # Every time that the actual byte is the same as the one before we add one
            # repetition
            repetitions += 1

        else:  # If its different we add to the encoded sequence the last byte followed by the number of repetitions
            # it had
            run_len += bytes_seq[i - 1] + str(repetitions)
            repetitions = 1  # Reinitialize the repetitions counter

    run_len += bytes_seq[-1] + str(repetitions)  # For the last byte type

    return run_len


# DCT CLASS

class DCT:
    def __init__(self):
        pass

    def forward_dct(self, data):
        N = len(data)
        dct = [0.0] * N  # init a list of N coefficients
        for i in range(N):
            sum_dct = 0.0
            for j in range(N):
                sum_dct += data[j] * np.cos(np.pi / N * (j + 0.5) * i)
            dct[i] = sum_dct
        return dct

    def inverse_dct(self, data):
        N = len(data)
        inverse = [0.0] * N
        for i in range(N):
            sum_inverse = 0.5 * data[0]
            for j in range(1, N):
                sum_inverse += data[j] * np.cos(np.pi / N * i * (j + 0.5))
            inverse[i] = sum_inverse
        return inverse


# CONSOLE MENU AND ITS FUNCTIONALITIES
def show_menu():
    print("Video P1 David Rovira:")
    print("1. RGB to YUV converter")
    print("2. YUV to RGB converter")
    print("3. Resize an image using ffmpeg")
    print("4. Read bytes of a jpeg file in serpentine")
    print("5. Convert an image to black and white using ffmpeg")
    print("6. Run-Length encoding of a series of bytes")
    print("7. DCT Class")
    print("0. Exit")


def show_dct_menu():
    print("DCT CLASS")
    print("1. Forward DCT (convert to DCT)")
    print("2. Inverse DCT (decode DCT)")
    print("0. Return to menu")


def run_app():
    dct = DCT()  # initialize DCT class for later use
    exit_app = False
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
            menu_rgb_2_yuv()

        elif option == 2:
            menu_yuv_2_rgb()

        elif option == 3:
            menu_resize()

        elif option == 4:
            print("Functionality not working")

        elif option == 5:
            menu_image_2_bw()

        elif option == 6:
            menu_run_len_encoding()

        elif option == 7:
            run_dct_menu(dct)

        else:
            print("Wrong option :(")


def menu_rgb_2_yuv():
    r = float(input("Enter the R value: "))
    g = float(input("Enter the G value: "))
    b = float(input("Enter the B value: "))
    yuv = rgb_2_yuv([r, g, b])
    print("Your YUV color is", yuv)


def menu_yuv_2_rgb():
    y = float(input("Enter the Y value: "))
    u = float(input("Enter the U value: "))
    v = float(input("Enter the V value: "))
    rgb = yuv_2_rgb([y, u, v])
    print("Your YUV color is", rgb)


def menu_resize():
    scale_x = int(input("Enter the scale in the x dimension: "))
    scale_y = int(input("Enter the scale in the y dimension: "))
    reduce_image_size(scale_x, scale_y)
    print("Image saved in the chosen directory")


def menu_image_2_bw():
    comp_value = input("Enter the compression level (0-51). Enter for default compression (Hardest Compression): ")
    image_2_bw(int(comp_value)) if comp_value else image_2_bw()
    print(f"Image converted to black and white with a compression level of {comp_value}")


def menu_run_len_encoding():
    bytes_seq = input("Enter the series of bytes: ")
    print(run_len_encoding(bytes_seq))


def run_dct_menu(dct):
    exit_dct = False
    while not exit_dct:
        show_dct_menu()

        option = input("Select an option: ")
        try:
            option = int(option)
        except:
            option = option

        if option == 0:
            exit_dct = True

        elif option == 1:
            menu_dct_forward(dct)

        elif option == 2:
            menu_dct_inverse(dct)


def menu_dct_forward(dct):
    input_data = input("Enter the data you want to code using DCT. Use format(x1,x2,x3,...,xn): ")
    try:
        data = [float(x) for x in input_data.split(",")]
    except:
        print("Format not correct!")
        return

    forward_dct = dct.forward_dct(data)
    print("DCT coding result: ", forward_dct)
    decode = input("Do you want to decode ? Y/N: ")
    if decode == "Y" or decode == "y":
        menu_dct_inverse(dct, forward_dct)

    elif decode == "N" or decode == "n":
        return

    else:
        print("Not valid input :(")


def menu_dct_inverse(dct, data=""):
    if not data:
        input_data = input("Enter the data you want to decode using DCT. Use format(x1,x2,x3,...,xn")
        try:
            data = [float(x) for x in input_data.split(",")]
        except:
            print("Format not correct!")
            return

    inverse_dct = dct.inverse_dct(data)
    print("DCT decoding result: ", inverse_dct)


# APP
run_app()
