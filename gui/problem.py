import platform
import subprocess
import webbrowser
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import customtkinter as ctk
import u_interface as ui
import urllib.request
import tempfile

from gui.profile import get_verdict_display, get_lang_display


def search(master):
    if master.search_form.get() == '':
        return

    if master.pid != int(master.search_form.get()) or master.pid is None:
        master.prob_data = ui.get_problem(int(master.search_form.get()))
        master.pid = master.prob_data["num"]
        master.clear()
        Problem(master)


def draw_graph(master):
    problem_submissions = {
        'AC': master.prob_data["ac"],
        'PE': master.prob_data["pe"],
        'WA': master.prob_data["wa"],
        'TLE': master.prob_data["tle"],
        'MLE': master.prob_data["mle"],
        'CE': master.prob_data["ce"],
        'RE': master.prob_data["re"],
        'OT': master.prob_data["sube"] + master.prob_data["rf"] + master.prob_data["nover"] + master.prob_data["ole"],
    }

    submission_types = list(problem_submissions.keys())
    submission_counts = list(problem_submissions.values())

    fig = Figure(figsize=(4, 3), dpi=100, facecolor='none')
    fig.patch.set_alpha(0)
    ax = fig.add_subplot(111)

    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.tick_params(axis='y', which='both', length=0)

    colors = ["#00aa00", "#666600", "#ff0000", "#0000ff", "#2c2cb6", "#aaaa00", "#00aaaa", "#000000"]
    bars = ax.bar(submission_types, submission_counts, color=colors, width=0.6, alpha=0.7)

    ax.set_title('Submissions Statistics', fontsize=14)

    for i, bar in enumerate(bars):
        ax.text(bar.get_x() + bar.get_width() / 2.0, bar.get_height() + 0.1,
                str(submission_counts[i]), ha='center', va='bottom', color=colors[i])

    ax.tick_params(axis='both', which='major', labelsize=10, pad=8)
    ax.set_yticklabels([])

    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()
    canvas.get_tk_widget().grid(row=2, column=1, padx=20, pady=(10, 20), sticky="w")


def open_web(master):
    webbrowser.open(
        "https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=submit_problem&problemid"
        "=" + str(master.prob_data["pid"]) + "&category=0")


def draw_submissions(master):
    if master.user is None:
        return

    master.uprob_data = ui.get_usubs_problem(master.uid, master.prob_data["pid"], master.num_data)
    data = master.uprob_data[master.uid]["subs"]

    if not data:
        master.not_tried_label = ctk.CTkLabel(master, text="Make a submission to see rank")
        master.not_tried_label.configure(font=("Arial", 16, "bold"))
        master.not_tried_label.grid(row=2, column=1, padx=10, pady=10, sticky="e")

        return

    canvas = ctk.CTkCanvas(master)
    scroll = ctk.CTkScrollbar(canvas, orientation="vertical")
    master.table3 = ttk.Treeview(canvas, columns=("Rank", "Verdict", "Lang", "Time"), show="headings",
                                 displaycolumns=(0, 1, 2, 3))
    master.table3.heading("Rank", text="Rank")
    master.table3.heading("Verdict", text="Verdict")
    master.table3.heading("Lang", text="Lang")
    master.table3.heading("Time", text="Time")
    master.table3.column("Rank", width=100, anchor="center")
    master.table3.column("Verdict", width=100, anchor="center")
    master.table3.column("Lang", width=100, anchor="center")
    master.table3.column("Time", width=100, anchor="center")
    master.table3.config(height=master.num_data)

    for item in reversed(data):
        if item[6] == -1:
            rank = "-"
        else:
            rank = item[6]
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

        master.table3.insert("", "end", values=(rank, verd_disp, lang_disp, time_disp), tags=verd_bg)

    master.table3.tag_configure("#B3E6CC", background="#B3E6CC", foreground="black")
    master.table3.tag_configure("#FFCC99", background="#FFCC99", foreground="black")
    master.table3.tag_configure("#FF9999", background="#FF9999", foreground="black")
    master.table3.tag_configure("#B3B3E6", background="#B3B3E6", foreground="black")
    master.table3.tag_configure("#99CCFF", background="#99CCFF", foreground="black")
    master.table3.tag_configure("#FFFF99", background="#FFFF99", foreground="black")
    master.table3.tag_configure("#9999FF", background="#9999FF", foreground="black")
    master.table3.tag_configure("#E6E6E6", background="#E6E6E6", foreground="black")
    master.table3.configure(height=5, yscrollcommand=scroll.set)
    master.table3.grid(row=0, rowspan=5, column=0, columnspan=3, sticky="nsew")

    scroll.configure(command=master.table3.yview)
    scroll.grid(row=0, column=4, rowspan=4, sticky="ns")

    canvas.grid(row=2, column=2, rowspan=1, padx=20, pady=10)
    canvas.configure(height=master.table3.winfo_reqheight() + master.table3.winfo_reqheight() // 5, width=master.table3.
                     winfo_reqwidth() + scroll.winfo_reqwidth())
    canvas.grid_propagate(False)


class Problem:
    def __init__(self, master):
        master.title("UVa Judge | Problem")
        master.search_form = ctk.CTkEntry(master, placeholder_text="number of the problem")
        master.search_form.grid(row=0, column=1, padx=10, pady=10, sticky="ne")
        master.search_btn = ctk.CTkButton(master, text="Search", command=lambda: search(master))
        master.bind('<Return>', lambda x: search(master))
        master.search_btn.grid(row=0, column=2, padx=10, pady=10, sticky="nw")
        if master.pid is not None:
            with urllib.request.urlopen(ui.get_pdf_url(str(master.pid))) as response:
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(response.read())
                    temp_file_path = tmp_file.name

            master.temp.append(temp_file_path)

            plat = platform.system()
            if plat == 'Darwin':  # for macOS
                subprocess.call(('open', temp_file_path))
            elif plat == 'Windows':  # for Windows
                subprocess.call(('cmd', '/C', 'start', '', temp_file_path))
            else:  # for Linux or other Unix-like systems
                subprocess.call(('xdg-open', temp_file_path))

            master.problem_label = ctk.CTkLabel(master, text=f'{master.prob_data["num"]} - {master.prob_data["title"]}')
            master.problem_label.configure(font=("Arial", 18, "bold"))
            master.problem_label.grid(row=1, column=1, sticky="nw", padx=10, pady=10)
            master.submit_btn = ctk.CTkButton(master, text="Submit this problem", command=lambda: open_web(master))
            master.submit_btn.grid(row=1, column=2, sticky="ne", padx=10)
            draw_graph(master)
            draw_submissions(master)
