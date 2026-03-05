#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import time

# Printer settings
PRINTER_NAME = "Toshiba_e-STUDIO2309A"  # CUPS-safe name
DISPLAY_NAME = "Toshiba e-STUDIO2309A"  # Display name
PPD_DRIVER = "foomatic-db-compressed-ppds:0/ppd/foomatic-ppd/Generic-PCL_6_PCL_XL_Printer-pxlmono.ppd"

# Ping the IP 4 times to check reachability
def ping_ip(ip):
    try:
        result = subprocess.run(
            ["ping", "-c", "4", ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.returncode == 0
    except:
        return False

# Update loading label
def update_loading(text, loading_label):
    loading_label.config(text=text)
    loading_label.update()

# Authenticate root once using pkexec
def authenticate_root():
    try:
        subprocess.run(["pkexec", "true"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Installation thread
def install_printer_thread(ip, loading_window, loading_label):
    update_loading("Authenticating for root access...", loading_label)
    if not authenticate_root():
        loading_window.destroy()
        status_label.config(text="Authentication failed ❌")
        messagebox.showerror("Error", "Root authentication failed or cancelled.")
        return

    update_loading("Pinging printer...", loading_label)
    if not ping_ip(ip):
        loading_window.destroy()
        status_label.config(text="Printer not reachable ❌")
        messagebox.showerror("Connection Error", f"Printer {ip} did not respond to ping (4 requests).")
        return

    try:
        update_loading(f"Adding {DISPLAY_NAME} printer...", loading_label)
        subprocess.run([
            "pkexec", "lpadmin",
            "-p", PRINTER_NAME,
            "-E",
            "-v", f"socket://{ip}:9100",
            "-m", PPD_DRIVER
        ], check=True)

        update_loading("Setting default printer...", loading_label)
        subprocess.run(["pkexec", "lpoptions", "-d", PRINTER_NAME], check=True)

        update_loading("Restarting CUPS...", loading_label)
        subprocess.run(["pkexec", "systemctl", "restart", "cups"], check=True)

        update_loading("Installation complete ✅", loading_label)
        time.sleep(1)
        loading_window.destroy()
        status_label.config(text=f"{DISPLAY_NAME} Installed Successfully ✅")
        messagebox.showinfo(
            "Success",
            f"{DISPLAY_NAME} Installed Successfully!\n\nIP: {ip}\nDefault Printer: {DISPLAY_NAME}"
        )

    except subprocess.CalledProcessError as e:
        loading_window.destroy()
        status_label.config(text="Installation failed ❌")
        messagebox.showerror("Error", f"Printer installation failed!\n{e}")

# Start installation
def install_printer():
    ip = ip_entry.get().strip()
    if not ip:
        messagebox.showwarning("Input Error", "Please enter Printer IP Address")
        return

    # Loading window
    loading_window = tk.Toplevel(root)
    loading_window.title("Installing...")
    loading_window.geometry("300x120")
    loading_window.resizable(False, False)
    loading_label = tk.Label(loading_window, text="Starting...", fg="blue")
    loading_label.pack(expand=True)
    loading_window.grab_set()

    threading.Thread(
        target=install_printer_thread,
        args=(ip, loading_window, loading_label),
        daemon=True
    ).start()

# Exit confirmation
def on_exit():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.destroy()

# GUI setup
root = tk.Tk()
root.title(f"{DISPLAY_NAME} Linux Installer")
root.geometry("450x260")

status_label = tk.Label(root, text=f"Enter {DISPLAY_NAME} IP to start installation", fg="blue")
status_label.pack(pady=10)

tk.Label(root, text="Printer IP Address").pack(pady=5)
ip_entry = tk.Entry(root, width=35)
ip_entry.pack(pady=5)

tk.Button(root, text=f"Install {DISPLAY_NAME} Printer", command=install_printer).pack(pady=15)
tk.Button(root, text="Exit", command=on_exit).pack()

root.protocol("WM_DELETE_WINDOW", on_exit)
root.mainloop()
