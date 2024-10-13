# Virtual piano sheet music to ducky script converter

# Written by MaximusMuir on 13/10/24
# Do not take and adertise as your own

# New and improved UI, upload / download buttons on UI along with a "help" button explaining how it works
# Along with a text edior, for if you dont have a .txt file but just

# Look out for updates in the future

# Message me on discord (info in README file) if any issues arise !

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, Toplevel
import re

# Function to upload a .txt file and display its content
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
        input_textbox.delete(1.0, tk.END)  # Clear the input box
        input_textbox.insert(tk.END, content)  # Insert file content into the box
    else:
        messagebox.showerror("Error", "No file selected!")

# Function to process and format the input content
def handle_file_content(content):
    content = content.replace('\n', ' ').strip()  # Remove newlines and extra spaces
    formatted_script = format_script(content)  # Format the content
    output_textbox.delete(1.0, tk.END)  # Clear previous output
    output_textbox.insert(tk.END, formatted_script)  # Display the formatted script

# Function to format the input into Ducky Script commands
def format_script(content):
    # Use regex to find all tokens, including alphanumeric characters and brackets
    tokens = re.findall(r'\[.*?\]|[^\s\[\]]+', content)

    formatted_script = []
    for token in tokens:
        if token.startswith('[') and token.endswith(']'):  # Keep content within brackets intact
            formatted_script.append("WAIT_FOR_BUTTON_PRESS")
            formatted_script.append(f"STRING {token}")
        else:  # Process individual characters outside of brackets
            for char in token:
                formatted_script.append("WAIT_FOR_BUTTON_PRESS")
                formatted_script.append(f"STRING {char}")
    
    return '\n'.join(formatted_script)  # Combine the formatted lines into one string

# Function to save the formatted script to a .txt file
def save_script():
    script = output_textbox.get(1.0, tk.END).strip()  # Get the script from output box
    if not script:
        messagebox.showerror("Error", "No script to save!")
        return
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if save_path:
        with open(save_path, 'w') as file:
            file.write(script)  # Save the formatted script
        messagebox.showinfo("Success", f"Formatted script saved as: {save_path}")

# Function to convert input content when "Convert" button is pressed
def convert_content():
    content = input_textbox.get(1.0, tk.END).strip()  # Get the input content
    handle_file_content(content)  # Process the content

# Function to display help information in a new window
def show_help():
    help_window = Toplevel(root)
    help_window.title("Help")
    help_window.geometry("400x500")  # Increase height for better visibility

    help_label = tk.Label(help_window, text="How to Use the Program", font=("Helvetica", 14, "bold"))
    help_label.pack(pady=10)

    instructions = (
        "1. 📂 Upload a .txt file or type directly in the 'Inputed File Content' box.\n"
        "2. 🔄 Press 'Convert' to format the content into a Ducky Script.\n"
        "3. 📜 Review the script in the 'Formatted Ducky Script' box.\n"
        "4. 💾 Press 'Save Formatted Script' to save it as a .txt file.\n\n"
        "You can also input content manually and hit 'Convert' at any time."
    )
    help_text = tk.Label(help_window, text=instructions, wraplength=350, justify="left", font=("Helvetica", 10))
    help_text.pack(pady=10)

    # Info section
    info_label = tk.Label(help_window, text="⚠️ Info ⚠", font=("Helvetica", 12, "bold"))
    info_label.pack(pady=5)

    info_text = (
        "- If the .txt file has writing to say the title, the program will convert that into the script.\n"
        "  You might need to edit the program to remove that part.\n\n"
        "- The program hasn't been tested with changing the piano transpose (up or down)."
    )
    info_details = tk.Label(help_window, text=info_text, wraplength=350, justify="left", font=("Helvetica", 10))
    info_details.pack(pady=10)

# Create the main window for Tkinter
root = tk.Tk()
root.title("📜 (Virtual Piano) Ducky Script Formatter 📜")

# Set a good window size for vertical layout
root.geometry("600x850")
root.configure(bg="#f0f0f0")  # Light background color

# Title label with an emoji 📜
title_label = tk.Label(root, text="📜 (Virtual Piano) Ducky Script Formatter 📜", 
                       font=("Helvetica", 20, "bold"), bg="#f0f0f0")
title_label.pack(pady=20)

# Create a frame to hold buttons
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=10)

# Button to upload the file
upload_button = tk.Button(frame, text="Upload .txt File", command=upload_file,
                          bg="#007bff", fg="white", font=("Helvetica", 12, "bold"), padx=20, pady=10)
upload_button.grid(row=0, column=0, padx=10)

# Button to save the formatted script
save_button = tk.Button(frame, text="Save Formatted Script", command=save_script,
                        bg="#28a745", fg="white", font=("Helvetica", 12, "bold"), padx=20, pady=10)
save_button.grid(row=0, column=1, padx=10)

# Button to open the help window
help_button = tk.Button(root, text="Help", command=show_help, bg="#f8f9fa", font=("Helvetica", 10))
help_button.pack(pady=5)

# Input Textbox for showing uploaded file content or manual input
input_label = tk.Label(root, text="Inputed File Content:", bg="#f0f0f0")
input_label.pack(pady=10)
input_textbox = scrolledtext.ScrolledText(root, height=10, width=70)
input_textbox.pack(pady=10)

# Convert button
convert_button = tk.Button(root, text="Convert", command=convert_content, bg="#ffc107", fg="black", 
                           font=("Helvetica", 10, "bold"), padx=10, pady=5)  # Smaller button
convert_button.pack(pady=5)  # Closer to the textbox

# Output Textbox for showing formatted Ducky Script
output_label = tk.Label(root, text="(Editor) Formatted Ducky Script:", bg="#f0f0f0")
output_label.pack(pady=10)
output_textbox = scrolledtext.ScrolledText(root, height=15, width=70)
output_textbox.pack(pady=10)

# "By MaximusMuir © 2024" at the bottom
credits_label = tk.Label(root, text="By MaximusMuir © 2024", font=("Helvetica", 8), fg="gray", bg="#f0f0f0")
credits_label.pack(side="bottom", pady=10)

# Start the Tkinter application
root.mainloop()
