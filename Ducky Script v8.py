import tkinter as tk
from tkinter import filedialog
import re

# Function to handle the uploaded file from Tkinter
def upload_file():
    print("Prompting user to upload a .txt file...")
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    
    if file_path:
        print(f"File uploaded: {file_path}")
        with open(file_path, 'r') as file:
            content = file.read()
            print("File content read successfully.")
            handle_file_content(content)

# Function to handle the file content
def handle_file_content(content):
    print("Processing file content...")
    # Replace new lines with spaces, so everything is treated as one continuous string
    content = content.replace('\n', ' ').strip()
    print("New lines replaced with spaces.")

    # Process the content and get the formatted result
    formatted_script = format_script(content)
    print("Content formatted into Ducky Script.")

    # Save the formatted script to a file
    save_script(formatted_script)

# Function to format the output by separating individual characters and preserving non-alphanumeric sequences
def format_script(content):
    print("Formatting the script...")
    # Adjust regex to capture alphanumeric, special characters, and brackets
    tokens = re.findall(r'\[.*?\]|[^\s\[\]]+', content)
    print(f"Tokens extracted: {tokens}")

    formatted_script = []
    # Loop through each token and prepare the output
    for token in tokens:
        formatted_script.append("WAIT_FOR_BUTTON_PRESS")
        formatted_script.append(f"STRING {token}")

    # Join all lines with newlines to ensure each command is on a new line
    print("Script formatting complete.")
    return '\n'.join(formatted_script)

# Function to save the formatted script to a .txt file
def save_script(script):
    print("Prompting user to save the formatted script...")
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                               filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if save_path:
        with open(save_path, 'w') as file:
            file.write(script)
        print(f"Formatted script saved as: {save_path}")

# Create the root window for Tkinter
root = tk.Tk()
root.title("Upload .txt File")

# Create a button to upload the file
upload_button = tk.Button(root, text="Upload .txt File", command=upload_file)
upload_button.pack(pady=30)

# Run the Tkinter application
print("Application started. Waiting for user input...")
root.mainloop()
