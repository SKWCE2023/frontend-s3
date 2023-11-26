import tkinter as tk
from tkinter import ttk
from .login_history import LoginHistory

class AdministratorFrame(ttk.Frame):
    def __init__(self, master=None, user_info = None):
        super().__init__(master)
        ttk.Label(self, text="Please select the action you need to perform:").pack(padx=10, pady=10)
        ttk.Button(self, text="Check Login History", command=self.check_login_history).pack(pady=10)
        ttk.Button(self, text="Check Reports", command=self.show_reports).pack(pady=10)
        ttk.Button(self, text="Check Consumables", command=self.view_consumables).pack(pady=10)

    def check_login_history(self):
        login_history_window = tk.Toplevel(self)
        login_history_frame = LoginHistory(login_history_window)

    def show_reports(self):
        print("Displaying Reports")

    def view_consumables(self):
        print("Viewing Consumables")