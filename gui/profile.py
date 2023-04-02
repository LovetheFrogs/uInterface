import customtkinter as ctk
import u_interface as ui
from tkinter import ttk
import tkinter as tk


def login(master):
    master.user = master.login_form.get()
    master.uid = ui.get_uid(master.user)
    if master.uid == 0:
        master.user = None
        master.login_label.configure(text="Invalid UVa username, try again")
    else:
        master.clear()
        Profile(master)


def get_prob_display(data):
    prob = ui.get_problem_pid(data)
    return f'{prob["num"]} - {prob["title"]}'


def get_lang_display(data):
    values = {1: "C", 2: "Java", 3: "C++", 4: "Pascal", 5: "C++11"}

    return values[data]


def get_verdict_display(data):
    values = {10: "SE", 15: "CBJ", 20: "QUEUED", 30: "CE", 35: "RF", 40: "RE", 50: "TLE", 60: "MLE", 70: "WA",
              80: "PE", 90: "AC"}

    return values[data]


def build_submission_table(master):
    if master.usr_data is None:
        master.usr_data = ui.get_user_submissions(master.uid, master.num_data)
    data = master.usr_data["subs"]

    canvas = ctk.CTkCanvas(master)
    scroll = ctk.CTkScrollbar(canvas, orientation="vertical")
    master.table = ttk.Treeview(canvas, columns=("Problem", "Verdict", "Lang", "Time"), show="headings",
                                displaycolumns=(0, 1, 2, 3))
    master.table.heading("Problem", text="Problem")
    master.table.heading("Verdict", text="Verdict")
    master.table.heading("Lang", text="Lang")
    master.table.heading("Time", text="Time")
    master.table.column("Problem", width=300, anchor="center")
    master.table.column("Verdict", width=100, anchor="center")
    master.table.column("Lang", width=100, anchor="center")
    master.table.column("Time", width=100, anchor="center")
    master.table.config(height=master.num_data)

    for item in reversed(data):
        prob_disp = get_prob_display(item[1])
        verd_disp = get_verdict_display(item[2])
        lang_disp = get_lang_display(item[5])
        time_disp = f'{item[3]} ms'

        if verd_disp == "AC":
            verd_bg = "#B3E6CC"  # pastel green
        elif verd_disp == "PE":
            verd_bg = "#FFCC99"  # pastel orange
        elif verd_disp == "WA":
            verd_bg = "#FF9999"  # pastel red
        elif verd_disp == "TLE":
            verd_bg = "#B3B3E6"  # pastel blue
        elif verd_disp == "MLE":
            verd_bg = "#99CCFF"  # pastel sky blue
        elif verd_disp == "CE":
            verd_bg = "#FFFF99"  # pastel yellow
        elif verd_disp == "RE":
            verd_bg = "#9999FF"  # pastel purple
        else:
            verd_bg = "#E6E6E6"  # pastel gray

        master.table.insert("", "end", values=(prob_disp, verd_disp, lang_disp, time_disp), tags=verd_bg)

    master.table.tag_configure("#B3E6CC", background="#B3E6CC", foreground="black")
    master.table.tag_configure("#FFCC99", background="#FFCC99", foreground="black")
    master.table.tag_configure("#FF9999", background="#FF9999", foreground="black")
    master.table.tag_configure("#B3B3E6", background="#B3B3E6", foreground="black")
    master.table.tag_configure("#99CCFF", background="#99CCFF", foreground="black")
    master.table.tag_configure("#FFFF99", background="#FFFF99", foreground="black")
    master.table.tag_configure("#9999FF", background="#9999FF", foreground="black")
    master.table.tag_configure("#E6E6E6", background="#E6E6E6", foreground="black")
    master.table.configure(height=5, yscrollcommand=scroll.set)
    master.table.grid(row=0, rowspan=5, column=0, columnspan=4, sticky="nsew")

    scroll.configure(command=master.table.yview)
    scroll.grid(row=0, column=4, rowspan=5, sticky="ns")

    canvas.grid(row=2, column=1, rowspan=1, padx=20, pady=10)
    canvas.configure(height=master.table.winfo_reqheight() + master.table.winfo_reqheight() // 5, width=master.table.
                     winfo_reqwidth() + scroll.winfo_reqwidth())
    canvas.grid_propagate(False)


def build_ranking_table(master):
    if master.rank_data is None:
        master.rank_data = ui.get_ranking(master.uid, master.num_data // 2, master.num_data // 2)

    canvas = ctk.CTkCanvas(master)
    scroll = ctk.CTkScrollbar(canvas, orientation="vertical")
    master.table2 = ttk.Treeview(canvas, columns=("Rank", "Username", "AC", "Subs"), show="headings",
                                 displaycolumns=(0, 1, 2, 3))
    master.table2.heading("Rank", text="Rank")
    master.table2.heading("Username", text="Username")
    master.table2.heading("AC", text="AC")
    master.table2.heading("Subs", text="Subs")
    master.table2.column("Rank", width=100, anchor="center")
    master.table2.column("Username", width=300, anchor="center")
    master.table2.column("AC", width=100, anchor="center")
    master.table2.column("Subs", width=100, anchor="center")
    master.table2.config(height=master.num_data)

    for item in master.rank_data:
        if item["username"] == master.user:
            bg_color = "#D3D3D3"  # darker grey
        else:
            bg_color = "white"
        master.table2.insert("", "end", values=(item["rank"], item["username"], item["ac"], item["nos"]), tags=bg_color)

    master.table2.tag_configure("#D3D3D3", background="#D3D3D3", foreground="black")
    master.table2.configure(height=5, yscrollcommand=scroll.set)
    master.table2.grid(row=0, rowspan=5, column=0, columnspan=4, sticky="nsew")

    scroll.configure(command=master.table2.yview)
    scroll.grid(row=0, column=4, rowspan=5, sticky="ns")

    canvas.grid(row=3, column=1, rowspan=1, padx=20, pady=10)
    canvas.configure(height=master.table2.winfo_reqheight() + master.table2.winfo_reqheight() // 5,
                     width=master.table2.winfo_reqwidth() + scroll.winfo_reqwidth())
    canvas.grid_propagate(False)


def logout(master):
    master.user = None
    master.clear()
    Profile(master)


class Profile:
    def __init__(self, master):
        master.title("UVa Judge | Profile")
        if master.user is None:
            master.login_label = ctk.CTkLabel(master, text="Login to your UVa account")
            master.login_label.configure(font=("Arial", 20, "bold"))
            master.login_label.grid(row=0, column=1, padx=20, pady=10, sticky="n")
            master.login_form = ctk.CTkEntry(master, placeholder_text="UVa username")
            master.login_form.grid(row=0, column=1, padx=10, pady=10, sticky="ne")
            master.login_btn = ctk.CTkButton(master, text="Log In", command=lambda: login(master))
            master.bind('<Return>', lambda x: login(master))
            master.login_btn.grid(row=0, column=2, padx=10, pady=10, sticky="nw")
        else:
            master.welcome_label = ctk.CTkLabel(master, text=f'Welcome {master.user}!')
            master.welcome_label.configure(font=("Arial", 20, "bold"))
            master.welcome_label.grid(row=0, column=1, padx=20, pady=10, sticky="n")

            master.logout = ctk.CTkButton(master, text="Logout", command=lambda: logout(master))
            master.logout.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

            master.sub_label = ctk.CTkLabel(master, text="Your last submissions & ranking position")
            master.sub_label.configure(font=("Arial", 18, "bold"))
            master.sub_label.grid(row=1, column=1, padx=20, pady=10)
            build_submission_table(master)
            build_ranking_table(master)
