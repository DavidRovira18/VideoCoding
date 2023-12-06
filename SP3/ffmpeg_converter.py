import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from tkinter import filedialog
from SP3 import ffmpeg_command


class MyGridLayout(GridLayout):
    # Init infinite keywords
    def __init__(self, **kwargs):
        super(MyGridLayout, self).__init__(**kwargs)

        # Init variables
        self.out_button = None
        self.convert_button = None
        self.file_path = None
        self.output_path = None
        self.label_in = None
        self.label_out = None

        # Set columns
        self.cols = 2

        # Add widgets
        self.in_button = Button(text="Click to select the video to convert!")
        self.in_button.bind(on_press=self.file_chooser)
        self.add_widget(self.in_button)

    def file_chooser(self,instance):
        self.file_path = filedialog.askopenfilename(title="Select a video",
                                               filetypes=[("Video", "*.mp4 *.mpeg")])

        if self.file_path:
            self.remove_widget(self.in_button)
            file = self.file_path.split("/")[-1]
            self.label_in = Label(text=file)
            self.add_widget(self.label_in)

            self.out_button = Button(text="Click to name the output video!")
            self.out_button.bind(on_press=self.save_file)
            self.add_widget(self.out_button)

    def save_file(self, instance):
        self.output_path = filedialog.asksaveasfilename(title="Save here",
                                                   filetypes=[("Video", "*.mp4 *.mpeg")])

        if self.output_path:
            output = self.output_path.split("/")[-1]
            self.remove_widget(self.out_button)
            self.label_out = Label(text=output)
            self.add_widget(self.label_out)

            self.cols = 1
            self.convert_button = Button(text="Click to convert")
            self.convert_button.bind(on_press=self.convert_video)
            self.add_widget(self.convert_button)

    def convert_video(self,instance):
        cmd = ["-i", f"{self.file_path}", f"{self.output_path}"]
        ffmpeg_command(cmd)

        self.remove_widget(self.label_in)
        self.remove_widget(self.label_out)
        self.remove_widget(self.convert_button)
        self.add_widget(InitialWindow())

class InitialWindow(GridLayout):
    def __init__(self, **kwargs):
        super(InitialWindow, self).__init__(**kwargs)

        self.cols = 1
        self.welcome = Button(text="Welcome, click to start!", font_size=20,  # Set the font size
            background_color=(0.2, 0.6, 1, 1),  size=(200, 100))

        # Bind the button
        self.welcome.bind(on_press=self.press_welcome)
        self.add_widget(self.welcome)

    def press_welcome(self, instance):
        self.remove_widget(self.welcome)

        self.add_widget(MyGridLayout())


class FFMPEGVideoConverter(App):
    def build(self):
        return InitialWindow()

if __name__ == "__main__":
    FFMPEGVideoConverter().run()