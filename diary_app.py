import tkinter as tk
from tkinter import messagebox, filedialog
import datetime
import os
import shutil
from PIL import Image, ImageTk

import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

default_font = ("Courier New", 12)
last_uploaded_picture = None

from PIL import Image, ImageTk

def set_app_icon():
    try:
        icon_path = resource_path("diary_icon.ico")
        icon_img = Image.open(icon_path)
        icon = ImageTk.PhotoImage(icon_img)
        root.iconphoto(False, icon)
    except Exception as e:
        print("Failed to set app icon:", e)


if not os.path.exists("entries"):
    os.makedirs("entries", exist_ok=True)
    os.makedirs("pictures", exist_ok=True)


def save_entry():
    global last_uploaded_picture

    text = entry_box.get("1.0", tk.END).strip()
    if text:
        now = datetime.datetime.now()
        filename = now.strftime("entries/%Y-%m-%d_%H-%M-%S.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
            if last_uploaded_picture:
                f.write(f"\n\n[Attached Image: {last_uploaded_picture}]")
        messagebox.showinfo("Saved", "Your diary entry was saved.")
        entry_box.delete("1.0", tk.END)
        last_uploaded_picture = None  # Reset after saving
    else:
        messagebox.showwarning("Empty", "You haven't written anything!")

# Upload and save a picture
from tkinter import filedialog
import shutil
import os
def upload_picture():
    global last_uploaded_picture

    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")]
    )

    if not file_path:
        return  # User canceled

    try:
        if not os.path.exists("pictures"):
            os.makedirs("pictures")

        filename = os.path.basename(file_path)
        target_path = os.path.join("pictures", filename)

        print(f"Copying from: {file_path}")
        print(f"To:           {target_path}")

        shutil.copy(file_path, target_path)

        if os.path.exists(target_path):
            last_uploaded_picture = filename
            messagebox.showinfo("Uploaded", f"Picture saved to:\n{target_path}")
        else:
            raise FileNotFoundError(f"Copied file not found: {target_path}")

    except Exception as e:
        messagebox.showerror("Upload Error", f"Failed to upload image:\n{e}")


def change_aesthetic():
    pass

def set_font(font_name):
    try:
        entry_box.configure(font=(font_name, 12))
    except Exception as e:
        messagebox.showerror("Font Error", f"Could not apply font:\n{e}")

# def new_entry():
#     pass    

import glob
from tkinter import Toplevel, Scrollbar

