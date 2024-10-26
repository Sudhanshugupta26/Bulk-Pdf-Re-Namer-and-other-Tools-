import tkinter as tk
from tkinter import filedialog
import os

def select_pdfs_and_save():
    # Open file dialog to select multiple PDF files
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_paths = filedialog.askopenfilenames(
        title="Select PDF files",
        filetypes=[("PDF files", "*.pdf")]
    )

    if file_paths:
        # Extract the file names without the '.pdf' extension
        file_names = [os.path.splitext(os.path.basename(file_path))[0] for file_path in file_paths]

        # Save the file names into a text file
        with open('selected_pdfs2018.txt', 'w') as f:
            for file_name in file_names:
                f.write(file_name + '\n')

        print(f"{len(file_names)} PDF file names saved to 'selected_pdfs.txt' without extension")

if __name__ == "__main__":
    select_pdfs_and_save()
