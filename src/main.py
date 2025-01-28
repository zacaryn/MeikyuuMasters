import tkinter as tk

def toggle_text():
    """Toggle the visibility of the 'Hello World' label."""
    if label.cget("text") == "":
        label.config(text="Hello World")
    else:
        label.config(text="")

# Create the main application window
root = tk.Tk()
root.title("Meikyuu Masters")
root.geometry("720x480")  # Set window size (width x height)

# Create a label to display the text
label = tk.Label(root, text="", font=("Arial", 16))
label.pack(pady=20)

# Create a button to toggle the label's text
toggle_button = tk.Button(root, text="Toggle", command=toggle_text, font=("Arial", 12))
toggle_button.pack(pady=10)

# Run the application
root.mainloop()
