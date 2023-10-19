import math
import tkinter as tk
from tkinter import filedialog
from rembg import remove
from PIL import Image, ImageTk

WIDTH = 800
HEIGHT = 600

IMAGE_WIDTH = 700
IMAGE_HEIGHT = 500


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    input_file = Image.open(file_path)
    image_width, image_height = input_file.size
    print(image_width, image_height)
    if image_width > IMAGE_WIDTH:
        percentage = IMAGE_WIDTH * 100 / image_width
        image_width = IMAGE_WIDTH
        image_height = math.floor(image_height * percentage / 100)
    if image_height > IMAGE_HEIGHT:
        percentage = IMAGE_HEIGHT * 100 / image_height
        image_height = IMAGE_HEIGHT
        image_width = math.floor(image_width * percentage / 100)
    print(image_width, image_height)
    output = remove(input_file)
    image_to_show = output.resize((image_width, image_height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image_to_show)
    if file_path:
        image_label.config(image=photo)
        image_label.image = photo
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")]
        )
        if save_path:
            output.save(save_path)


window = tk.Tk()
window.title = "Background remover"
window.geometry(f"{WIDTH}x{HEIGHT}")

open_label = tk.Label(window, text="Click to open, to open an image, which you want to remove the background.")
open_label.pack()

open_button = tk.Button(window, text="Open File", command=open_file)
open_button.pack(pady=10)

# Create a label to display the selected file
image_label = tk.Label(window)
image_label.pack()

window.mainloop()
