import tkinter as tk
import customtkinter as ctk

from gui.home import Home
from profile import Profile

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")
NUM_OF_WINDOWS = 5


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window logic
        self.screens = [True, False, False, False, False]
        self.user = None
        self.uid = None
        self.NUM_DATA = 5
        self.generated_data = [True, False, False, False, False]

        # Configure window
        self.title("UVa Judge")
        self.geometry(f"{1100}x{500}")

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure((0, 1), weight=1)

        # Creating sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)
        self.sidebar_logo = ctk.CTkLabel(self.sidebar_frame, text="UVa online judge")
        self.sidebar_logo.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_home_button = ctk.CTkButton(self.sidebar_frame, command=self.home_event, text="Home")
        self.sidebar_home_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.sidebar_profile = ctk.CTkButton(self.sidebar_frame, command=self.profile_event, text="Profile")
        self.sidebar_profile.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.sidebar_problem = ctk.CTkButton(self.sidebar_frame, command=self.problem_event, text="Problem")
        self.sidebar_problem.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.sidebar_submit = ctk.CTkButton(self.sidebar_frame, command=self.submit_event, text="Submit")
        self.sidebar_submit.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.sidebar_settings = ctk.CTkButton(self.sidebar_frame, command=self.settings_event, text="Settings")
        self.sidebar_settings.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        Home(self)

    def home_event(self):
        if self.screens[0]:
            return
        else:
            self.clear()
            Home(self)
            for i in range(NUM_OF_WINDOWS):
                self.screens[i] = False
            self.screens[0] = True

    def profile_event(self):
        if self.screens[1]:
            return
        else:
            self.clear()
            Profile(self)
            for i in range(NUM_OF_WINDOWS):
                self.screens[i] = False
            self.screens[1] = True

    def problem_event(self):
        return

    def submit_event(self):
        return

    def settings_event(self):
        return

    def clear(self):
        widgets = self.winfo_children()

        for child in widgets:
            if child == self.sidebar_frame:
                continue
            else:
                child.destroy()
