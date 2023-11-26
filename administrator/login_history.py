import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
import requests
from db import fetch_login_history

class LoginHistory:
    def __init__(self, root):
        self.root = root
        img = PhotoImage(file='assets/images/Logo.png')
        self.root.iconphoto(False, img)
        self.root.title("Login History")
        self.root.geometry("800x600")
        self.root.minsize("800","600")
        self.search_var = tk.StringVar()
        self.sort_order_var = tk.StringVar(value="Ascending") 
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=5, fill=tk.X)
        ttk.Label(search_frame, text="Search By Name:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        sort_order_frame = ttk.Frame(self.root)
        sort_order_frame.pack(pady=5, fill=tk.X)
        ttk.Label(sort_order_frame, text="Date Sort Order:").pack(side=tk.LEFT, padx=5)
        sort_options = ["Ascending", "Descending"]
        self.sort_order_combobox = ttk.Combobox(sort_order_frame, values=sort_options, textvariable=self.sort_order_var)
        self.sort_order_combobox.pack(side=tk.LEFT, padx=5)
        search_button_frame = ttk.Frame(self.root)
        search_button_frame.pack(pady=5, fill=tk.X)
        ttk.Button(search_button_frame, text="Search", command=self.fetch_and_display_data).pack(side=tk.LEFT, padx=5, pady=5)
        self.tree = ttk.Treeview(self.root, columns=("User Login", "User Name", "IP Address", "Login At", "Result"), show="headings")
        self.tree.heading("User Login", text="User Login", anchor="w")
        self.tree.heading("User Name", text="User Name", anchor="w")
        self.tree.heading("IP Address", text="IP Address", anchor="w")
        self.tree.heading("Login At", text="Login At", anchor="w")
        self.tree.heading("Result", text="Result", anchor="w")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.fetch_and_display_data()

    def fetch_and_display_data(self):
        username_to_search = self.search_var.get()
        sort_order = self.sort_order_var.get().lower()
        try:
            response = fetch_login_history(username=username_to_search, sort_order=sort_order)
            if response.get("error_message"):
                messagebox.showerror("Operation Failed", response["error_message"])
            else:
                for item in self.tree.get_children():
                    self.tree.delete(item)
                for row in response['data']:
                    result = "Error"
                    if row.get("successful"):
                        result = "Success"
                    self.tree.insert("", "end", values=(row.get("user_login"), row.get("user_name"), row.get("ip_address"), row.get("login_time"), result))
        except requests.exceptions.RequestException as e:
            print(f"Error in the request: {e}")
