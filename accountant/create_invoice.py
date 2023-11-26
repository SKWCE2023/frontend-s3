import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from fpdf import FPDF
import csv
from tkcalendar import DateEntry
from db import fetch_customers_by_name, fetch_services_by_period_and_customer, fetch_company_by_name

class CreateInvoiceFrame:
    def __init__(self, root):
        self.root = root
        self.root.title("Invoice Generator")
        self.root.geometry("800x600")
        self.root.minsize("800","600")
        self.root.configure(bg="white")
        self.legal_entity_data = {}
        self.individual_data = {}
        self.style = ttk.Style()
        self.style.configure("TLabel", background="white", font=('Helvetica', 12))
        self.invoice_frame = ttk.Frame(self.root, padding=(20, 20))
        self.invoice_frame.pack(padx=10, pady=10)
        self.invoice_type_var = tk.StringVar()
        self.period_start_var = tk.StringVar()
        self.period_end_var = tk.StringVar()
        self.customers = []
        self.selected_customer_var = tk.StringVar()
        self.selected_company_var = tk.StringVar()
        self.selected_customer = None
        self.create_invoice_type_widget()

    def create_invoice_type_widget(self):
        ttk.Label(self.invoice_frame, text="Invoice Type:", style="TLabel").grid(row=0, column=0, padx=10, pady=10)
        invoice_type_combobox = ttk.Combobox(self.invoice_frame, textvariable=self.invoice_type_var, values=["Legal Entity", "Individual"], font = ("Helvetica", 10), width = 35)
        invoice_type_combobox.grid(row=0, column=1, padx=10, pady=10)
        invoice_type_combobox.bind("<<ComboboxSelected>>", self.add_widgets_based_on_invoice_type)

    def add_widgets_based_on_invoice_type(self, event):
        if self.invoice_type_var.get() == "Legal Entity":
            ttk.Label(self.invoice_frame, text="Company:", style="TLabel").grid(row=1, column=0, padx=10, pady=10)
            self.company_combobox = ttk.Combobox(self.invoice_frame, textvariable=self.selected_company_var, values=[], font = ("Helvetica", 10), width = 35, height = 50)
            self.company_combobox.grid(row=1, column=1, padx=10, pady=10)
            self.company_combobox.bind("<KeyRelease>", self.filter_companies)
        elif self.invoice_type_var.get() == "Individual":
            ttk.Label(self.invoice_frame, text="Customer:", style="TLabel").grid(row=1, column=0, padx=10, pady=10)
            self.customer_combobox = ttk.Combobox(self.invoice_frame, textvariable=self.selected_customer_var, values=[], font = ("Helvetica", 10), width = 35, height = 50)
            self.customer_combobox.grid(row=1, column=1, padx=10, pady=10)
            self.customer_combobox.bind("<KeyRelease>", self.filter_customers)
            self.customer_combobox.bind("<<ComboboxSelected>>", self.get_data_of_selected_customer)
            
        ttk.Label(self.invoice_frame, text="Period Start:", style="TLabel").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.period_start = DateEntry(self.invoice_frame, selectmode='day', textvariable=self.period_start_var, width = 35, font = ("Helvetica", 10))
        self.period_start.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(self.invoice_frame, text="Period End:", style="TLabel").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.period_end = DateEntry(self.invoice_frame, selectmode='day', textvariable=self.period_end_var, width = 35, font = ("Helvetica", 10))
        self.period_end.grid(row=3, column=1, padx=10, pady=10)

        generate_button = ttk.Button(self.invoice_frame, text="Generate Invoice", command=self.generate_invoice)
        generate_button.grid(row=4, column=0, columnspan=2, pady=10)
    
    def generate_invoice(self):
        invoice_type = self.invoice_type_var.get()
        period_start = self.period_start.get_date().strftime("%d/%m/%Y")
        period_end = self.period_end.get_date().strftime("%d/%m/%Y")
        self.fetch_services()
        data = self.biling_data
        pdf_filename = f"{invoice_type}_Invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        self.generate_pdf_invoice(pdf_filename, data, period_start, period_end)
        self.save_to_csv(data, period_start, period_end)
        messagebox.showinfo("Invoice Generated", f"Invoice PDF generated successfully \n CSV entry added successfully \n Please check invoices folder")
        self.root.destroy()

    def generate_pdf_invoice(self, filename, data, period_start, period_end):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        pdf.cell(200, 10, txt=f"Invoice Type: {self.invoice_type_var.get()}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Period: {period_start} to {period_end}", ln=True, align='L')
        if self.invoice_type_var.get() == "Legal Entity":
            pdf.cell(200, 10, txt=f"Company Name: {data['company_name']}", ln=True, align='L')
        elif self.invoice_type_var.get() == "Individual":
            pdf.cell(200, 10, txt=f"Customer Name: {data['full_name']}", ln=True, align='L')
            pdf.cell(200, 10, txt=f"Phone Number: {data['phone_number']}", ln=True, align='L')
        pdf.cell(200, 10, txt="Services:", ln=True, align='L')
        for service, cost in data['services'].items():
            pdf.cell(200, 10, txt=f"    - {service}: {cost}", ln=True, align='L')
        total_cost = sum(data['services'].values())
        pdf.cell(200, 10, txt=f"Total Cost: {total_cost}", ln=True, align='L')
        pdf.output(f'invoices/{filename}')

    def save_to_csv(self, data, period_start, period_end):
        with open('invoices/invoices_csv.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(["Invoice Type", "Period Start", "Period End", "Details"])
            writer.writerow([self.invoice_type_var.get(), period_start, period_end, data])

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
    
    def get_data_of_selected_customer(self, event):
        value = event.widget.get()
        self.selected_customer_id = tk.IntVar()
        for customer in self.customers:
            if customer['name'] == value:
                self.selected_customer = customer
                break

    def fetch_services(self):
        invoice_type = self.invoice_type_var.get()
        company_name = self.selected_company_var.get()
        period_start = self.period_start.get_date()
        period_end = self.period_end.get_date()
        customer_id = self.selected_customer['id'] if self.selected_customer else 0
        response = {}
        response = fetch_services_by_period_and_customer(period_start, period_end, customer_id, company_name)
        if response.get("error_message"):
            messagebox.showerror("Request Failed", "Failed to fetch services. Please try again")
        else:
            services = {}
            for row in response['data']:
                services[row['service']] = row['price']
                if invoice_type == "Legal Entity":
                    self.biling_data = {
                        "company_name": company_name,
                        "services": services
                    }
                elif invoice_type == "Individual":
                    self.biling_data = {
                        "full_name": self.selected_customer['name'],
                        "phone_number": self.selected_customer['phone'],
                        "services": services
                    }

    def filter_companies(self, event):
        filter_text = self.selected_company_var.get().strip()
        if not filter_text:
            self.company_combobox['values'] = []
        else:
            response = fetch_company_by_name(filter_text)
            filtered_companies = []
            self.companies = response['data']
            for row in response['data']:
                filtered_companies.append(row['name'])
            self.company_combobox['values'] = filtered_companies