def view_all_entries():
    entries_window = Toplevel(root)
    entries_window.title("All Diary Entries")
    entries_window.geometry("600x500")
    entries_window.configure(bg="#fff0f5")

    canvas = tk.Canvas(entries_window, bg="#fff0f5")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(entries_window, command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    container = tk.Frame(canvas, bg="#fff0f5")
    canvas.create_window((0, 0), window=container, anchor="nw")

    files = sorted(glob.glob("entries/*.txt"))
    if not files:
        tk.Label(container, text="No diary entries found.", bg="#fff0f5", font=("Arial", 14)).pack(pady=20)
    else:
        for file_path in files:
            with open(file_path, "r", encoding="utf-8") as file:
                filename = os.path.basename(file_path)
                content = file.read()

                # Display entry text
                label = tk.Label(container, text=f"📅 {filename}", font=("Arial", 12, "bold"), bg="#fff0f5", anchor="w")
                label.pack(fill="x", padx=10, pady=(10, 0))

                text = content
                img_label = None

                # Check for attached image
                if "[Attached Image:" in content:
                    lines = content.splitlines()
                    image_line = next((line for line in lines if "[Attached Image:" in line), None)

                    if image_line:
                        image_name = image_line.replace("[Attached Image:", "").replace("]", "").strip()
                        text = content.replace(image_line, "")  # remove that line from the text

                        image_path = os.path.join("pictures", image_name)
                        try:
                            image = Image.open(image_path)
                            image.thumbnail((200, 200))
                            photo = ImageTk.PhotoImage(image)

                            img_label = tk.Label(container, image=photo, bg="#fff0f5")
                            img_label.image = photo  # keep reference
                        except Exception as e:
                            print(f"Could not load image: {image_path} - {e}")
                            img_label = tk.Label(container, text=f"[Image not found: {image_name}]", bg="#fff0f5")

                text_label = tk.Label(container, text=text.strip(), justify="left", wraplength=550, bg="#fff0f5", anchor="w")
                text_label.pack(fill="x", padx=10, pady=(0, 10))

                if img_label:
                    img_label.pack(padx=10, pady=(0, 10))

    container.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


def search_entries():
    pass

def add_picture():
    pass    

def view_gallery():
    gallery_window = Toplevel(root)
    gallery_window.title("Picture Gallery")
    gallery_window.geometry("600x400")
    gallery_window.configure(bg="#fff0f5")

    canvas = tk.Canvas(gallery_window, bg="#fff0f5")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(gallery_window, command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    gallery_frame = tk.Frame(canvas, bg="#fff0f5")
    canvas.create_window((0, 0), window=gallery_frame, anchor="nw")

    # Load images
    image_files = sorted(glob.glob("pictures/*"))
    if not image_files:
        label = tk.Label(gallery_frame, text="No pictures uploaded yet!", bg="#fff0f5", font=("Arial", 14))
        label.pack(pady=20)
    else:
        thumbnails = []
        for img_path in image_files:
            try:
                img = Image.open(img_path)
                img.thumbnail((150, 150))
                photo = ImageTk.PhotoImage(img)
                thumbnails.append(photo)

                label = tk.Label(gallery_frame, image=photo, bg="#fff0f5")
                label.image = photo  # prevent garbage collection
                label.pack(pady=5)
            except Exception as e:
                print(f"Failed to load image: {img_path}\n{e}")

    # Scroll region update
    gallery_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


# 🌸 Create the main window
root = tk.Tk()
set_app_icon()
root.title("Diary App")
root.geometry("550x500")

# 🌸 Create the menu bar
menu_bar = tk.Menu(root)

# 📁 File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
# file_menu.add_command(label="New")
# file_menu.add_command(label="Open")
# file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Edit Window menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Change Aesthetic")
edit_menu.add_separator()
font_menu = tk.Menu(edit_menu, tearoff=0)
font_menu.add_command(label="Arial", command=lambda: set_font("Arial"))
font_menu.add_command(label="1990", command=lambda: set_font("Courier New"))
font_menu.add_command(label="Cursive", command=lambda: set_font("Lucida Handwriting"))
edit_menu.add_cascade(label="Change Font", menu=font_menu)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# # ✍️ Write menu
# write_menu = tk.Menu(menu_bar, tearoff=0)
# write_menu.add_command(label="New Entry")
# write_menu.add_command(label="Save Entry", command=save_entry)
# menu_bar.add_cascade(label="Write", menu=write_menu)

# 📚 Entries menu
entries_menu = tk.Menu(menu_bar, tearoff=0)
entries_menu.add_command(label="View All Entries", command=view_all_entries)
# entries_menu.add_command(label="Search Entries")
menu_bar.add_cascade(label="Entries", menu=entries_menu)

# 🖼️ Pictures menu
pictures_menu = tk.Menu(menu_bar, tearoff=0)
pictures_menu.add_command(label="Add Picture", command=upload_picture)
pictures_menu.add_command(label="View Gallery", command=view_gallery)
menu_bar.add_cascade(label="Pictures", menu=pictures_menu)


## 🌸 Create the main window
root.config(menu=menu_bar) 
root.configure(bg="#f8c8dc")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

# 📷 Upload Picture button (row 0, column 0)
upload_button = tk.Button(
    root,
    text="Upload a Picture",
    command=upload_picture,
    font=("Arial", 12, "bold"),
    bg="#f8c8dc",
    fg="white",
    activebackground="#ebe2f1",
    activeforeground="white",
    height=2  # Ensures consistent height
)
upload_button.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

# 💾 Save Entry button (row 0, column 1)
save_button = tk.Button(
    root,
    text="Save Entry",
    command=save_entry,
    font=("Arial", 12, "bold"),
    bg="#f8c8dc",
    fg="white",
    activebackground="#ebe2f1",
    activeforeground="white",
    height=2  # Same height as upload button
)
save_button.grid(row=1, column=1, sticky="nsew", padx=10, pady=5)

# 📝 Text entry box (row 1, spans both columns)
entry_box = tk.Text(
    root,
    wrap="word",
    font=default_font,
    bg="#ebe2f1",
    fg="#ff69b4",
    insertbackground="#ff69b4"
)
entry_box.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)

root.mainloop()
