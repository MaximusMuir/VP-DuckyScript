# Virtual piano sheet music to ducky script converter

# Written by MaximusMuir on 28/09/24
# Do not take and adertise as your own

# Download this script and run.
# It will show a small window with a button to upload a .txt file (upload virtual piano sheet there)
# It will then imediat immediately prompt you to save a .txt file (the converted ducky script)
# Save the .txt ducky script somewhere you will remeber it, then transfer it to your BadUSB (my case: qFlipper - BadUSB folder)

# Message me on discord (info in README file) if any issues arise !

import tkinter as tk
from tkinter import filedialog
import re

# Function to handle the uploaded file from Tkinter
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            handle_file_content(content)

# Function to handle the file content
def handle_file_content(content):
    # Replace new lines with spaces, so everything is treated as one continuous string
    content = content.replace('\n', ' ').strip()
    
    # Process the content and get the formatted result
    formatted_script = format_script(content)
    
    # Save the formatted script to a file
    save_script(formatted_script)

# Function to format the output by separating individual characters and preserving non-alphanumeric sequences
def format_script(content):
    # Split into individual characters, keeping groups of non-alphanumeric characters like [123] together
    tokens = re.findall(r'\[.*?\]|\w|\d', content)
    
    formatted_script = []
    # Loop through each token and prepare the output
    for token in tokens:
        formatted_script.append("WAIT_FOR_BUTTON_PRESS")
        formatted_script.append(f"STRING {token}")
    
    return '\n'.join(formatted_script)

# Function to save the formatted script to a .txt file
def save_script(script):
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                               filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if save_path:
        with open(save_path, 'w') as file:
            file.write(script)

# Create the root window for Tkinter
root = tk.Tk()
root.title("Upload .txt File")

# Create a button to upload the file
upload_button = tk.Button(root, text="Upload .txt File", command=upload_file)
upload_button.pack(pady=30)

# Run the Tkinter application
root.mainloop()
