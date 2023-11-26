import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import os
import time
from image_resizer_automatic import process_images
import os

# Get the home directory of the current user
home_directory = os.path.expanduser('~')

class FileArrangerApp:
    def __init__(self, root):
        self.root = root
        root.title("File Arranger with Image Viewer and Keyboard Reordering")

        # Frame for the file list and image viewer
        self.file_frame = tk.Frame(root, width=400, height=300, bg="white")
        self.image_frame = tk.Frame(root, width=400, height=300)
        self.file_frame.pack(side="left", fill="both", expand=True)
        self.image_frame.pack(side="right", fill="both", expand=True)

        # Instructions label
        self.label = tk.Label(self.file_frame, text="Drag and drop files here. Use arrow keys to reorder.")
        self.label.pack()

        # Listbox for files
        self.file_listbox = tk.Listbox(self.file_frame)
        self.file_listbox.pack(fill="both", expand=True)

        # Button to set timestamps
        self.set_timestamps_button = tk.Button(self.file_frame, text="Set Timestamps", command=self.set_timestamps)
        self.set_timestamps_button.pack()

        # Button to set timestamps and resize
        self.process_and_resize_button = tk.Button(self.file_frame, text="Set Timestamps and Resize", command=self.set_timestamps_and_resize)
        self.process_and_resize_button.pack()


        # Bind drop event
        self.file_listbox.drop_target_register(DND_FILES)
        self.file_listbox.dnd_bind('<<Drop>>', self.drop)

        # Bind selection event
        self.file_listbox.bind('<<ListboxSelect>>', self.show_image)

        # Bind key events
        self.file_listbox.bind('<Up>', self.move_up)
        self.file_listbox.bind('<Down>', self.move_down)
        self.file_listbox.bind('<Delete>', self.delete_selected)

        # Store file paths
        self.file_list = []

        # Label for the image
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()

    def drop(self, event):
        files = self.root.tk.splitlist(event.data)
        for f in files:
            if os.path.isfile(f) and f not in self.file_list:
                # Insert the file at the beginning of the list and Listbox
                self.file_list.insert(0, f)
                self.file_listbox.insert(0, os.path.basename(f))

    def set_timestamps_and_resize(self):
        # First, set timestamps as the original button does
        self.set_timestamps()

        # Then, resize images
        self.resize_images()

    def resize_images(self):
        # Set parameters for the resizing process
        canvas_width = 1440
        canvas_height = 3088
        #output_directory = '~/Pictures/Wallpapers/drmz'
        output_directory = os.path.join(home_directory, 'Pictures', 'Wallpapers', 'drmz')
        #originals_backed_up_dir = '~/Pictures/Wallpapers/originals'
        originals_backed_up_dir = os.path.join(home_directory, 'Pictures', 'Wallpapers', 'originals')

        # Call the process_images function
        if self.file_list:
            process_images(self.file_list, canvas_width, canvas_height, output_directory, originals_backed_up_dir)

    def set_timestamps(self):
        base_time = time.time()
        # Reverse the file list so that the oldest file is first
        self.file_list.reverse()
        for file in self.file_list:
            os.utime(file, (base_time, base_time))
            base_time += 60  # Increment time by 1 minute for each file

    def show_image(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            file_path = self.file_list[index]
            if os.path.splitext(file_path)[1].lower() in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
                img = Image.open(file_path)
                img.thumbnail((400, 300))
                photo = ImageTk.PhotoImage(img)
                self.image_label.config(image=photo)
                self.image_label.image = photo  # Keep a reference!

    def move_up(self, event):
        selected_indices = self.file_listbox.curselection()
        if selected_indices:
            index = selected_indices[0]
            if index > 0:
                # Move item in the listbox and file list
                selected_text = self.file_listbox.get(index)
                self.file_listbox.delete(index)
                self.file_listbox.insert(index - 1, selected_text)
                file = self.file_list.pop(index)
                self.file_list.insert(index - 1, file)

                # Update the last selected index
                self.last_selected_index = index - 1

                # Update selection and focus after a short delay
                self.file_listbox.after(100, self.update_selection_and_focus)

    def update_selection_and_focus(self):
        if hasattr(self, 'last_selected_index'):
            # Clear and then set the selection
            self.file_listbox.selection_clear(0, tk.END)
            self.file_listbox.selection_set(self.last_selected_index)

            # Ensure the moved item is visible
            self.file_listbox.see(self.last_selected_index)

            # Set focus to the Listbox and then to the specific item
            self.file_listbox.focus_set()
            self.file_listbox.activate(self.last_selected_index)
            self.file_listbox.selection_anchor(self.last_selected_index)

            # Update the image viewer with the newly selected item
            self.show_image_for_index(self.last_selected_index)

    def show_image_for_index(self, index):
        if 0 <= index < len(self.file_list):
            file_path = self.file_list[index]
            if os.path.splitext(file_path)[1].lower() in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
                img = Image.open(file_path)
                img.thumbnail((400, 300))
                photo = ImageTk.PhotoImage(img)
                self.image_label.config(image=photo)
                self.image_label.image = photo  # Keep a reference!

    def delete_selected(self, event):
        selected_indices = self.file_listbox.curselection()
        if selected_indices:
            index = selected_indices[0]
            self.file_listbox.delete(index)
            del self.file_list[index]

    def move_down(self, event):
        selected_indices = self.file_listbox.curselection()
        if selected_indices:
            index = selected_indices[0]
            if index < self.file_listbox.size() - 1:
                # Move item in the listbox
                text = self.file_listbox.get(index)
                self.file_listbox.delete(index)
                self.file_listbox.insert(index + 1, text)
                self.file_listbox.select_set(index + 1)

                # Reorder the file list
                file = self.file_list.pop(index)
                self.file_list.insert(index + 1, file)

# Initialize the application


# Initialize the application
root = TkinterDnD.Tk()

# Keep the window always on top
root.attributes('-topmost', True)


# Set a custom icon (replace 'path_to_icon.png' with your icon file path)
#icon = tk.PhotoImage(file='~/projects/dreamdrawer/image_modifier_gui_icon.png')
icon = tk.PhotoImage(file=os.path.join(home_directory, 'projects', 'dreamdrawer', 'image_modifier_gui_icon.png'))

root.iconphoto(False, icon)

app = FileArrangerApp(root)
root.mainloop()

