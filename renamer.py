import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def extract_last_four(filename):
    """Extract the last four characters from the filename (excluding the extension)."""
    return filename[-8:-4]  # Last four characters before the ".pdf"

def clean_filename(filename):
    """Remove unwanted text from the filename and convert to uppercase."""
    parts = filename.split('-')

    # Remove everything before the third dash from the start
    cleaned_parts_start = parts[3:]

    # Remove everything after the second dash from the end
    cleaned_parts_end = cleaned_parts_start[:-2]

    # Join the cleaned parts into the final cleaned filename
    cleaned_filename = '-'.join(cleaned_parts_end)

    # Convert to uppercase
    final_output = cleaned_filename.upper().replace('-', ' ')

    return final_output

def unique_filename(base_name, directory):
    """Generate a unique filename by appending a number in parentheses if it already exists."""
    base_name_without_ext, ext = os.path.splitext(base_name)  # Separate base name and extension
    count = 1
    new_name = base_name
    # Loop to find a unique name
    while os.path.exists(os.path.join(directory, new_name)):
        new_name = f"{base_name_without_ext}({count}){ext}"  # Append a number in parentheses before the extension
        count += 1
    return new_name

def move_pdfs_to_last_four_folders(directory):
    """Move PDF files into separate folders based on the last four characters."""
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]

    for pdf in pdf_files:
        last_four = extract_last_four(pdf)  # Extract the last four characters
        last_four_folder = os.path.join(directory, last_four)

        # Create a new folder for the last four characters if it doesn't exist
        os.makedirs(last_four_folder, exist_ok=True)

        # Move the PDF to the corresponding folder
        src = os.path.join(directory, pdf)
        dest = os.path.join(last_four_folder, pdf)
        shutil.move(src, dest)  # Move the file to the last four character folder

def sort_pdfs_and_store_unique(directory):
    # List all PDF files in the directory
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]

    if not pdf_files:
        messagebox.showinfo("No PDFs", "No PDF files found in the selected folder.")
        return

    # Sort the PDF filenames based on the year (last part of the filename)
    sorted_pdfs = sorted(pdf_files, key=lambda f: extract_last_four(f))

    # Clean the filenames by removing unwanted parts and keep only relevant data
    cleaned_filenames = [clean_filename(os.path.splitext(f)[0]) for f in sorted_pdfs]

    # Save the cleaned, sorted data to a text file in the same directory
    txt_file_path = os.path.join(directory, 'unique_names_sorted_cleaned.txt')
    with open(txt_file_path, 'w') as file:
        for data in cleaned_filenames:
            file.write(f"{data}\n")

    # Rename PDFs according to the cleaned names
    for original_pdf, new_name in zip(sorted_pdfs, cleaned_filenames):
        # Create new filename with .pdf extension
        base_new_pdf_name = new_name + '.pdf'
        new_pdf_name = unique_filename(base_new_pdf_name, directory)  # Ensure uniqueness
        original_pdf_path = os.path.join(directory, original_pdf)
        new_pdf_path = os.path.join(directory, new_pdf_name)

        # Rename the PDF file
        os.rename(original_pdf_path, new_pdf_path)

    # Move PDFs to folders based on the last four characters
    move_pdfs_to_last_four_folders(directory)

    # Pop up to inform where the text file is saved
    messagebox.showinfo("Success",
                        f"PDF files sorted and cleaned names saved in:\n{txt_file_path}\nFiltered PDFs moved to folders based on last four characters.")

def browse_folder():
    # Open a folder dialog to select the folder with PDFs
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        sort_pdfs_and_store_unique(folder_selected)

# Create the basic UI
root = tk.Tk()
root.title("PDF Sorter and Renamer")

# Create a button to browse the folder
browse_button = tk.Button(root, text="Select Folder with PDFs", command=browse_folder)
browse_button.pack(pady=20)

# Run the tkinter main loop
root.geometry("300x150")
root.mainloop()
