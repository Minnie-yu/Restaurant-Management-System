import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
from mysql.connector import Error
import sys
class CustomerOrderViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Information and Order Management System")
        self.root.geometry("1000x600")

        # Database connection
        self.db_connection = None
        if len(sys.argv) > 1:
            db_password = sys.argv[1]
        else:
            db_password = os.environ.get('MYSQL_PASSWORD', '')  # 默认密码

        # 使用传入的密码
        self.db_config = {
            'host': 'localhost',
            'database': 'restaurant_test1',
            'user': 'root',
            'password': db_password
        }

        self.connection = None
        self.cursor = None

        # Create UI
        self.create_widgets()

        # Connect to database and load data
        self.connect_to_database()
        self.load_customers()

    def create_widgets(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Customer information area
        customer_frame = ttk.LabelFrame(main_frame, text="Customer Information", padding="10")
        customer_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Customer table
        columns = ("customer_id", "name", "phone", "email", "address")
        self.customer_tree = ttk.Treeview(customer_frame, columns=columns, show="headings")
        for col in columns:
            self.customer_tree.heading(col, text=col)
            self.customer_tree.column(col, width=100)
        self.customer_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(customer_frame, orient=tk.VERTICAL, command=self.customer_tree.yview)
        self.customer_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Button frame
        button_frame = ttk.Frame(customer_frame, padding="10")
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons
        self.add_btn = ttk.Button(button_frame, text="Add Customer", command=self.add_customer)
        self.add_btn.pack(fill=tk.X, pady=(0, 5))

        self.edit_btn = ttk.Button(button_frame, text="Edit Customer", command=self.edit_customer)
        self.edit_btn.pack(fill=tk.X, pady=(0, 5))
        # Order history area
        self.order_frame = ttk.LabelFrame(main_frame, text="Order History", padding="10")
        self.order_frame.pack(fill=tk.BOTH, expand=True)

        # Order table
        order_columns = ("order_id", "date", "total", "status")
        self.order_tree = ttk.Treeview(self.order_frame, columns=order_columns, show="headings")
        for col in order_columns:
            self.order_tree.heading(col, text=col)
            self.order_tree.column(col, width=100)
        self.order_tree.pack(fill=tk.BOTH, expand=True)

        # Bind selection event
        self.customer_tree.bind("<<TreeviewSelect>>", self.on_customer_select)

        if len(sys.argv) > 1:
            db_password = sys.argv[1]
        else:
            db_password = os.environ.get('MYSQL_PASSWORD', '')  # 默认密码

            # 使用传入的密码
        self.db_config = {
            'host': 'localhost',
            'database': 'restaurant_test1',
            'user': 'root',
            'password': db_password
        }

    def connect_to_database(self):
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print("Database connection successful")
        except Error as e:
            messagebox.showerror("Database Error", f"Connection failed: {str(e)}")

    def load_customers(self):
        # Clear existing data
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)

        try:
            query = "SELECT customer_id, CONCAT(first_name, ' ', last_name) AS name, customer_phone_number AS phone, customer_email AS email, customer_address AS address FROM customer"
            self.cursor.execute(query)
            customers = self.cursor.fetchall()

            for customer in customers:
                self.customer_tree.insert('', tk.END, values=(
                    customer['customer_id'], 
                    customer['name'],
                    customer['phone'],
                    customer['email'],
                    customer['address']
                ))
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load customers: {str(e)}")

    def on_customer_select(self, event):
        # Automatically load orders when customer is selected
        self.view_orders()

    def view_orders(self):
        # Clear existing order data
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)

        selected_items = self.customer_tree.selection()
        if not selected_items:
            messagebox.showinfo("Notice", "Please select a customer first")
            return

        selected_item = selected_items[0]
        customer_data = self.customer_tree.item(selected_item, "values")
        if len(customer_data) == 0:
            messagebox.showwarning("Warning", "No customer data retrieved")
            return

        try:
            customer_id = customer_data[0]
            query = "SELECT co.customer_order_id AS order_id, co.customer_order_date AS date, SUM(oli.meal_price * oli.customer_quantity_ordered) AS total, co.customer_order_status AS status FROM customer_order co JOIN order_line_item oli ON co.customer_order_id = oli.customer_order_id WHERE co.customer_id = %s GROUP BY co.customer_order_id, co.customer_order_date, co.customer_order_status"
            self.cursor.execute(query, (customer_id,))
            orders = self.cursor.fetchall()

            if not orders:
                messagebox.showinfo("Notice", "This customer has no order history")
                return

            for order in orders:
                self.order_tree.insert('', tk.END, values=(
                    order['order_id'],
                    order['date'],
                    order['total'],
                    order['status']
                ))
        except IndexError:
            messagebox.showerror("Error", "Failed to get customer ID")
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load orders: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error occurred: {str(e)}")

    def add_customer(self):
        # Create add customer dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Customer")
        dialog.geometry("300x250")
        dialog.resizable(False, False)

        # Center the dialog
        dialog.transient(self.root)
        dialog.grab_set()

        # Create input fields
        fields = ["Name", "Phone", "Email", "Address"]
        entries = {}

        for i, field in enumerate(fields):
            ttk.Label(dialog, text=f"{field}:").grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
            entry = ttk.Entry(dialog, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[field] = entry

        def save_customer():
            name = entries["Name"].get().split()
            first_name = name[0] if len(name) > 0 else ''
            last_name = name[1] if len(name) > 1 else ''
            phone = entries["Phone"].get()
            email = entries["Email"].get()
            address = entries["Address"].get()

            if not name or not phone:
                messagebox.showwarning("Warning", "Name and phone cannot be empty")
                return

            try:
                query = "INSERT INTO customer (first_name, last_name, customer_phone_number, customer_email, customer_address, customer_registration_date) VALUES (%s, %s, %s, %s, %s, CURDATE())"
                self.cursor.execute(query, (first_name, last_name, phone, email, address))
                self.connection.commit()
                messagebox.showinfo("Success", "Customer added successfully")
                dialog.destroy()
                self.load_customers()
            except Error as e:
                self.connection.rollback()
                messagebox.showerror("Database Error", f"Failed to add customer: {str(e)}")

        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=15)

        ttk.Button(button_frame, text="Save", command=save_customer).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=10)

        dialog.wait_window()

    def edit_customer(self):
        selected_items = self.customer_tree.selection()
        if not selected_items:
            messagebox.showinfo("Notice", "Please select a customer first")
            return

        selected_item = selected_items[0]
        customer_data = self.customer_tree.item(selected_item, "values")
        customer_id = customer_data[0]

        # Create edit dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Customer Information")
        dialog.geometry("300x250")
        dialog.resizable(False, False)

        # Center the dialog
        dialog.transient(self.root)
        dialog.grab_set()

        # Create input fields
        fields = ["Name", "Phone", "Email", "Address"]
        entries = {}

        for i, (field, value) in enumerate(zip(fields, customer_data[1:])):
            ttk.Label(dialog, text=f"{field}:").grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
            entry = ttk.Entry(dialog, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry.insert(0, value)
            entries[field] = entry

        def update_customer():
            name = entries["Name"].get().split()
            first_name = name[0] if len(name) > 0 else ''
            last_name = name[1] if len(name) > 1 else ''
            phone = entries["Phone"].get()
            email = entries["Email"].get()
            address = entries["Address"].get()

            if not name or not phone:
                messagebox.showwarning("Warning", "Name and phone cannot be empty")
                return

            try:
                query = "UPDATE customer SET first_name = %s, last_name = %s, customer_phone_number = %s, customer_email = %s, customer_address = %s WHERE customer_id = %s"
                self.cursor.execute(query, (first_name, last_name, phone, email, address, customer_id))
                self.connection.commit()
                messagebox.showinfo("Success", "Customer information updated successfully")
                dialog.destroy()
                self.load_customers()
            except Error as e:
                self.connection.rollback()
                messagebox.showerror("Database Error", f"Failed to update customer: {str(e)}")

        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=15)

        ttk.Button(button_frame, text="Update", command=update_customer).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=10)

        dialog.wait_window()

    def close(self):
        # Explicitly close database connection
        if hasattr(self, 'connection') and self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

    def on_close(self):
        self.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerOrderViewer(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.iconbitmap("logo.ico")
    root.mainloop()