import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

# Fungsi untuk menyembunyikan pesan dalam gambar
def encode_image(image_path, message, output_path):
    try:
        img = Image.open(image_path)
        binary_message = ''.join(format(ord(i), '08b') for i in message)

        if img.size[0] * img.size[1] < len(binary_message) // 3:
            raise ValueError("Gambar terlalu kecil untuk menampung pesan.")

        pixels = img.load()
        data = list(img.getdata())

        new_data = []
        msg_index = 0
        for pixel in data:
            if msg_index < len(binary_message):
                r, g, b = pixel
                r = (r & ~1) | int(binary_message[msg_index])
                msg_index += 1
                if msg_index < len(binary_message):
                    g = (g & ~1) | int(binary_message[msg_index])
                    msg_index += 1
                if msg_index < len(binary_message):
                    b = (b & ~1) | int(binary_message[msg_index])
                    msg_index += 1
                new_data.append((r, g, b))
            else:
                new_data.append(pixel)

        img.putdata(new_data)
        img.save(output_path)
        return True
    except Exception as e:
        return False, str(e)

# Fungsi untuk mengekstrak pesan dari gambar
def decode_image(image_path):
    try:
        img = Image.open(image_path)
        binary_message = ''

        for pixel in img.getdata():
            r, g, b = pixel
            binary_message += str(r & 1)
            binary_message += str(g & 1)
            binary_message += str(b & 1)

        message = ''
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i+8]
            message += chr(int(byte, 2))
            if message.endswith("$$$"):
                return message[:-3]
        return "Pesan tidak ditemukan."
    except Exception as e:
        return str(e)

# Fungsi untuk memilih gambar input
def select_input_image():
    file_path = filedialog.askopenfilename(title="Pilih Gambar")
    entry_input_image.delete(0, tk.END)
    entry_input_image.insert(0, file_path)

# Fungsi untuk memilih gambar output
def select_output_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    entry_output_image.delete(0, tk.END)
    entry_output_image.insert(0, file_path)

# Fungsi untuk menyembunyikan pesan
def hide_message():
    image_path = entry_input_image.get()
    message = text_message.get("1.0", tk.END).strip()
    output_path = entry_output_image.get()

    if not image_path or not message or not output_path:
        messagebox.showerror("Kesalahan", "Harap lengkapi semua input.")
        return

    message += "$$$"
    success, error_message = encode_image(image_path, message, output_path) if encode_image(image_path, message, output_path) else (False, error_message)

    if success:
        messagebox.showinfo("Berhasil", "Pesan berhasil disembunyikan!")
    else:
        messagebox.showerror("Kesalahan", f"Terjadi kesalahan: {error_message}")

# Fungsi untuk mengekstrak pesan
def extract_message():
    image_path = entry_input_image.get()

    if not image_path:
        messagebox.showerror("Kesalahan", "Harap pilih gambar terlebih dahulu.")
        return

    message = decode_image(image_path)
    text_message.delete("1.0", tk.END)
    text_message.insert(tk.END, message)

# Membuat aplikasi GUI dengan Tkinter
root = tk.Tk()
root.title("StegoPic - Aplikasi Steganografi Gambar")
root.geometry("700x600")
root.config(bg="#E3F2FD")  # Latar belakang biru muda

# Menambahkan gaya untuk font dan warna
heading_font = ("Helvetica", 16, "bold")
label_font = ("Arial", 12)
button_font = ("Arial", 10, "bold")

# Menambahkan label untuk nama aplikasi dan penjelasan di atas
header_label = tk.Label(root, text="StegoPic - Aplikasi Steganografi Gambar", font=("Arial", 18, "bold"), bg="#E3F2FD", fg="#37474F")
header_label.pack(pady=10)

description_label = tk.Label(root, text="Sembunyikan pesan dalam gambar atau ekstrak pesan tersembunyi dari gambar yang sudah ada.",
                             font=("Arial", 12), bg="#E3F2FD", fg="#37474F", wraplength=600)
description_label.pack(pady=5)

# Frame untuk Input
frame_input = tk.Frame(root, bg="#E3F2FD")
frame_input.pack(pady=15)

label_input_image = tk.Label(frame_input, text="Pilih Gambar Masukan:", font=label_font, bg="#E3F2FD", fg="#37474F")
label_input_image.grid(row=0, column=0, padx=10)

entry_input_image = tk.Entry(frame_input, width=40, font=("Arial", 12))
entry_input_image.grid(row=0, column=1, padx=10)

button_browse_input = tk.Button(frame_input, text="Pilih Gambar", font=button_font, bg="#A5D6A7", fg="#37474F", command=select_input_image)
button_browse_input.grid(row=0, column=2, padx=10, ipadx=10)

# Frame untuk Output
frame_output = tk.Frame(root, bg="#E3F2FD")
frame_output.pack(pady=15)

label_output_image = tk.Label(frame_output, text="Pilih Gambar Output:", font=label_font, bg="#E3F2FD", fg="#37474F")
label_output_image.grid(row=0, column=0, padx=10)

entry_output_image = tk.Entry(frame_output, width=40, font=("Arial", 12))
entry_output_image.grid(row=0, column=1, padx=10)

button_browse_output = tk.Button(frame_output, text="Pilih Lokasi", font=button_font, bg="#A5D6A7", fg="#37474F", command=select_output_image)
button_browse_output.grid(row=0, column=2, padx=10, ipadx=10)

# Frame untuk Pesan
frame_message = tk.Frame(root, bg="#E3F2FD")
frame_message.pack(pady=15)

label_message = tk.Label(frame_message, text="Pesan:", font=label_font, bg="#E3F2FD", fg="#37474F")
label_message.grid(row=0, column=0, padx=10)

text_message = tk.Text(frame_message, height=5, width=40, font=("Arial", 12))
text_message.grid(row=1, column=0, columnspan=3, padx=10)

# Tombol untuk menyembunyikan dan mengekstrak pesan
button_hide = tk.Button(root, text="Sembunyikan Pesan", font=button_font, bg="#90CAF9", fg="#37474F", command=hide_message)
button_hide.pack(pady=10, ipadx=10)

button_extract = tk.Button(root, text="Ekstrak Pesan", font=button_font, bg="#90CAF9", fg="#37474F", command=extract_message)
button_extract.pack(pady=10, ipadx=10)

# Menjalankan aplikasi
root.mainloop()
