import platform
import subprocess
import tkinter as tk
from tkhtmlview import HTMLLabel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import customtkinter as ctk
import u_interface as ui
import urllib.request
import tempfile


def search(master):
    master.prob_data = ui.get_problem(int(master.search_form.get()))
    master.pid = master.prob_data["num"]
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


class Problem:
    def __init__(self, master):
        master.title("UVa Judge | Problem")
        master.search_form = ctk.CTkEntry(master, placeholder_text="name of the problem")
        master.search_form.grid(row=0, column=1, padx=10, pady=10, sticky="ne")
        master.search_btn = ctk.CTkButton(master, text="Search", command=lambda: search(master))
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
            master.problem_label.grid(row=1, column=1, sticky="nw", padx=20, pady=10)
            draw_graph(master)

