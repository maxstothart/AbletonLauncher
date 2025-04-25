import os
import tkinter as tk
from tkinter import ttk, messagebox, font
from PIL import Image, ImageTk
import subprocess
import yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# --- Configuration ---
ROW_HEIGHT = config["settings"]["style"]["scale"]
ROW_COUNT = 1 + 7
HEIGHT_OFFEST = 50  # 20-70 70-120
FONT_SIZE_BASE = 16
ICON_SIZE_FACTOR = 0.8
MAIN_ABLETON_FOLDER = config["settings"]["libraries"]["saves"]
ABLETON_PATH = config["settings"]["executables"]["ableton"]
try:
    FLEXGUI_PATH = config["settings"]["executables"]["flex"]
except:
    FLEXGUI_PATH = False
icon_path = "ableton_launcher.ico"
dark = config["settings"]["style"]["dark"]
# ----------------------


def set_dark_mode(root):
    """
    Sets the Tkinter window and its elements to a dark theme.

    Args:
        root: The Tkinter root window.
    """
    # Use the 'clam' or 'alt' theme, which supports dark mode.  The 'clam' theme is generally preferred.
    try:
        ttk.Style().theme_use('clam')
    except tk.TclError:
        try:
            ttk.Style().theme_use('alt')
        except tk.TclError:
            print(
                "Neither 'clam' nor 'alt' themes are available.  Dark mode may not be fully supported."
            )
            return  # Exit if no suitable theme is found

    # Configure the style for the entire application.  This targets the Ttk widgets.
    root.configure(bg="#2D2D2D")  # Set the background color of the main window.

    default_style = ttk.Style()

    # Dark background for Ttk frames.
    default_style.configure("TFrame", background="#2D2D2D")

    # Dark background and light foreground for labels.
    default_style.configure(
        "TLabel", background="#2D2D2D", foreground="#EEEEEE"
    )

    # Dark background, light foreground, and dark border for buttons.
    default_style.configure(
        "TButton",
        background="#424242",
        foreground="#EEEEEE",
        bordercolor="#616161",
        relief="raised",
    )
    default_style.map(
        "TButton",
        background=[
            ("active", "#666666"),  # Lighter on hover
            ("disabled", "#2D2D2D"),
        ],
        foreground=[("disabled", "#888888")],
    )

    # Dark background and light foreground for entries.
    default_style.configure(
        "TEntry",
        background="#424242",
        foreground="#EEEEEE",
        fieldbackground="#424242",  # For the text entry area
        bordercolor="#616161",
    )

    # Dark background and light foreground for text widgets (if you use them).
    default_style.configure(
        "TText",
        background="#2D2D2D",
        foreground="#EEEEEE",
        insertcolor="#EEEEEE",
    )  # Cursor color

    # Dark background and light foreground for Treeview
    default_style.configure(
        "Treeview",
        background="#2D2D2D",
        foreground="#EEEEEE",
        fieldbackground="#2D2D2D",
        bordercolor="#616161",
    )
    default_style.map(
        "Treeview",
        background=[("selected", "#4a4a4a")],  # Highlight selected rows
        foreground=[("selected", "#ffffff")],
    )

    # scrollbar
    default_style.configure(
        "Vertical.TScrollbar",
        background="#2D2D2D",
        troughcolor="#424242",
        arrowcolor="#EEEEEE",
    )


def find_ableton_sets_with_icons(root_folder):
    project_info_icons = []
    for root, _, files in os.walk(root_folder):
        if "Backup" not in root:
            for file in files:
                if file.endswith(".als"):
                    als_path = os.path.join(root, file)
                    set_directory = os.path.dirname(als_path)
                    icon_path = os.path.join(
                        set_directory, "Ableton Project Info", "AProject.ICO"
                    )
                    icon = None
                    if os.path.exists(icon_path):
                        try:
                            icon_size = int(ROW_HEIGHT * ICON_SIZE_FACTOR)
                            img = Image.open(icon_path)
                            img = img.resize((icon_size, icon_size), Image.LANCZOS)
                            icon = ImageTk.PhotoImage(img)
                        except Exception as e:
                            print(f"Error loading icon: {e}")
                    project_info_icons.append(
                        (os.path.getmtime(als_path), als_path, icon)
                    )
    project_info_icons.sort(key=lambda item: item[0], reverse=True)
    return project_info_icons


def open_set(set_path):
    try:
        os.startfile(set_path)
        exit()
    except OSError as e:
        messagebox.showerror("Error", f"Could not open '{set_path}': {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Error opening set: {e}")


