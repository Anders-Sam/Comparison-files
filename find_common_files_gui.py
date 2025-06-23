import os
import tkinter as tk
from tkinter import filedialog, Listbox, Label, Button, ttk # Added ttk
from datetime import datetime # Added datetime

# --- Global variables to store folder paths ---
folder1_path = ""
folder2_path = ""

# --- Helper function for file size ---
def format_size(size_bytes):
    """Converts size in bytes to a human-readable string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes/1024:.1f} KB"
    elif size_bytes < 1024**3:
        return f"{size_bytes/1024**2:.1f} MB"
    else:
        return f"{size_bytes/1024**3:.1f} GB"

# --- Main Application Window ---
window = tk.Tk()
window.title("Find Common Files")
window.geometry("900x500") # Increased window size for Treeview

# --- Helper function to get formatted file dates ---
def get_file_dates(file_path):
    """Gets formatted creation and modification dates for a file."""
    try:
        c_time = os.path.getctime(file_path)
        m_time = os.path.getmtime(file_path)
        # datetime is already imported globally: from datetime import datetime
        c_date_str = datetime.fromtimestamp(c_time).strftime('%Y-%m-%d %H:%M:%S')
        m_date_str = datetime.fromtimestamp(m_time).strftime('%Y-%m-%d %H:%M:%S')
        return c_date_str, m_date_str
    except OSError:
        return "N/A", "N/A"

# --- Functions to select folders ---
def select_folder1():
    global folder1_path
    folder1_path = filedialog.askdirectory()
    if folder1_path:
        folder1_label.config(text=f"Folder 1: {folder1_path}")
    else:
        folder1_label.config(text="Folder 1: Not Selected")

def select_folder2():
    global folder2_path
    folder2_path = filedialog.askdirectory()
    if folder2_path:
        folder2_label.config(text=f"Folder 2: {folder2_path}")
    else:
        folder2_label.config(text="Folder 2: Not Selected")

# --- Labels to display selected folder paths ---
folder1_label = Label(window, text="Folder 1: Not Selected")
folder1_label.pack(pady=5)

folder2_label = Label(window, text="Folder 2: Not Selected")
folder2_label.pack(pady=5)

# --- Status Label ---
status_label = Label(window, text="", fg="red")
status_label.pack(pady=5)

# --- Function to find common files ---
def find_common_files_action():
    status_label.config(text="")
    # Clear previous results from Treeview
    for item in results_tree.get_children():
        results_tree.delete(item)

    if not folder1_path or not folder2_path:
        status_label.config(text="Please select both folders.")
        return

    try:
        files_folder1 = {f for f in os.listdir(folder1_path) if os.path.isfile(os.path.join(folder1_path, f))}
        files_folder2 = {f for f in os.listdir(folder2_path) if os.path.isfile(os.path.join(folder2_path, f))}

        common_filenames = sorted(list(files_folder1.intersection(files_folder2)))

        if not common_filenames:
            status_label.config(text="No common files found.")
        else:
            status_label.config(text=f"Found {len(common_filenames)} common file(s):")
            for fname in common_filenames:
                path_f1 = os.path.join(folder1_path, fname)
                path_f2 = os.path.join(folder2_path, fname)

                f1_size_str = "N/A"
                try:
                    size_bytes_f1 = os.path.getsize(path_f1)
                    f1_size_str = format_size(size_bytes_f1)
                except OSError:
                    pass

                f2_size_str = "N/A"
                try:
                    size_bytes_f2 = os.path.getsize(path_f2)
                    f2_size_str = format_size(size_bytes_f2)
                except OSError:
                    pass

                f1_cdate, f1_mdate = get_file_dates(path_f1)
                f2_cdate, f2_mdate = get_file_dates(path_f2)

                results_tree.insert('', tk.END, values=(
                    fname,
                    f1_size_str,
                    f2_size_str,
                    f1_cdate,
                    f1_mdate,
                    f2_cdate,
                    f2_mdate
                ))

    except FileNotFoundError:
        status_label.config(text="Error: One or both folder paths are invalid.")
        # Clear treeview in case of error too
        for item in results_tree.get_children():
            results_tree.delete(item)
    except Exception as e:
        status_label.config(text=f"An error occurred: {e}")
        # Clear treeview in case of error too
        for item in results_tree.get_children():
            results_tree.delete(item)

# --- Treeview Frame and Scrollbars ---
tree_frame = ttk.Frame(window)
tree_frame.pack(pady=10, padx=10, fill="both", expand=True)

tree_scroll_y = ttk.Scrollbar(tree_frame, orient="vertical")
tree_scroll_y.pack(side="right", fill="y")

tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")
tree_scroll_x.pack(side="bottom", fill="x")

# --- Results Treeview ---
columns = ("filename", "f1_size", "f2_size", "f1_created", "f1_modified", "f2_created", "f2_modified")
results_tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                            yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

tree_scroll_y.config(command=results_tree.yview)
tree_scroll_x.config(command=results_tree.xview)

# Define column headings and properties
results_tree.heading("filename", text="Filename", anchor='w')
results_tree.column("filename", width=250, stretch=tk.YES, anchor='w')

results_tree.heading("f1_size", text="F1 Size", anchor='w') # Renamed from "size"
results_tree.column("f1_size", width=80, anchor='w')     # Renamed from "size"

results_tree.heading("f2_size", text="F2 Size", anchor='w') # New column
results_tree.column("f2_size", width=80, anchor='w')     # New column

results_tree.heading("f1_created", text="F1 Created", anchor='w')
results_tree.column("f1_created", width=140, anchor='w')

results_tree.heading("f1_modified", text="F1 Modified", anchor='w')
results_tree.column("f1_modified", width=140, anchor='w')

results_tree.heading("f2_created", text="F2 Created", anchor='w')
results_tree.column("f2_created", width=140, anchor='w')

results_tree.heading("f2_modified", text="F2 Modified", anchor='w')
results_tree.column("f2_modified", width=140, anchor='w')

results_tree.pack(side="left", fill="both", expand=True)


# --- Buttons ---
select_folder1_button = Button(window, text="Select Folder 1", command=select_folder1)
select_folder1_button.pack(pady=5)

select_folder2_button = Button(window, text="Select Folder 2", command=select_folder2)
select_folder2_button.pack(pady=5)

find_button = Button(window, text="Find Common Files", command=find_common_files_action)
find_button.pack(pady=10)

# --- Start the GUI event loop ---
window.mainloop()
