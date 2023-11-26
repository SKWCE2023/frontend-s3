import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
import requests
from db import create_customer, fetch_company_by_name
from tkcalendar import DateEntry

class AddClientFrame:
    def __init__(self, root):
        self.root = root
        img = PhotoImage(file='assets/images/Logo.png')
        self.root.iconphoto(False, img)
        self.root.title("Add New Client")
        self.root.geometry("800x600")
        self.root.minsize("800","600")
        self.root.configure(bg="white")
        ttk.Label(self.root, text="Please fill the following data").pack(padx=10, pady=10)
        self.frame = ttk.Frame(self.root, padding=(20, 20))
        self.frame.pack(padx=10, pady=10)
        labels = ['First Name', 'Last Name', 'Login', 'Password', 'Date of Birth', 'Passport Series', 'Passport Number', 'Phone Number', 'Email', 'Company Name']
        self.entries = {}
        self.selected_company_var = tk.StringVar()
        for i, label_text in enumerate(labels):
            key = label_text.lower().replace(' ', '_')
            label = ttk.Label(self.frame, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=10, sticky=tk.W)
            if key == 'date_of_birth':
                entry = DateEntry(self.frame, selectmode='day', textvariable=key, width = 35, font = ("Helvetica", 10))
            elif key == 'phone_number':
                entry = ttk.Entry(self.frame, width = 37, font = ("Helvetica", 10))
                entry.insert(0, '+{country_code}{number}')
                entry.configure(foreground="gray")
                entry.bind("<FocusIn>", self.on_entry_focus_in)
                entry.bind("<FocusOut>", self.on_entry_focus_out)
            elif key == 'company_name':
                entry = ttk.Combobox(self.frame, textvariable=self.selected_company_var, values=[], font = ("Helvetica", 10), width = 35, height = 50)
                entry.grid(row=i, column=1, padx=10, pady=10)
                entry.bind("<KeyRelease>", self.filter_companies)
            else:
                entry = ttk.Entry(self.frame, width = 37, font = ("Helvetica", 10))
            entry.grid(row=i, column=1, padx=10, pady=10)
            self.entries[key] = entry
        add_button = ttk.Button(self.frame, text="Add Client", command=self.add_client)
        add_button.grid(row=len(labels), column=0, columnspan=2, pady=14)

    def add_client(self):
        try:
            data = {}
            for key, entry in self.entries.items():
                if not entry.get() and key != 'company_name':
                    messagebox.showerror("Error", "Please fill in all the fields.")
                    return
                if key == 'date_of_birth':
                    data[key] = entry.get_date().strftime("%d/%m/%Y")
                else:
                    data[key] = entry.get()
            response = create_customer(data)
            if response.get("error_message"):
                messagebox.showerror("Operation Failed", "Failed to add customer. Please try again")
            else:
                messagebox.showinfo("Success", "Customer added successfully")
                self.root.destroy()
        except requests.exceptions.RequestException as e:
            print(f"Error in the request: {e}")

    def on_entry_focus_in(self, event):
        entry = self.entries['phone_number']
        if entry.get() == '+{country_code}{number}':
            entry.delete(0, tk.END)
            entry.configure(show="")
            entry.configure(foreground="black")

    def on_entry_focus_out(self, event):
        entry = self.entries['phone_number']
        if entry.get() == '':
            entry.insert(0, '+{country_code}{number}')
            entry.configure(show="")
            entry.configure(foreground="gray")

    def filter_companies(self, event):
        filter_text = self.selected_company_var.get().strip()
        if not filter_text:
            self.entries['company_name']['values'] = []
        else:
            response = fetch_company_by_name(filter_text)
            filtered_companies = []
            self.companies = response['data']
            for row in response['data']:
                filtered_companies.append(row['name'])
            self.entries['company_name']['values'] = filtered_companies