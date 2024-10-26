import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox


def extract_year_from_filename(filename):
    """Extract the year from the filename (assuming it's the last part before the extension)."""
    parts = filename.split('-')
    year_part = parts[-1]  # Assuming the year is always the last part before the extension
    year = os.path.splitext(year_part)[0]  # Remove the '.pdf' extension
    return year


def clean_filename(filename):
    """Remove everything before the third dash from the start and between the third and first dashes from the end."""
    parts = filename.split('-')

    # Remove everything before the third dash from the start (keep from the 4th part onward)
    parts_after_start_clean = parts[3:]

    # Remove everything between the third dash from the end and the first dash from the end
    cleaned_parts = parts_after_start_clean[:-3] + [
        parts_after_start_clean[-1]]  # Keep all except 3rd and 2nd from last

    # Join the cleaned parts into the final cleaned filename
    cleaned_filename = '-'.join(cleaned_parts)

    # Remove everything after the first dash from the end
    cleaned_filename = cleaned_filename.rsplit('-', 1)[0]

    # Convert to uppercase and replace dashes with spaces
    final_output = cleaned_filename.upper().replace('-', ' ')

    return final_output


def move_filtered_pdfs(directory, new_folder):
    """Move PDF files ending with certain years to a new folder."""
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    valid_years = ('2018', '2019', '2020', '2021', '2022', '2023', '2024')

    # Create the new folder if it doesn't exist
    os.makedirs(new_folder, exist_ok=True)

    for pdf in pdf_files:
        # Check if the filename ends with one of the valid years
        if pdf[-8:-4] in valid_years:  # Extracting last 4 characters before ".pdf"
            src = os.path.join(directory, pdf)
            dest = os.path.join(new_folder, pdf)
            shutil.move(src, dest)  # Move the file to the new folder


def sort_pdfs_and_store_unique(directory):
    # List all PDF files in the directory
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]

    if not pdf_files:
        messagebox.showinfo("No PDFs", "No PDF files found in the selected folder.")
        return

    # Sort the PDF filenames based on the year (last part of the filename)
    sorted_pdfs = sorted(pdf_files, key=lambda f: extract_year_from_filename(f))

    # Clean the filenames by removing unwanted parts and keep only relevant data
    cleaned_filenames = [clean_filename(os.path.splitext(f)[0]) for f in sorted_pdfs]

    # Save the cleaned, sorted data to a text file in the same directory
    txt_file_path = os.path.join(directory, 'unique_names_sorted_cleaned12.txt')
    with open(txt_file_path, 'w') as file:
        for data in cleaned_filenames:
            file.write(f"{data}\n")

    # Create a new folder for the filtered PDFs
    new_folder_name = "Filtered_PDFs"
    new_folder_path = os.path.join(directory, new_folder_name)

    # Move filtered PDFs to the new folder
    move_filtered_pdfs(directory, new_folder_path)

    # Pop up to inform where the text file is saved
    messagebox.showinfo("Success",
                        f"PDF files sorted and cleaned names saved in:\n{txt_file_path}\nFiltered PDFs moved to:\n{new_folder_path}")


def browse_folder():
    # Open a folder dialog to select the folder with PDFs
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        sort_pdfs_and_store_unique(folder_selected)


# Create the basic UI
root = tk.Tk()
root.title("PDF Sorter by Year (Cleaned)")

# Create a button to browse the folder
browse_button = tk.Button(root, text="Select Folder with PDFs", command=browse_folder)
browse_button.pack(pady=20)

# Run the tkinter main loop
root.geometry("300x150")
root.mainloop()
