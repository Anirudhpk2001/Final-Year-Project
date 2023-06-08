
import tkinter as tk
import PIL
from PIL import Image
from PIL import ImageTk
from cardiacdata import cardiacdata
from tkinter import filedialog
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import subprocess
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


import numpy as np
import os, torch

window = tk.Tk()
window.title("Cardiac Data Visualization")
canvas = None

def load_data():
    global folder_name
    folder_name = filedialog.askdirectory()  # Open folder selection dialog
    print(folder_name)
    if folder_name:
        dataset = cardiacdata(folder_name)
    loader = DataLoader(dataset, shuffle=False, batch_size=1)
    step, (img, gt) = next(enumerate(loader))
    img_np = img.squeeze().numpy()
    gt_np = gt.squeeze().numpy()
    # Create a Matplotlib figure and axes
    fig, axes = plt.subplots(1, 2, figsize=(6, 12))

    # Display the grayscale image slices
    for i in range(img_np.shape[0]):
        ax = axes[0].imshow(img_np[i], cmap='gray')
        axes[0].set_title('Image')
        axes[0].axis('off')

    # Display the ground truth slices
    for i in range(gt_np.shape[0]):
        ax = axes[1].imshow(gt_np[i], cmap='gray')
        axes[1].set_title('Ground Truth')
        axes[1].axis('off')
    #refresh_window()
    result_frame.update()
    width = result_frame.winfo_width()
    height = result_frame.winfo_height()

    fig.set_size_inches(width / 100, height / 100)
    canvas = FigureCanvasTkAgg(fig, master=result_frame)
    canvas.draw()
    #canvas.get_tk_widget().pack()
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

def generate_results():
    if folder_name:
        
        subprocess.run(["python", "TST_ELUNET.py", folder_name])
        #display_results()
    
    result_img = ImageTk.PhotoImage(Image.open('result.png'))
    result_label = tk.Label(result_frame, image=result_img)
    result_label.image = result_img  # Store a reference to prevent garbage collection
    result_label.grid(row=0, column=0, sticky="nsew")
    
    

"""
def display_results():
    # Perform the necessary processing to obtain the result image
    result_image = generate_results()

    # Create a PhotoImage object from the result image
    result_photo = ImageTk.PhotoImage(image=result_image)

    # Create a label to display the result image in the output frame
    result_label = tk.Label(output_frame, image=result_photo)
    result_label.image = result_photo  # Store a reference to prevent garbage collection
    result_label.pack
"""


button_frame = tk.Frame(window)
button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")


load_button = tk.Button(button_frame, text="Load Image", command=load_data)
load_button.grid(row=0, column=0, padx=5, pady=5)


generate_button = tk.Button(button_frame, text="Generate Results", command=generate_results)
generate_button.grid(row=1, column=0, padx=5, pady=5)


result_frame = tk.Frame(window, bd=1, relief=tk.SUNKEN)
result_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")



window.columnconfigure(1, weight=1)
window.rowconfigure(0, weight=1)
#window_width = 600
#window_height = 250

# Set the minimum and maximum size to the fixed width and height
#window.minsize(window_width, window_height)
#window.maxsize(window_width, window_height)
window.geometry("600x200")
# Run the tkinter event loop
window.mainloop()

