import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from pdfrw import PdfReader, PdfWriter

def split_pdf_into_a6_labels(input_pdf_path, output_pdf_path):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        media_box = page.MediaBox

        width_A4 = float(media_box[2])  # Upper-right x
        height_A4 = float(media_box[3])  # Upper-right y

        width_A6 = width_A4 / 2
        height_A6 = height_A4 / 2

        for i in range(2):
            for j in range(2):
                lower_left_x = i * width_A6
                lower_left_y = j * height_A6
                upper_right_x = lower_left_x + width_A6
                upper_right_y = lower_left_y + height_A6

                new_page = page
                new_page.MediaBox = [lower_left_x, lower_left_y, upper_right_x, upper_right_y]
                new_page.CropBox = new_page.MediaBox

                writer.addpage(new_page)

    with open(output_pdf_path, 'wb') as output_pdf:
        writer.write(output_pdf)

    if os.path.exists(output_pdf_path):
        subprocess.call(['xdg-open', output_pdf_path])

def select_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

def split_pdf():
    input_pdf = input_entry.get()
    output_pdf = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                filetypes=[("PDF files", "*.pdf")])
    if output_pdf:
        try:
            split_pdf_into_a6_labels(input_pdf, output_pdf)
            messagebox.showinfo("Success", "PDF split successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("PDF A6 Splitter")

# Create the UI elements
tk.Label(root, text="Select PDF file:").pack(pady=10)
input_entry = tk.Entry(root, width=50)
input_entry.pack(padx=10)

tk.Button(root, text="Browse", command=select_pdf).pack(pady=5)
tk.Button(root, text="Split PDF", command=split_pdf).pack(pady=20)

# Start the main loop
root.mainloop()