def openProgram(program):
    if program == "Ableton":
        try:
            subprocess.Popen([ABLETON_PATH])
            exit()
            print(f"Opening Ableton Live from: {ABLETON_PATH}")
        except FileNotFoundError:
            messagebox.showerror(
                "Error", f"Ableton Live not found at: {ABLETON_PATH}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error opening Ableton Live: {e}")
    elif program == "flex":
        try:
            subprocess.Popen([FLEXGUI_PATH])
            print(f"Opening Flex GUI from: {FLEXGUI_PATH}")
        except FileNotFoundError:
            messagebox.showerror(
                "Error", f"Flex GUI not found at: {FLEXGUI_PATH}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error opening Flex GUI: {e}")



def main():
    root = tk.Tk()
    root.title("Ableton Live Sets")
    root.iconphoto(False, tk.PhotoImage(file=icon_path))

    try:
        found_sets_with_icons = find_ableton_sets_with_icons(MAIN_ABLETON_FOLDER)
        set_names = [
            os.path.splitext(os.path.basename(item[1]))[0]
            for item in found_sets_with_icons
        ]
        font_size = int(ROW_HEIGHT * (FONT_SIZE_BASE / 30))
        large_font = font.Font(family="Helvetica", size=font_size)
        longest_name = max(set_names, key=len) if set_names else ""
        text_width_pixels = large_font.measure(longest_name)
        icon_width_pixels = int(ROW_HEIGHT * 1.3)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        padding = 20
        window_width = icon_width_pixels + text_width_pixels + padding
        window_height = ROW_HEIGHT * ROW_COUNT + HEIGHT_OFFEST

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        if dark:
            set_dark_mode(root)

        style = ttk.Style()
        style.configure("Treeview", font=large_font, rowheight=ROW_HEIGHT)
        style.configure("Treeview.Heading", font=large_font)
        style.configure("TButton", font=large_font)

        # --- New Project Button Frame ---
        button_frame = ttk.Frame(root)
        button_frame.pack(side="bottom", pady=10)

        new_project_button = ttk.Button(
            button_frame, text="New Project", command=lambda: openProgram("Ableton"), style="TButton"
        )
        new_project_button.pack(side="left", padx=5)  # Add some padding between buttons
        new_project_button.configure(width={(x/4)*3})

        # Add a button to open Flex
        if FLEXGUI_PATH:
            open_flex_button = ttk.Button(
                button_frame, text="Flex Cfg", command=lambda: openProgram("flex"), style="TButton"
            )
            open_flex_button.pack(side="left", padx=5)
            open_flex_button.configure(width={(x/4)})


        tree_frame = ttk.Frame(root)
        tree_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        tree_y_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        tree_y_scrollbar.pack(side="right", fill="y")

        tree = ttk.Treeview(
            tree_frame,
            columns=('Name',),
            show='tree',
            style="Treeview",
            yscrollcommand=tree_y_scrollbar.set,
        )
        tree.heading('#0', text='', anchor=tk.W)
        tree.heading('Name', text='Name', anchor=tk.W)
        tree.column('#0', width=int(ROW_HEIGHT * 1.3), stretch=tk.NO)
        tree.column('Name', width=text_width_pixels, stretch=tk.NO)
        tree.pack(side="left", fill="both", expand=True)

        tree_y_scrollbar.config(command=tree.yview)

        for timestamp, set_path, icon in found_sets_with_icons:
            set_name_with_ext = os.path.basename(set_path)
            set_name = os.path.splitext(set_name_with_ext)[0]
            tree.insert(
                '', 'end', text='', values=(" " + set_name,), image=icon if icon else ""
            )

        def open_selected_set_event(event):
            selected_item = tree.selection()
            if selected_item:
                index = tree.index(selected_item[0])
                if 0 <= index < len(found_sets_with_icons):
                    set_to_open = found_sets_with_icons[index][1]
                    open_set(set_to_open)
        def open_selected_folder_event(event):
            selected_item = tree.selection()
            if selected_item:
                index = tree.index(selected_item[0])
                if 0 <= index < len(found_sets_with_icons):
                    set_to_open = found_sets_with_icons[index][1].split("\\")[:-1]
                    set_to_open = "\\".join(set_to_open)
                    print(set_to_open)
                    os.system("explorer.exe "+set_to_open)

        #tree.bind('<Double-Button-1>', open_selected_set_event)
        tree.bind('<Double-Button-1>', open_selected_set_event)
        tree.bind('<Button-3>', open_selected_folder_event)

        root.mainloop()

    except Exception as e:
        messagebox.showerror(
            "Fatal Error",
            f"An unexpected error occurred:\n\n{e}\n\nThe application will now close.",
        )
        root.destroy()



if __name__ == "__main__":
    main()
