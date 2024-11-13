import tkinter as tk
from tkinter import messagebox

def enkripsi(plain_text, shift):
    cipher_text = ""
    for char in plain_text:
        if char.isupper():
            cipher_text += chr((ord(char) + shift - 65) % 26 + 65)
        elif char.islower():
            cipher_text += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            cipher_text += char
    return cipher_text

def dekripsi(cipher_text, shift):
    plain_text = ""
    for char in cipher_text:
        if char.isupper():
            plain_text += chr((ord(char) - shift - 65) % 26 + 65)
        elif char.islower():
            plain_text += chr((ord(char) - shift - 97) % 26 + 97)
        else:
            plain_text += char
    return plain_text

def process_text():
    try:
        shift = int(shift_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid integer for the shift value.")
        return

    text = input_text.get("1.0", tk.END).strip()
    
    if encrypt_var.get():
        output = enkripsi(text, shift)
    else:
        output = dekripsi(text, shift)
    
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, output)

# Create main window
root = tk.Tk()
root.title("CIPHER ENCRYPTION MACHINE")
root.configure(bg="#1a1a2e")  # Set background color

# Shift value entry
tk.Label(root, text="Set Shift Value:", bg="#16213e", fg="white").grid(row=0, column=0, padx=10, pady=5, sticky="e")
shift_entry = tk.Entry(root, width=5, bg="#0f3460", fg="white")
shift_entry.grid(row=0, column=1, padx=10, pady=5)
shift_entry.insert(0, "3")  # Default shift value

# Input text area
tk.Label(root, text="Input Text to Encrypt/Decrypt:", bg="#16213e", fg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
input_text = tk.Text(root, height=5, width=50, bg="#0f3460", fg="white", insertbackground="white")
input_text.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

# Output text area
tk.Label(root, text="Output:", bg="#16213e", fg="white").grid(row=3, column=0, padx=10, pady=5, sticky="w")
output_text = tk.Text(root, height=5, width=50, bg="#0f3460", fg="white", insertbackground="white")
output_text.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

# Encryption/Decryption options
encrypt_var = tk.BooleanVar(value=True)
tk.Radiobutton(root, text="ENCRYPT", variable=encrypt_var, value=True, bg="#16213e", fg="white", selectcolor="#1a1a2e").grid(row=5, column=0, padx=10, pady=5, sticky="w")
tk.Radiobutton(root, text="DECRYPT", variable=encrypt_var, value=False, bg="#16213e", fg="white", selectcolor="#1a1a2e").grid(row=5, column=1, padx=10, pady=5, sticky="w")

# Process button
process_button = tk.Button(root, text="PROCESS TEXT", command=process_text, bg="#e94560", fg="white")
process_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Run the application
root.mainloop()
