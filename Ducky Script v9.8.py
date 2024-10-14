import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, Toplevel
import re

# Global variable to count title clicks for dev mode check
title_click_count = 0
animation_enabled = False  # Track animation status (off by default)

# Function to animate text writing
def animate_text(output_widget, text, delay=50):
    output_widget.delete(1.0, tk.END)
    for i, char in enumerate(text):
        output_widget.insert(tk.END, char)
        output_widget.update()
        output_widget.after(delay)  # Delay for each character

# Function to toggle animation
def toggle_animation():
    global animation_enabled
    animation_enabled = not animation_enabled
    animation_button.config(text=f"Animation ({'ON' if animation_enabled else 'OFF'})")  # Update button text

# Function to open developer menu
def open_dev_menu():
    dev_window = Toplevel(root)
    dev_window.title("Developer Menu")
    dev_window.geometry("400x300")

    dev_label = tk.Label(dev_window, text="Developer Menu", font=("Helvetica", 16, "bold"))
    dev_label.pack(pady=10)

    debug_button = tk.Button(dev_window, text="Debug Mode", command=debug_mode)
    debug_button.pack(pady=5)

    # Additional buttons for the dev menu
    button_1 = tk.Button(dev_window, text="Feature 1 Test", command=lambda: print("Feature 1"))
    button_1.pack(pady=5)

    button_2 = tk.Button(dev_window, text="Feature 2 Test", command=lambda: print("Feature 2"))
    button_2.pack(pady=5)

    button_3 = tk.Button(dev_window, text="Feature 3 Test", command=lambda: print("Feature 3"))
    button_3.pack(pady=5)

# Function for detecting title clicks
def on_title_click(event):
    global title_click_count
    title_click_count += 1  # Increment the click count
    if title_click_count >= 5:  # Check if clicked 5 times
        open_dev_menu()  # Open dev menu
        title_click_count = 0  # Reset after activation

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
    if animation_enabled:
        animate_text(output_textbox, formatted_script, delay=40)  # Animate the text
    else:
        output_textbox.delete(1.0, tk.END)
        output_textbox.insert(tk.END, formatted_script)  # Insert without animation

# Function to format the input into Ducky Script commands
def format_script(content):
    tokens = re.findall(r'\[.*?\]|[^\s\[\]]+', content)
    formatted_script = []

    for token in tokens:
        if token.startswith('[') and token.endswith(']'):  # Keep content within brackets intact
            formatted_script.append("WAIT_FOR_BUTTON_PRESS")
            formatted_script.append(f"DELAY {token}")
        else:
            for char in token:
                formatted_script.append("WAIT_FOR_BUTTON_PRESS")
                formatted_script.append(f"DELAY {char}")
    
    return '\n'.join(formatted_script)

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

# Function for debug mode (triggered by Dev menu)
def debug_mode():
    print("Debug mode activated!")  # debug-specific features here

# Function to display help information in a new window
def show_help():
    help_window = Toplevel(root)
    help_window.title("Help")
    help_window.geometry("400x500")
    help_window.configure(bg="#2c2c2c")

    help_label = tk.Label(help_window, text="How to Use the Program", font=("Helvetica", 14, "bold"), bg="#2c2c2c", fg="white")
    help_label.pack(pady=10)

    instructions = (
        "1. 📂 Upload a .txt file or type directly in the 'Input File Content' box.\n"
        "2. 🔄 Press 'Convert' to format the content into a Ducky Script.\n"
        "3. 📜 Review the script in the 'Formatted Ducky Script' box.\n"
        "4. 💾 Press 'Save Formatted Script' to save it as a .txt file.\n\n"
        "You can also input content manually and hit 'Convert' at any time."
    )
    help_text = tk.Label(help_window, text=instructions, wraplength=350, justify="left", font=("Helvetica", 10), bg="#2c2c2c", fg="white")
    help_text.pack(pady=10)

    # Info section
    info_label = tk.Label(help_window, text="⚠️ Info ⚠", font=("Helvetica", 12, "bold"), bg="#2c2c2c", fg="white")
    info_label.pack(pady=5)

    info_text = (
        "- If the .txt file has writing such as the title, the program will convert that into the script.\n"
        "- The program hasn't been tested with changing the piano transpose (up or down).\n\n"
        
        "🔒 Clicking the title 5 times opens a secret developer menu."
    )
    info_details = tk.Label(help_window, text=info_text, wraplength=350, justify="left", font=("Helvetica", 10), bg="#2c2c2c", fg="white")
    info_details.pack(pady=10)

