import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from fuzzywuzzy import fuzz
from db import fetch_all_services, fetch_customers_by_name, fetch_last_order_id, create_order
import requests
from barcode import EAN13
from barcode.writer import ImageWriter
import re
from fpdf import FPDF
from datetime import datetime
import base64
from reportlab.graphics import barcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import random

class CreateOrderFrame:
    def __init__(self, root, user_info):
        self.root = root
        self.user_info = user_info
        self.root.title("Create New Order")
        self.root.geometry("800x600")
        self.root.minsize("800","600")
        self.root.configure(bg="white")
        style = ttk.Style()
        self.customers = []
        self.selected_customer_var = tk.StringVar()
        self.selected_service_var = tk.StringVar()
        self.quantity_var = tk.IntVar()
        self.barcode_var = tk.StringVar()
        self.order_price_var = tk.StringVar()
        ttk.Label(self.root, text="Please fill the following data").pack(padx=10, pady=10)
        self.order_frame = ttk.Frame(self.root, padding=(20, 20))
        self.order_frame.pack(padx=10, pady=10)
        self.fetch_last_order_id()
        self.create_barcode_widget()

    def fetch_last_order_id(self):
        self.service_names = []
        try:
            response = fetch_last_order_id()
            if response.get("error_message"):
                messagebox.showerror("Operation Failed", "Failed to fetch latest order data. Please try again")
            else:
                self.last_order_id = tk.IntVar(value=response['data'])
        except requests.exceptions.RequestException as e:
            print(f"Error in the request: {e}")

    def create_services_values(self):
        self.service_names = []
        try:
            response = fetch_all_services()
            self.services = response['data']
            for row in response['data']:
                self.service_names.append(f"{row['service']} ({row['code']})")
        except requests.exceptions.RequestException as e:
            print(f"Error in the request: {e}")

    def create_barcode_widget(self):
        self.barcode_var.set(f"{self.last_order_id.get()}{datetime.now().strftime('%Y%m%d')}{random.randint(100000, 999999)}")
        ttk.Label(self.order_frame, text="Barcode:").grid(row=0, column=0, padx=10, pady=10)
        self.barcode_entry = ttk.Entry(self.order_frame, textvariable=self.barcode_var, width = 37, font = ("Helvetica", 10))
        self.barcode_entry.grid(row=0, column=1, padx=10, pady=10)
        self.barcode_entry.bind("<Return>", self.generate_barcode)

    def create_order_detail_widgets(self):
        ttk.Label(self.order_frame, text="Customer:").grid(row=1, column=0, padx=10, pady=10)
        self.customer_combobox = ttk.Combobox(self.order_frame, textvariable=self.selected_customer_var, values=[], font = ("Helvetica", 10), width = 35, height = 50)
        self.customer_combobox.grid(row=1, column=1, padx=10, pady=10)
        self.customer_combobox.bind("<KeyRelease>", self.filter_customers)
        self.customer_combobox.bind("<<ComboboxSelected>>", self.get_id_of_selected_customer)
        self.customer_combobox.focus_set()
        ttk.Label(self.order_frame, text="Service:").grid(row=2, column=0, padx=10, pady=10)
        self.service_combobox = ttk.Combobox(self.order_frame, textvariable=self.selected_service_var, values=[], font = ("Helvetica", 10), width = 35, height = 50)
        self.service_combobox.grid(row=2, column=1, padx=10, pady=10)
        self.service_combobox.bind("<KeyRelease>", self.filter_services)
        self.service_combobox.bind("<<ComboboxSelected>>", self.update_cost_based_on_selected_service)
        ttk.Label(self.order_frame, text="Order Cost:").grid(row=4, column=0, padx=10, pady=10)
        ttk.Entry(self.order_frame, textvariable=self.order_price_var, state='readonly', width = 37, font = ("Helvetica", 10)).grid(row=4, column=1, padx=10, pady=10)
        ttk.Button(self.order_frame, text="Generate Order", command=self.generate_order).grid(row=5, columnspan=2, pady=10)

    def filter_customers(self, event):
        filter_text = self.selected_customer_var.get().strip()
        if not filter_text:
            self.customer_combobox['values'] = []
        else:
            response = fetch_customers_by_name(filter_text)
            filtered_customers = []
            self.customers = response['data']
            for row in response['data']:
                filtered_customers.append(row['name'])
            self.customer_combobox['values'] = filtered_customers

    def filter_services(self, event):
        filter_text = self.selected_service_var.get().strip()
        if not filter_text:
            self.service_combobox['values'] = []
        else:
            filtered_services = [service for service in self.service_names if fuzz.partial_ratio(filter_text, service) >= 50]
            self.service_combobox['values'] = filtered_services

    def generate_barcode(self, event):
        PAGESIZE = A4
        barcode_text = self.barcode_var.get().strip()
        if int(barcode_text[:-14]) >= int(self.last_order_id.get()):
            myCanvas = canvas.Canvas(F'orders/Barcode_{barcode_text}.pdf', pagesize=PAGESIZE)
            newBarcode = barcode.createBarcodeDrawing('EAN13', value=barcode_text)
            newBarcode.drawOn(myCanvas, 100, 100)
            myCanvas.save()
            self.create_services_values()
            self.barcode_entry.config(state='disabled')
            messagebox.showinfo("Barcode Generated", f"Barcode saved to barcode_{barcode_text}.pdf")
            self.create_order_detail_widgets()
        else:
            messagebox.showerror("Input Error", "Order ID already exists.")

    def update_cost_based_on_selected_service(self, event):
        value = event.widget.get()
        pattern = r'\b(\d+)\b'
        matches = re.findall(pattern, value)
        service_code = int(matches[0])
        self.selected_service_id = tk.IntVar()
        for service in self.services:
            if service['code'] == service_code:
                self.order_price_var.set(f"{service['price']}")
                self.selected_service_id.set(service['id'])
                return 

    def get_id_of_selected_customer(self, event):
        value = event.widget.get()
        self.selected_customer_id = tk.IntVar()
        self.selected_customer_company = tk.StringVar()
        for customer in self.customers:
            if customer['name'] == value:
                self.selected_customer_id.set(customer['id'])
                self.selected_customer_company.set(customer['company_name'])
                return

    def generate_order(self):
        order_id = self.last_order_id.get()
        bar_code = self.barcode_var.get()
        customer_id = self.selected_customer_id.get()
        customer_name = self.selected_customer_var.get()
        company_name = self.selected_customer_company.get()
        service_id = self.selected_service_id.get()
        service_name = self.selected_service_var.get()
        cost = self.order_price_var.get()
        if not bar_code or not customer_name or not service_name:
            messagebox.showerror("Error", "Please fill in all the fields.")
            return

        data = {
           'order_id': order_id, 
           'bar_code': bar_code, 
           'customer_id': customer_id, 
           'customer_name': customer_name, 
           'service_id': service_id, 
           'cost': cost,
           'user_id': self.user_info['id'],
           'service_name': service_name,
           'company_name': company_name
        }
        try:
            response = create_order(data)
            if response.get("error_message"):
                messagebox.showerror("Request Failed", response.get("error_message"))
            else:
                self.generate_pdf_and_base64_link_of_order(data)
                self.root.destroy()
                messagebox.showinfo("Success", "Order created successfully")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Request Error", "Error in the request")

    def generate_pdf_and_base64_link_of_order(self, data):
        order_date = datetime.now()
        order_text = f"Order Number: {data['order_id']}\n"
        order_text += f"Order Date: {order_date}\n"
        order_text += f"Case Code: {data['bar_code']}\n"
        order_text += f"Customer Name: {data['customer_name']}\n"
        order_text += f"Requested Service: {data['service_name']}\n"
        order_text += f"Cost: {data['cost']}\n"
        base64_link = self.generate_base64_link(order_text)
        with open("orders/order_links.txt", "a") as file:
            file.write(f'{base64_link} \n')

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Order Number: {data['order_id']}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Order Date: {order_date}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Case Code: {data['bar_code']}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Customer Name: {data['customer_name']}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Requested Service: {data['service_name']}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Total Cost: {data['cost']}", ln=True, align='L')
        # pdf.cell(200, 10, txt=f"Company: {}\n", ln=True, align='L')
        # pdf.cell(200, 10, txt=f"Date of Birth: {}\n", ln=True, align='L')
        pdf_filename = f"Order_{self.barcode_var.get()}.pdf"
        pdf.output(f'orders/{pdf_filename}')

    def generate_base64_link(self, order_info):
        encoded_order_info = base64.b64encode(order_info.encode()).decode()
        return encoded_order_info
