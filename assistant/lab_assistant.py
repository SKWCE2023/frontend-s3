import tkinter as tk
from tkinter import ttk
from .add_client import AddClientFrame
from .create_order import CreateOrderFrame

class AssistantFrame(ttk.Frame):
    def __init__(self, master=None, user_info = None):
        super().__init__(master)
        self.user_info = user_info
        ttk.Label(self, text="Please select the action you need to perform:").pack(padx=10, pady=10)
        ttk.Button(self, text="Create Order", command=self.create_order_frame).pack(pady=10)
        ttk.Button(self, text="Add New Client", command=self.add_client_frame).pack(pady=10)

    def create_order_frame(self):
        create_order_window = tk.Toplevel(self)
        CreateOrderFrame(create_order_window, self.user_info)
    
    def add_client_frame(self):
        add_client_window = tk.Toplevel(self)
        add_client_frame = AddClientFrame(add_client_window)