# Function to copy formatted text to clipboard
def copy_to_clipboard():
    script = output_textbox.get(1.0, tk.END).strip()
    if script:
        root.clipboard_clear()  # Clear the clipboard
        root.clipboard_append(script)  # Copy the script to clipboard
        messagebox.showinfo("Copied", "Formatted script copied to clipboard!")

# Create the main window for Tkinter
root = tk.Tk()
root.title("📜 (Virtual Piano) Ducky Script Formatter 📜")
root.geometry("800x850")
root.configure(bg="#2c2c2c")  # Dark mode

# Create a frame for the title
title_frame = tk.Frame(root, bg="#2c2c2c")
title_frame.pack(pady=20)

# Title label with an emoji 📜
title_label = tk.Label(title_frame, text="📜 (Virtual Piano) Ducky Script Formatter 📜", 
                       font=("Helvetica", 20, "bold"), bg="#2c2c2c", fg="white")
title_label.pack()

# Help button under the title
help_button = tk.Button(title_frame, text="Help", command=show_help, bg="#f8f9fa", font=("Helvetica", 10))
help_button.pack(pady=5)

# Create a frame to hold the input and output buttons
frame = tk.Frame(root, bg="#2c2c2c")
frame.pack(pady=10)

# Button to upload the file
upload_button = tk.Button(frame, text="Upload .txt File", command=upload_file,
                          bg="#007bff", fg="white", font=("Helvetica", 12, "bold"), padx=20, pady=10)
upload_button.grid(row=0, column=0, padx=10)

# Button to save the formatted script
save_button = tk.Button(frame, text="Save Formatted Script", command=save_script,
                        bg="#28a745", fg="white", font=("Helvetica", 12, "bold"), padx=20, pady=10)
save_button.grid(row=0, column=1, padx=10)

# Input Textbox for showing uploaded file content or manual input
input_label = tk.Label(root, text="Input File Content:", bg="#2c2c2c", fg="white")
input_label.pack(pady=10)
input_textbox = scrolledtext.ScrolledText(root, height=10, width=50)  # Fairly large size
input_textbox.pack(padx=20)

# Convert Button
convert_button = tk.Button(root, text="Convert", command=convert_content,
                            bg="#ffc107", fg="black", font=("Helvetica", 12, "bold"), padx=20, pady=10)
convert_button.pack(pady=10)

# Output Textbox for formatted Ducky script
output_label = tk.Label(root, text="Formatted Ducky Script:", bg="#2c2c2c", fg="white")
output_label.pack(pady=10)
output_textbox = scrolledtext.ScrolledText(root, height=10, width=50)  # Fairly large size
output_textbox.pack(padx=20)

# Animation and Copy to Clipboard buttons
button_frame = tk.Frame(root, bg="#2c2c2c")
button_frame.pack(pady=10)

animation_button = tk.Button(button_frame, text="Animation (OFF)", command=toggle_animation,
                              bg="#6f42c1", fg="white", font=("Helvetica", 12, "bold"))
animation_button.pack(side=tk.LEFT, padx=20)

copy_button = tk.Button(button_frame, text="Copy to Clipboard", command=copy_to_clipboard,
                        bg="#17a2b8", fg="white", font=("Helvetica", 12, "bold"))
copy_button.pack(side=tk.RIGHT, padx=20)

# Reset Program button
reset_button = tk.Button(root, text="RESET PROGRAM", command=lambda: reset_program(),
                         bg="#dc3545", fg="white", font=("Helvetica", 10, "bold"))
reset_button.pack(pady=5)

# By MaximusMuir © 2024 text
footer_label = tk.Label(root, text="By MaximusMuir © 2024", bg="#2c2c2c", fg="white", font=("Helvetica", 8))
footer_label.pack(side=tk.BOTTOM, pady=10)

# Bind the title click event to detect 5 clicks for dev menu
title_label.bind("<Button-1>", on_title_click)

# Function to reset the program
def reset_program():
    input_textbox.delete(1.0, tk.END)  # Clear input text box
    output_textbox.delete(1.0, tk.END)  # Clear output text box
    # Reset other program states as necessary

# Start the Tkinter main loop
root.mainloop()
