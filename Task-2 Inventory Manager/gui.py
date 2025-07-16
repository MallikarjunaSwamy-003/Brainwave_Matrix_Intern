import tkinter as tk
from tkinter import messagebox, simpledialog
from auth import login_user, register_user
from inventory import *
from db import init_db

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Manager")
        self.root.geometry("800x600")
        init_db()
        self.login_screen()

    def login_screen(self):
        self.clear_window()
        tk.Label(self.root, text="Login", font=("Arial", 16)).pack()
        self.username = tk.Entry(self.root)
        self.username.pack()
        self.password = tk.Entry(self.root, show="*")
        self.password.pack()
        tk.Button(self.root, text="Login", command=self.login).pack()
        tk.Button(self.root, text="Register", command=self.register).pack()

    def login(self):
        user = self.username.get()
        pwd = self.password.get()
        if login_user(user, pwd):
            self.dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    def register(self):
        user = self.username.get()
        pwd = self.password.get()
        if register_user(user, pwd):
            messagebox.showinfo("Success", "User Registered")
        else:
            messagebox.showerror("Error", "Username already exists")

    def dashboard(self):
        self.clear_window()
        tk.Label(self.root, text="Inventory Dashboard", font=("Arial", 16)).pack()
        tk.Button(self.root, text="Add Product", command=self.add_product_ui).pack()
        tk.Button(self.root, text="View Inventory", command=self.view_inventory).pack()
        tk.Button(self.root, text="Low Stock Alerts", command=self.low_stock_alert).pack()
        tk.Button(self.root, text="Sales Summary", command=self.sales_summary).pack()

    def add_product_ui(self):
        name = simpledialog.askstring("Product Name", "Enter product name:")
        qty = simpledialog.askinteger("Quantity", "Enter quantity:")
        price = simpledialog.askfloat("Price", "Enter price:")
        if name and qty is not None and price is not None:
            add_product(name, qty, price)
            messagebox.showinfo("Success", "Product Added!")

    def view_inventory(self):
        self.clear_window()
        tk.Label(self.root, text="Inventory", font=("Arial", 16)).grid(row=0, column=0, columnspan=5)

        headers = ["ID", "Name", "Quantity", "Price"]
        for i, h in enumerate(headers):
            tk.Label(self.root, text=h, borderwidth=2, relief="groove", width=15).grid(row=1, column=i)

        products = get_all_products()
        self.selected_product_id = tk.StringVar()

        for r, row in enumerate(products, start=2):
            for c, value in enumerate(row):
                tk.Label(self.root, text=value, borderwidth=1, relief="ridge", width=15).grid(row=r, column=c)
            tk.Radiobutton(self.root, variable=self.selected_product_id, value=row[0]).grid(row=r, column=len(row))

        tk.Button(self.root, text="Edit Selected", command=self.edit_selected_product).grid(row=r+1, column=0)
        tk.Button(self.root, text="Delete Selected", command=self.delete_selected_product).grid(row=r+1, column=1)
        tk.Button(self.root, text="Back", command=self.dashboard).grid(row=r+1, column=2)

    def low_stock_alert(self):
        items = get_low_stock()
        self.display_data(items, ["ID", "Name", "Quantity", "Price"])

    def sales_summary(self):
        sales = get_sales_summary()
        self.display_data(sales, ["Product", "Qty Sold", "Total Revenue"])

    def display_data(self, data, headers):
        self.clear_window()
        for i, h in enumerate(headers):
            tk.Label(self.root, text=h, borderwidth=2, relief="groove").grid(row=0, column=i)
        for r, row in enumerate(data, start=1):
            for c, value in enumerate(row):
                tk.Label(self.root, text=value, borderwidth=1, relief="ridge").grid(row=r, column=c)
        tk.Button(self.root, text="Back", command=self.dashboard).grid(row=r+1, column=0, columnspan=2)

    def edit_selected_product(self):
        product_id = self.selected_product_id.get()
        if not product_id:
            messagebox.showwarning("No Selection", "Please select a product to edit.")
            return
        product_id = int(product_id)
        name = simpledialog.askstring("Edit Name", "Enter new product name:")
        quantity = simpledialog.askinteger("Edit Quantity", "Enter new quantity:")
        price = simpledialog.askfloat("Edit Price", "Enter new price:")
        if name and quantity is not None and price is not None:
            edit_product(product_id, name, quantity, price)
            messagebox.showinfo("Updated", "Product updated successfully.")
            self.view_inventory()

    def delete_selected_product(self):
        product_id = self.selected_product_id.get()
        if not product_id:
            messagebox.showwarning("No Selection", "Please select a product to delete.")
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?")
        if confirm:
            delete_product(int(product_id))
            messagebox.showinfo("Deleted", "Product deleted successfully.")
            self.view_inventory()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
