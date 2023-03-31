import customtkinter as ctk


class Home:
    def __init__(self, master):
        master.title("UVa Judge | Home")

        master.home_label = ctk.CTkLabel(master, text="Welcome to the UVa Judge app")
        master.home_label.config(font=("Arial", 20, "bold"))
        master.home_label.grid(row=0, column=1, padx=20, pady=10, sticky="n")
        master.home_text = ctk.CTkLabel(master, text="To use the app, please refer to the README file of the repo. As "
                                                     "starters, you should try login to your UVa account and coding a "
                                                     "problem!", wraplength=800)
        master.home_text.config(font=("Arial", 14))
        master.home_text.grid(row=1, column=1, padx=20, pady=20, sticky="n")
