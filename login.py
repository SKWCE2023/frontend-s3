import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk, ImageDraw
import random
import string
from dashboard import DashboardFrame
from db import login

class LoginFrame:
    def __init__(self, root, showCaptcha, locked, logout_lock = False):
        self.showCaptcha = showCaptcha
        self.locked = locked
        self.root = root
        self.logout_lock = logout_lock
        self.create_app_icon_frame()
        self.create_login_frame()
        if self.logout_lock:
            messagebox.showinfo("Login Locked", "You can login after 1 minute.")
            self.lock_account(60000)

    def create_app_icon_frame(self):
        self.icon_frame = ttk.Frame(self.root)
        self.icon_frame.pack(padx=10, pady=10)
        image_path = 'assets/images/Logo.png'
        image_pil = Image.open(image_path).resize((150, 150))
        self.image = ImageTk.PhotoImage(image_pil)
        self.image_label = ttk.Label(self.icon_frame, image=self.image)
        self.image_label.pack(padx=10, pady=10)
    
    def create_login_frame(self):
        self.login_frame = ttk.Frame(self.root, padding=(20, 20))
        self.login_frame.pack(padx=10, pady=10)
        ttk.Label(self.login_frame, text="Username:", style="TLabel").grid(row=0, column=0, sticky="e", pady=10)
        self.username_entry = ttk.Entry(self.login_frame, font=('Helvetica 10'))
        self.username_entry.grid(row=0, column=1, pady=10)
        ttk.Label(self.login_frame, text="Password:", style="TLabel").grid(row=1, column=0, sticky="e", pady=10)
        self.password_entry = ttk.Entry(self.login_frame, show="*", font=('Helvetica 10'))
        self.password_entry.grid(row=1, column=1, pady=10)
        self.show_password_var = tk.IntVar()
        ttk.Checkbutton(
            self.login_frame, text="Show Password", variable=self.show_password_var, command=self.toggle_password_visibility,
            style="TCheckbutton"
        ).grid(row=2, columnspan=2, pady=10)
        if self.showCaptcha:
            self.create_captcha()
        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.validate_login)
        self.login_button.grid(row=6, columnspan=2, pady=10)

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def validate_login(self):
        try:
            if self.showCaptcha and not self.check_captcha():
                messagebox.showerror("Login Locked", "Incorrect captcha. Please try again after 10 seconds.")
                self.captcha_entry.delete(0, tk.END)
                self.generate_captcha()
                self.lock_account(10000)
                return
            username = self.username_entry.get()
            password = self.password_entry.get()
            if not username or not password:
                messagebox.showerror("Error", "Please fill in all the fields.")
                return
            data = {'username': username, 'password': password}
            response = login(data)
            if response.get("error_message"):
                if self.showCaptcha:
                    self.generate_captcha()
                    self.lock_account(10000)
                else:
                    self.create_captcha()
                self.showCaptcha = True
                messagebox.showerror("Login Failed", response["error_message"])
            else:
                self.showCaptcha = False
                self.show_dashboard(response['data'])
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Request Error", "Error in the request")

    def create_captcha(self):
        self.captcha_var = tk.StringVar()
        captcha_frame = ttk.Frame(self.login_frame, padding=(0, 10), style="TFrame")
        captcha_frame.grid(row=3, column=0, columnspan=2)
        ttk.Label(captcha_frame, text="Captcha:", style="TLabel").grid(row=0, column=0, sticky="e", pady=10)
        self.captcha_entry = ttk.Entry(captcha_frame)
        self.captcha_entry.grid(row=0, column=1)
        self.captcha_image_label = ttk.Label(captcha_frame, style="TLabel")
        self.captcha_image_label.grid(row=1, columnspan=2, pady=10)
        ttk.Button(captcha_frame, text="Regenerate", command=self.generate_captcha, style="TButton").grid(
            row=2, columnspan=2, pady=10
        )
        self.generate_captcha()

    def generate_captcha(self):
        captcha_text = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=4))
        self.captcha_var.set(captcha_text)
        captcha_image = Image.new('RGB', (150, 50), color=(150, 150, 150))
        captcha_draw = ImageDraw.Draw(captcha_image)
        x = 30
        for char in captcha_text:
            x1, y1 = random.randint(0, 150), random.randint(0, 50)
            x2, y2 = random.randint(0, 150), random.randint(0, 50)
            captcha_draw.line((x1, y1, x2, y2), fill="black")

            y = random.randint(10, 40)
            captcha_draw.text((x, y), char, font=None, fill="black")
            x += 30
        captcha_image_tk = ImageTk.PhotoImage(captcha_image)
        self.captcha_image_label.config(image=captcha_image_tk)
        self.captcha_image_label.image = captcha_image_tk

    def check_captcha(self):
        entered_captcha = self.captcha_entry.get()
        return entered_captcha == self.captcha_var.get()

    def lock_account(self, time):
        self.locked = True
        self.login_button.config(state=tk.DISABLED)
        self.root.after(time, self.unlock_account)

    def unlock_account(self):
        self.locked = False
        self.login_button.config(state=tk.NORMAL)
        messagebox.showinfo("Login Unlocked", "Login is now unlocked. You can try again.")

    def show_dashboard(self, user_info):
        self.login_frame.destroy()
        self.icon_frame.destroy()
        DashboardFrame(self.root, user_info, self.destroy_dashboard)
    
    def destroy_dashboard(self, root):
        LoginFrame(root, False, False, True)
