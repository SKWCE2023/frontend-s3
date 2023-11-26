import tkinter as tk
from tkinter import ttk
from .create_invoice import CreateInvoiceFrame

class AccountantFrame(ttk.Frame):
    def __init__(self, master=None, user_info = None):
        super().__init__(master)
        ttk.Label(self, text="Please select the action you need to perform:").pack(padx=10, pady=10)
        ttk.Button(self, text="Create Invoice", command=self.create_invoice_frame).pack(pady=10)
        ttk.Button(self, text="Create Reports", command=self.create_report_frame).pack(pady=10)

    def create_invoice_frame(self):
        root = tk.Toplevel(self)
        CreateInvoiceFrame(root)

    def create_report_frame(self):
        pass