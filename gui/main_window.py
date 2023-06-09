import linecache
import os
from tkinter import ttk
import customtkinter as ctk

from home import Home
from problem import Problem
from setting import Settings
from profile import Profile

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")
NUM_OF_WINDOWS = 4


def load_user():
    if not os.path.exists("resources//config.conf"):
        return None, None

    usr = linecache.getline("resources//config.conf", 3, module_globals=None)
    if usr == "" or usr == "None\n":
        return None, None

    return usr.strip(), int(linecache.getline("resources//config.conf", 4, module_globals=None).strip())


def load_data():
    if not os.path.exists("resources//config.conf"):
        return 5

    data = linecache.getline("resources//config.conf", 2, module_globals=None)
    if data == "" or data == "None\n":
        return 5

    return int(data.strip())


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window logic
        self.screens = [True, False, False, False]
        self.user, self.uid = load_user()
        self.num_data = load_data()
        self.generated_data = [True, False, False, False]
        self.pid = None
        self.temp = []
        self.prob_data = None
        self.usr_data = None
        self.rank_data = None
        self.uprob_data = None

        theme = linecache.getline("resources//config.conf", 1, module_globals=None)
        if theme != "":
            ctk.set_appearance_mode(theme.strip())

        # Configure window
        self.title("UVa Judge")
        self.geometry(f"{1100}x{500}")
        self.protocol("WM_DELETE_WINDOW", self.cleanup)
        self.resizable(0, 0)

        self.style = ttk.Style(self)
        self.style.configure("Treeview.Heading", font=("Arial", 18, "bold"))
        self.style.configure("Treeview", font=("Arial", 16))
        ttk.Style()

        self.style.theme_use("default")

        self.style.configure("Treeview",
                             background="#2a2d2e",
                             foreground="white",
                             rowheight=25,
                             fieldbackground="#343638",
                             bordercolor="#343638",
                             borderwidth=0)
        self.style.map('Treeview', background=[('selected', '#22559b')])

        self.style.configure("Treeview.Heading",
                             background="#565b5e",
                             foreground="white",
                             relief="flat")
        self.style.map("Treeview.Heading",
                       background=[('active', '#3484F0')])

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure((0, 1), weight=1)

        # Creating sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.sidebar_logo = ctk.CTkLabel(self.sidebar_frame, text="UVa online judge")
        self.sidebar_logo.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_home_button = ctk.CTkButton(self.sidebar_frame, command=self.home_event, text="Home")
        self.sidebar_home_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.sidebar_profile = ctk.CTkButton(self.sidebar_frame, command=self.profile_event, text="Profile")
        self.sidebar_profile.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.sidebar_problem = ctk.CTkButton(self.sidebar_frame, command=self.problem_event, text="Problem")
        self.sidebar_problem.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.sidebar_settings = ctk.CTkButton(self.sidebar_frame, command=self.settings_event, text="Settings")
        self.sidebar_settings.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        Home(self)

    def home_event(self):
        self.clear()
        Home(self)
        for i in range(NUM_OF_WINDOWS):
            self.screens[i] = False
        self.screens[0] = True

    def profile_event(self):
        self.clear()
        Profile(self)
        for i in range(NUM_OF_WINDOWS):
            self.screens[i] = False
        self.screens[1] = True

    def problem_event(self):
        self.clear()
        Problem(self)
        for i in range(NUM_OF_WINDOWS):
            self.screens[i] = False
        self.screens[2] = True

    def settings_event(self):
        if self.screens[3]:
            return
        else:
            self.clear()
            Settings(self)
            for i in range(NUM_OF_WINDOWS):
                self.screens[i] = False
            self.screens[3] = True

    def clear(self):
        widgets = self.winfo_children()

        for child in widgets:
            if child == self.sidebar_frame:
                continue
            else:
                child.destroy()

    def cleanup(self):
        with open(r'resources//config.conf', 'w') as f:
            f.writelines([str(ctk.get_appearance_mode()), "\n" + str(self.num_data),
                          "\n" + str(self.user), "\n" + str(self.uid)])

        for f in self.temp:
            os.remove(f)
        self.destroy()
