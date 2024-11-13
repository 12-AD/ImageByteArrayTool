import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import pyperclip

def save_image(data, filename):
    try:
        with open(filename, "wb") as f:
            f.write(bytearray(data))
        messagebox.showinfo("Success", f"Image saved as {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save image: {e}")

def on_save_button_click():
    # Get the byte data from the text box
    byte_data = text_box.get("1.0", "end-1c")
    
    # Validate if the byte data is not empty
    if not byte_data:
        messagebox.showwarning("Input Error", "Please paste the byte array into the text box.")
        return
    
    # Convert the pasted string into a list of integers
    try:
        byte_data_list = [int(byte.strip(), 16) for byte in byte_data.split(",") if byte.strip()]
    except ValueError:
        messagebox.showerror("Error", "Invalid byte data format. Please ensure it's a comma-separated list of hexadecimal values.")
        return

    # Ask for the file name using a save file dialog
    filename = filedialog.asksaveasfilename(defaultextension=".bmp", filetypes=[("BMP files", "*.bmp")])
    
    # If the user cancels the file dialog, return
    if not filename:
        return
    
    # Save the image
    save_image(byte_data_list, filename)

def on_upload_button_click():
    # Ask the user to upload an image file
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.bmp;*.png;*.jpg;*.jpeg")])
    
    if file_path:
        try:
            # Open the image and convert it to bytes
            with open(file_path, "rb") as img_file:
                img_data = img_file.read()
            
            # Update the text box with the byte data
            byte_string = ", ".join(f"0x{byte:02x}" for byte in img_data)
            text_box.delete("1.0", "end")  # Clear existing text
            text_box.insert("1.0", byte_string)  # Insert the byte array

            messagebox.showinfo("Success", f"Image '{file_path}' loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")

def on_copy_button_click():
    # Get the text from the text box and copy it to the clipboard
    byte_data = text_box.get("1.0", "end-1c")
    if byte_data:
        pyperclip.copy(byte_data)  # Copy to clipboard using pyperclip
        messagebox.showinfo("Copied", "Byte array copied to clipboard.")
    else:
        messagebox.showwarning("Input Error", "No byte array to copy. Please paste or upload image data.")

# Set up the main Tkinter window
root = tk.Tk()
root.title("Image to Byte Array and Save")

# Set window size
root.geometry("500x500")

# Label for instructions
label = tk.Label(root, text="Paste the byte array here or upload an image:")
label.pack(pady=10)

# Text box for byte array input
text_box = tk.Text(root, width=50, height=10)
text_box.pack(pady=10)

# Save button
save_button = tk.Button(root, text="Save Image", command=on_save_button_click)
save_button.pack(pady=10)

# Upload button
upload_button = tk.Button(root, text="Upload Image", command=on_upload_button_click)
upload_button.pack(pady=10)

# Copy button
copy_button = tk.Button(root, text="Copy to Clipboard", command=on_copy_button_click)
copy_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
