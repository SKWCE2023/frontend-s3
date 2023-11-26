# from utils.utils import create_login_frame
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw
from datetime import datetime, timedelta
from assistant.lab_assistant import AssistantFrame
from researcher.lab_researcher import ResearcherFrame
from administrator.administrator import AdministratorFrame
from accountant.accountant import AccountantFrame
import utils.constants as constants
import requests
from db import logout

class DashboardFrame:
    def __init__(self, root, user_info, on_destroy):
        self.on_destroy = on_destroy
        self.user_type = str(user_info['role'])
        self.user_frames = {
            '1': AssistantFrame,
            '2': ResearcherFrame,
            '3': AccountantFrame,
            '4': AdministratorFrame,
        }
        self.root = root
        self.user_info = user_info
        self.create_dashboard_frame()
        self.create_user_frame()

    def create_dashboard_frame(self):
        self.dashboard_frame = ttk.Frame(self.root)
        self.dashboard_frame.pack(fill=tk.BOTH, expand=True)
        self.display_user_info()
        self.session_timer = 2 * 60
        self.warning_time = 1 * 60
        self.create_timer_label()
        self.start_timer()
        ttk.Button(self.dashboard_frame, text='Logout', command=self.user_logout).pack(pady=10)

    def get_image_path(self):
        if self.user_type == '2':
            return 'assets/images/laborant_2.png'
        if self.user_type == '3':
            return 'assets/images/accountant.jpeg'
        elif self.user_type == '4':
            return 'assets/images/Administrator.png'
        else:
            return 'assets/images/laborant_1.jpeg'

    def display_user_info(self):
        image_path = self.get_image_path()
        original_image = Image.open(image_path).resize((100, 100))
        mask = Image.new('L', original_image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, original_image.size[0], original_image.size[1]), fill=255)
        circular_image = Image.new('RGBA', original_image.size, (255, 255, 255, 0))
        circular_image.paste(original_image, mask=mask)
        self.circular_image_tk = ImageTk.PhotoImage(circular_image)
        ttk.Label(self.dashboard_frame, image=self.circular_image_tk).pack(pady=10)
        ttk.Label(self.dashboard_frame, text=f"{self.user_info['first_name']} {self.user_info['last_name']}", font=('Helvetica', 16)).pack()
        ttk.Label(self.dashboard_frame, text=f"Role: {constants.user_roles[self.user_type]}", font=('Helvetica', 12)).pack()

    def create_timer_label(self):
        self.timer_label = ttk.Label(self.dashboard_frame, text='', font=('Helvetica', 10))
        self.timer_label.pack()

    def start_timer(self):
        self.remaining_time = self.session_timer
        self.update_timer_display()

    def update_timer_display(self):
        minutes, seconds = divmod(self.remaining_time, 60)
        timer_text = f'Session ends: {minutes:02d}:{seconds:02d}'
        self.timer_label['text'] = timer_text
        if self.remaining_time == self.warning_time:
            messagebox.showinfo('Warning: 1 minutes left', 'Your session will expire in 1 minute')
        self.remaining_time -= 1
        if self.remaining_time >= 0:
            self.root.after(1000, self.update_timer_display)
        else:
            self.user_logout()

    def user_logout(self):
        try:
            response = logout()
            self.user_frame.destroy()
            self.dashboard_frame.destroy()
            self.on_destroy(self.root)
        except requests.exceptions.RequestException as e:
            messagebox.showerror('Request Error', 'Error in the request')

    def create_user_frame(self):
        self.user_frame = ttk.Frame(self.root)
        self.user_frame.pack(fill=tk.BOTH, expand=True)
        for widget in self.user_frame.winfo_children():
            widget.destroy()
        user_frame_class = self.user_frames.get(self.user_type, AssistantFrame)
        user_frame = user_frame_class(self.user_frame, self.user_info)
        user_frame.pack()
