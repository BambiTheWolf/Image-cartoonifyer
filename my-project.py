import cv2 #for image processing
import easygui
from easygui.boxes.derived_boxes import codebox #to open the filebox
import numpy as np #to store image
import imageio #to read image stored at particular path
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

top=tk.Tk()
top.geometry('400x400')
top.title('Cartoonify Your Image!')
top.configure(background='white')
label=Label(top, background='#CDCDCD', font=('calibri', 20, 'bold'))


def upload():
    image_path = easygui.fileopenbox()
    cartoonify(image_path)
    
    
# Main function
def cartoonify(image_path):
    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)   
    
# Confirming the image
    if original_image is None:
        print("Image missing. Choose an image to continue.")
        sys.exit()
    re_size1 = cv2.resize(original_image, (960, 540))
    
# Converting the file to a grayscale
    gray_scale_image = cv2.cvtColor (original_image, cv2.COLOR_BGR2GRAY)
    re_size2 = cv2.resize (gray_scale_image, (960, 540))
    
# Smoothening the image
    smooth_gray_scale = cv2.medianBlur(gray_scale_image, 5)
    re_size3 = cv2.resize(smooth_gray_scale, (960, 540))
    
# Retrieving the edges
    get_edge = cv2.adaptiveThreshold(smooth_gray_scale, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    re_size4 = cv2.resize(get_edge, (960, 540))
    
# Applying bilateral filter to remove noise 
# and keep edge sharp
    color_image = cv2.bilateralFilter(original_image, 9, 300, 300)
    re_size5 = cv2.resize(color_image, (960, 450))
    
# Masking edged image
    cartoon_image = cv2.bitwise_and(color_image, color_image, mask=get_edge)
    re_size6 = cv2.resize(cartoon_image, (960, 540))
    
# Plotting the entire transition
    images = [re_size1, re_size2, re_size3, re_size4, re_size5, re_size6]
    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
        
# Save button 
    save1 = Button(top, text='Save image', command=lambda: save(image_path, re_size6), padx=30, pady=5)
    save1.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
    save1.pack(side=TOP, pady=50)
    
    plt.show()
    
    
def save(resize6, image_path):
    new_name = 'cartoonified_image'
    path1 = os.path.dirname(image_path)
    extension = os.path.splitext (image_path)[1]
    path = os.path.join(path1, new_name + extension)
    cv2.imwrite(path, cv2.cvtColor(resize6, cv2.COLOR_RGB2BGR))
    I = 'Image saved as' + new_name + 'in' + path
    tk.messagebox.showinfo(title=None, message=I)
    
upload = Button(top, text="Cartoonify an Image", command=upload, padx=10, pady=5)
upload.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
upload.pack(side=TOP, pady=50)
    
top.mainloop()