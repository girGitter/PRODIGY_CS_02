import numpy as np
from PIL import Image, ImageTk
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
    img = img.resize((300, 300))
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
    input_canvas.create_text(150, 150, text="Before", font=("Helvetica", 16), fill="white")
    output_canvas.create_text(150, 150, text="After", font=("Helvetica", 16), fill="white")

def exit_application():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()

def create_gui():
    global root
    root = tk.Tk()
    root.title("Image Encrypting Tool")

    title_label = tk.Label(root, text="Image Encrypting Tool", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=20)

    frame = tk.Frame(root)
    frame.pack(pady=10)

    encrypt_button = tk.Button(frame, text="Encrypt Image", command=encrypt_action, width=20, height=2)
    encrypt_button.grid(row=0, column=0, padx=10, pady=10)

    decrypt_button = tk.Button(frame, text="Decrypt Image", command=decrypt_action, width=20, height=2)
    decrypt_button.grid(row=0, column=1, padx=10, pady=10)

    refresh_button = tk.Button(frame, text="Refresh Images", command=refresh_images, width=20, height=2)
    refresh_button.grid(row=1, column=0, padx=10, pady=10)

    exit_button = tk.Button(frame, text="Exit", command=exit_application, width=20, height=2)
    exit_button.grid(row=1, column=1, padx=10, pady=10)

    global input_canvas, output_canvas
    input_canvas = tk.Canvas(root, width=300, height=300, bg='gray')
    input_canvas.pack(side=tk.LEFT, padx=10, pady=10)
    input_canvas.create_text(150, 150, text="Before", font=("Helvetica", 16), fill="white")

    output_canvas = tk.Canvas(root, width=300, height=300, bg='gray')
    output_canvas.pack(side=tk.RIGHT, padx=10, pady=10)
    output_canvas.create_text(150, 150, text="After", font=("Helvetica", 16), fill="white")

    root.mainloop()

if __name__ == "__main__":
    create_gui()

