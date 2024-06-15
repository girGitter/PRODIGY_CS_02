import numpy as np
from PIL import Image, ImageTk, ImageOps
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def arnold_cat_map(image_array, iterations):
    n, m, c = image_array.shape
    result = np.copy(image_array)
    for _ in range(iterations):
        temp = np.copy(result)
        for i in range(n):
            for j in range(m):
                new_i = (i + j) % n
                new_j = (i + 2 * j) % m
                result[new_i, new_j] = temp[i, j]
    return result

def inverse_arnold_cat_map(image_array, iterations):
    n, m, c = image_array.shape
    result = np.copy(image_array)
    for _ in range(iterations):
        temp = np.copy(result)
        for i in range(n):
            for j in range(m):
                new_i = (2 * i - j) % n
                new_j = (-i + j) % m
                result[new_i, new_j] = temp[i, j]
    return result

def encrypt_image(image_path, output_path, key):
    image = Image.open(image_path)
    pixels = np.array(image)
    encrypted_pixels = arnold_cat_map(pixels, key)
    encrypted_image = Image.fromarray(encrypted_pixels.astype('uint8'))
    encrypted_image.save(output_path)
    return encrypted_image

def decrypt_image(encrypted_image_path, output_path, key):
    encrypted_image = Image.open(encrypted_image_path)
    encrypted_pixels = np.array(encrypted_image)
    decrypted_pixels = inverse_arnold_cat_map(encrypted_pixels, key)
    decrypted_image = Image.fromarray(decrypted_pixels.astype('uint8'))
    decrypted_image.save(output_path)
    return decrypted_image

def select_file():
    file_path = filedialog.askopenfilename()
    return file_path

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                             filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
    return file_path

def display_image(canvas, img):
    canvas.delete("all")
    img = img.resize((300, 300), Image.LANCZOS)
    tk_img = ImageTk.PhotoImage(img)
    canvas.image = tk_img
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)

def encrypt_action():
    input_path = select_file()
    if not input_path:
        return
    output_path = save_file()
    if not output_path:
        return
    key = simpledialog.askinteger("Input", "Enter encryption key (number of iterations):", minvalue=1, maxvalue=1000)
    if key is None:
        return
    img = Image.open(input_path)
    display_image(input_canvas, img)
    encrypted_img = encrypt_image(input_path, output_path, key)
    display_image(output_canvas, encrypted_img)
    messagebox.showinfo("Success", "Image encrypted successfully!")

def decrypt_action():
    input_path = select_file()
    if not input_path:
        return
    output_path = save_file()
    if not output_path:
        return
    key = simpledialog.askinteger("Input", "Enter decryption key (number of iterations):", minvalue=1, maxvalue=1000)
    if key is None:
        return
    img = Image.open(input_path)
    display_image(input_canvas, img)
    decrypted_img = decrypt_image(input_path, output_path, key)
    display_image(output_canvas, decrypted_img)
    messagebox.showinfo("Success", "Image decrypted successfully!")

def refresh_images():
    input_canvas.delete("all")
    output_canvas.delete("all")
    input_canvas.create_text(150, 150, text="Before", font=("Consolas", 16), fill="#FFFFFF")  # White color
    output_canvas.create_text(150, 150, text="After", font=("Consolas", 16), fill="#FFFFFF")  # White color

def exit_application():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()

def create_gui():
    global root
    root = tk.Tk()
    root.title("Image Encrypting Tool")
    root.geometry("800x600")

    # Load the background image
    bg_image = Image.open("terminal_background.jpg")
    bg_image = bg_image.resize((800, 600), Image.LANCZOS)  # Resize using LANCZOS filter
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    # Create a background label
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
    
    # Create a frame to hold all widgets and make it transparent
    main_frame = tk.Frame(root, bg='#008000', bd=0)  # Neonish green background
    main_frame.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.05)
    main_frame.tkraise(bg_label)

    title_label = tk.Label(main_frame, text="Image Encrypting Tool", font=("Consolas", 18, "bold"), bg='#008000', fg='#FFFFFF')  # White text
    title_label.pack(pady=20)

    button_frame = tk.Frame(main_frame, bg='#008000')
    button_frame.pack(pady=10)

    button_style = {'bg': '#FFFFFF', 'fg': '#000000', 'font': ("Consolas", 12, "bold"), 'relief': 'raised', 'bd': 3}  # White button with black text

    encrypt_button = tk.Button(button_frame, text="Encrypt Image", command=encrypt_action, width=20, height=2, **button_style)
    encrypt_button.grid(row=0, column=0, padx=20, pady=10)

    decrypt_button = tk.Button(button_frame, text="Decrypt Image", command=decrypt_action, width=20, height=2, **button_style)
    decrypt_button.grid(row=0, column=1, padx=20, pady=10)

    refresh_button = tk.Button(button_frame, text="Refresh Images", command=refresh_images, width=20, height=2, **button_style)
    refresh_button.grid(row=1, column=0, padx=20, pady=10)

    exit_button = tk.Button(button_frame, text="Exit", command=exit_application, width=20, height=2, **button_style)
    exit_button.grid(row=1, column=1, padx=20, pady=10)

    global input_canvas, output_canvas
    input_canvas = tk.Canvas(main_frame, width=300, height=300, bg='#000000', bd=2, relief='sunken')  # Black canvas
    input_canvas.pack(side=tk.LEFT, padx=10, pady=10)
    input_canvas.create_text(150, 150, text="Before", font=("Consolas", 16), fill="#FFFFFF")  # White text

    output_canvas = tk.Canvas(main_frame, width=300, height=300, bg='#000000', bd=2, relief='sunken')  # Black canvas
    output_canvas.pack(side=tk.RIGHT, padx=10, pady=10)
    output_canvas.create_text(150, 150, text="After", font=("Consolas", 16), fill="#FFFFFF")  # White text

    root.mainloop()

if __name__ == "__main__":
    create_gui()
