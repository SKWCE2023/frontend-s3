import tkinter as tk
from tkinter import ttk
import requests
from db import fetch_all_orders

class OrdersWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Orders List")
        self.root.geometry("800x600")
        self.root.minsize("800","600")
        self.root.configure(bg="white")
        self.tree = ttk.Treeview(root, columns=("ID", "Creation Date", "Order Status", "Service Status"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("#1", text="Creation Date")
        self.tree.heading("#2", text="Order Status")
        self.tree.heading("#3", text="Service Status")
        self.tree.pack(pady=10)
        self.fetch_orders()

    def fetch_orders(self):
        try:
            response = fetch_all_orders()
            if response.get("error_message"):
                messagebox.showerror("Request Failed", "Failed to fetch orders. Please try again")
                self.root.destroy()
            else:
                orders = response.get('data', [])
                for item in self.tree.get_children():
                    self.tree.delete(item)
                for order in orders:
                    self.tree.insert("", "end", values=(
                        order['id'],
                        order['creation_date'],
                        order['order_status'],
                        order['service_status']
                    ))
        except requests.RequestException as e:
            print(f"Error fetching orders: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OrdersWindow(root)
    root.mainloop()
