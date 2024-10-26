import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox


def copy_contents_to_target(parent_folder, target_folder):
    """Copy contents of all subdirectories in the parent folder to the target folder."""
    # Traverse the parent directory
    for root, dirs, files in os.walk(parent_folder):
        for file in files:
            source_path = os.path.join(root, file)
            # Construct the destination path
            destination_path = os.path.join(target_folder, file)

            # If the file already exists in the target, append a number to avoid overwriting
            if os.path.exists(destination_path):
                base, extension = os.path.splitext(file)
                count = 1
                while os.path.exists(destination_path):
                    destination_path = os.path.join(target_folder, f"{base} ({count}){extension}")
                    count += 1

            # Copy the file to the target folder
            shutil.copy2(source_path, destination_path)

    messagebox.showinfo("Success", f"All files copied to:\n{target_folder}")


def select_parent_folder():
    """Open a dialog to select the parent folder containing subdirectories."""
    parent_folder = filedialog.askdirectory(title="Select Parent Folder with Subdirectories")
    if parent_folder:
        target_folder = filedialog.askdirectory(title="Select Target Folder")
        if target_folder:
            copy_contents_to_target(parent_folder, target_folder)


# Create the basic UI
root = tk.Tk()
root.title("Folder Content Copier")

# Create a button to select the parent folder
browse_button = tk.Button(root, text="Select Parent Folder with Subdirectories", command=select_parent_folder)
browse_button.pack(pady=20)

# Run the tkinter main loop
root.geometry("300x150")
root.mainloop()
