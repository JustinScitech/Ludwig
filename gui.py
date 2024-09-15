# import tkinter as tk
# from tkinter import filedialog
# import subprocess

# def select_image():
#     # Open a file dialog to select an image file
#     file_path = filedialog.askopenfilename(
#         title='Select Image',
#         filetypes=[('Image Files', '*.jpg *.jpeg *.png *.gif *.bmp')]
#     )
#     if file_path:
#         # Run 'python3 main.py <image_file>'
#         subprocess.run(['python3', 'main.py', file_path])

# # Create the main application window
# root = tk.Tk()
# root.title('Image Submitter')

# # Create and place the 'Select Image' button
# select_button = tk.Button(root, text='Select Image', command=select_image)
# select_button.pack(pady=20)

# # Start the GUI event loop
# root.mainloop()






import tkinter as tk
from tkinter import filedialog
import subprocess
from PIL import Image, ImageTk

def select_image():
    # Open a file dialog to select an image file
    file_path = filedialog.askopenfilename(
        title='Select Image',
        filetypes=[('Image Files', '*.jpg *.jpeg *.png *.gif *.bmp')]
    )
    if file_path:
        # Run 'python3 main.py <image_file>'
        subprocess.run(['python3', 'main.py', file_path])

# Create the main application window
root = tk.Tk()
root.title('Ludwig')

# Set window size
root.geometry('900x600')
root.resizable(False, False)

# Set window icon (replace 'icon.ico' with your icon file)
try:
    root.iconbitmap('icon.ico')
except:
    pass  # If the icon file is not found, continue without setting an icon

# Load and set the background image (replace 'background.jpg' with your image file)
try:
    bg_image = Image.open('background.jpg')
    bg_image = bg_image.resize((300, 300), Image.ANTIALIAS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
except:
    root.configure(bg='#ffffff')  # Set a default background color if image not found

# Create a frame to hold the content with transparent background
content_frame = tk.Frame(root, bg='#ffffff')
content_frame.pack(pady=150)

# Create and place a title label
title_label = tk.Label(
    content_frame,
    text='Ludwig',
    font=('Arial', 60, 'bold'),
    bg='#ffffff',  # Match the background color
    fg='#333333'
)
title_label.pack(pady=10)

# Add the description label
description_label = tk.Label(
    content_frame,
    text='Ludwig is a tool that takes in a picture of sheet music as input and then plays the notes on a physical piano. Upload a picture of sheet music to get started!',
    font=('Arial', 20),
    bg='#ffffff',
    fg='#555555',
    wraplength=600,
    justify='center',
    
)
description_label.pack(pady=10)

# Create and place the 'Select Image' button with styling
select_button = tk.Button(
    content_frame,
    text='Select Image',
    command=select_image,
    font=('Arial', 20),
    bg='#4CAF50',
    fg='#000000',  # Changed from white to black
    activebackground='#45a049',
    padx=20,
    pady=10,
    bd=0,
    relief='flat',
    cursor='hand2'
)
select_button.pack(pady=20)

# Start the GUI event loop
root.mainloop()