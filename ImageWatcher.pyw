"""

########################################
#                                      #
#            ImageWatcher              #
#                                      #
#   Version : v1.00                    #
#   Author  : github.com/Nenotriple    #
#                                      #
########################################

Description:
-------------
Continuously scan a specific folder for new images and display them as they appear.

"""

################################################################################################################################################
################################################################################################################################################
#         #
# Imports #
#         #

import os
import threading
import tkinter as tk
from tkinter import filedialog, Menu

##################
#                #
# Install Pillow #
#                #
##################

try:
    from PIL import Image, ImageTk
except ImportError:
    import subprocess, sys
    import threading
    from tkinter import Tk, Label, messagebox

    def download_pillow():
        cmd = ["pythonw", '-m', 'pip', 'install', 'pillow']
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        for line in iter(lambda: process.stdout.readline(), b''):
            pillow_label = Label(root, wraplength=450)
            pillow_label.pack(anchor="w")
            pillow_label.config(text=line.rstrip())
        process.stdout.close()
        process.wait()
        done_label = Label(root, text="\nAll done! This window will now close...", wraplength=450)
        done_label.pack(anchor="w")
        root.after(3000, root.destroy)

    root = Tk()
    root.title("Pillow Is Installing...")
    root.geometry('600x200')
    root.resizable(False, False)
    root.withdraw()
    root.protocol("WM_DELETE_WINDOW", lambda: None)

    install_pillow = messagebox.askyesno("Pillow not installed!", "Pillow not found!\npypi.org/project/Pillow\n\nWould you like to install it? ~2.5MB \n\n It's required to view images.")
    if install_pillow:
        root.deiconify()
        pillow_label = Label(root, wraplength=450)
        pillow_label.pack(anchor="w")
        pillow_label.config(text="Beginning Pillow install now...\n")
        threading.Thread(target=download_pillow).start()
        root.mainloop()
        from PIL import Image
    else:
        sys.exit()

################################################################################################################################################
################################################################################################################################################
#       #
# Setup #
#       #

class ImageWatcher:
    def __init__(self, folder):
        self.setup_window()
        self.setup_menu()
        self.setup_context_menu()
        self.folder = folder
        self.current_image = None
        self.update_id = None
        self.is_closed = False

    def setup_window(self):
        self.window = tk.Tk()
        self.window.title("v1.0 - Image Display  ---  github.com/Nenotriple/ImageWatcher")
        self.window.minsize(512, 512)
        self.window.geometry("512x512")
        self.photo_label = tk.Label(self.window)
        self.photo_label.pack(fill=tk.BOTH, expand=tk.YES)
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.bind("<Configure>", self.resize_image)

    def setup_menu(self):
        self.always_on_top = tk.BooleanVar()
        self.menubar = tk.Menu(self.window)
        self.window.config(menu=self.menubar)
        self.menubar.add_command(label="Choose Directory", command=self.choose_directory)
        self.menubar.add_checkbutton(label="Always on Top", variable=self.always_on_top, command=self.toggle_on_top)

    def setup_context_menu(self):
        self.context_menu = Menu(self.window, tearoff=0)
        self.context_menu.add_command(label="Open Image", command=self.open_image)
        self.context_menu.add_command(label="Open Folder", command=self.open_folder)
        self.photo_label.bind("<Button-3>", self.show_context_menu)

################################################################################################################################################
################################################################################################################################################
#      #
# Main #
#      #

    def choose_directory(self):
        def directory_dialog():
            new_folder = filedialog.askdirectory()
            if new_folder:
                self.folder = new_folder
            self.window.after(1000, self.update_image)
        threading.Thread(target=directory_dialog).start()

    def update_image(self):
        if self.folder:
            images = [f for f in os.listdir(self.folder) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
            latest_image = max(images, key=lambda x: os.path.getctime(os.path.join(self.folder, x)))
            if latest_image != self.current_image:
                self.current_image = latest_image
                self.resize_image()
        self.update_id = self.window.after(1000, self.update_image)

    def resize_image(self, event=None):
        if self.current_image:
            img = Image.open(os.path.join(self.folder, self.current_image))
            ratio = min(self.window.winfo_width()/img.width, self.window.winfo_height()/img.height)
            new_size = (int(img.width*ratio), int(img.height*ratio))
            img = img.resize(new_size, Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.photo_label.config(image=photo)
            self.photo_label.image = photo

    def run(self):
        self.update_image()
        self.window.mainloop()

    def on_close(self):
        if self.update_id is not None:
            self.window.after_cancel(self.update_id)
        self.window.destroy()

################################################################################################################################################
################################################################################################################################################
#      #
# Misc #
#      #

    def toggle_on_top(self):
        self.window.after(0, lambda: self.window.attributes('-topmost', self.always_on_top.get()))

    def show_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def open_image(self):
        os.startfile(os.path.join(self.folder, self.current_image))

    def open_folder(self):
        os.startfile(self.folder)

################################################################################################################################################
################################################################################################################################################
#       #
# Setup #
#       #

if __name__ == "__main__":
    display = ImageWatcher("")
    display.choose_directory()
    display.run()
