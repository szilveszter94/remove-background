import math
import tkinter as tk
from tkinter import filedialog
import threading
from rembg import remove, new_session
from PIL import Image, ImageTk, ImageSequence

WIDTH = 800
HEIGHT = 600

IMAGE_WIDTH = 700
IMAGE_HEIGHT = 500


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;")])
    try:
        input_file = Image.open(file_path)
        open_image_button.config(state="disabled")
        open_gif_button.config(state="disabled")
        image_width, image_height = input_file.size
        if image_width > IMAGE_WIDTH:
            percentage = IMAGE_WIDTH * 100 / image_width
            image_width = IMAGE_WIDTH
            image_height = math.floor(image_height * percentage / 100)
        if image_height > IMAGE_HEIGHT:
            percentage = IMAGE_HEIGHT * 100 / image_height
            image_height = IMAGE_HEIGHT
            image_width = math.floor(image_width * percentage / 100)
        open_label.config(text="Processing...")
        output = remove(input_file)
        image_to_show = output.resize((image_width, image_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image_to_show)
        if file_path:
            open_label.config(text="Select the path, where you want to save.")
            image_label.config(image=photo)
            image_label.image = photo
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG Files", "*.png;"), ("All Files", "*.*")]
            )
            if save_path:
                output.save(save_path)
        open_image_button.config(state="normal")
        open_gif_button.config(state="normal")
        open_label.config(text="Click to open an image, which you want to remove the background.")
    except AttributeError:
        pass


def open_gif():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.gif")])

    def process_gif():
        try:
            gif = Image.open(file_path)
            open_image_button.config(state="disabled")
            open_gif_button.config(state="disabled")
            frame_count = 0
            frames = []
            for _ in ImageSequence.Iterator(gif):
                frame_count += 1
            session = new_session()
            for frame_number, frame in enumerate(ImageSequence.Iterator(gif), start=1):
                # Save each frame as a separate image (e.g., PNG)
                output = remove(frame, session=session, post_process_mask=True)
                frames.append(output)
                open_label.config(text=f"Process: {frame_number * 100 / frame_count} %")
            open_label.config(text="Select the path, where you want to save.")
            save_path = filedialog.asksaveasfilename(
                defaultextension=".gif",
                filetypes=[("GIF Files", "*.gif;"), ("All Files", "*.*")]
            )
            frames[0].save(save_path, save_all=True, append_images=frames[1:], loop=0, duration=50, disposal=2)
            open_image_button.config(state="normal")
            open_gif_button.config(state="normal")
            open_label.config(text="Click to open an image, which you want to remove the background.")
        except AttributeError:
            pass

    processing_thread = threading.Thread(target=process_gif)
    processing_thread.start()


window = tk.Tk()
window.title = "Background remover"
window.geometry(f"{WIDTH}x{HEIGHT}")

open_label = tk.Label(window, text="Click to open an image, which you want to remove the background.")
open_label.pack()

button_frame = tk.Frame(window)  # Create a frame for the buttons
button_frame.pack()

open_image_button = tk.Button(button_frame, text="Open Image", command=open_file)
open_image_button.pack(side="left", padx=10, pady=5)

open_gif_button = tk.Button(button_frame, text="Open Gif", command=open_gif)
open_gif_button.pack(side="right", padx=10, pady=5)

# Create a label to display the selected file
image_label = tk.Label(window)
image_label.pack()

window.mainloop()
