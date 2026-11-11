import os
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import sys
class RestaurantDataViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Data Display System")  # Translated
        self.root.geometry("1000x600")
        self.root.resizable(True, True)

        # Set Chinese font
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("SimHei", 10, "bold"))
        self.style.configure("Treeview", font=("SimHei", 10))
        self.style.configure("TButton", font=("SimHei", 10))
        self.style.configure("TNotebook.Tab", font=("SimHei", 10))

        # Create notebook widget
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tabs
        self.customer_frame = ttk.Frame(self.notebook)
        self.inventory_frame = ttk.Frame(self.notebook)
        self.order_frame = ttk.Frame(self.notebook)
        self.budget_frame = ttk.Frame(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.customer_frame, text="Customer Information")  # Translated
        self.notebook.add(self.inventory_frame, text="Inventory")  # Translated
        self.notebook.add(self.order_frame, text="Order Information")  # Translated
        self.notebook.add(self.budget_frame, text="Budget Information")  # Translated

        # Create refresh button
        self.refresh_btn = ttk.Button(root, text="Refresh Data", command=self.refresh_all_data)  # Translated
        self.refresh_btn.pack(pady=10)

        # Create tables
        self.create_customer_table()
        self.create_inventory_table()
        self.create_order_table()
        self.create_budget_table()

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

        # Initial data load
        self.refresh_all_data()

    def create_customer_table(self):
        # Create customer table
        columns = ("customer_id", "first_name", "last_name", "phone", "email", "address", "reg_date")
        self.customer_tree = ttk.Treeview(self.customer_frame, columns=columns, show="headings")

        # Set column widths and headings
        self.customer_tree.column("customer_id", width=80, anchor=tk.CENTER)
        self.customer_tree.column("first_name", width=80, anchor=tk.CENTER)
        self.customer_tree.column("last_name", width=80, anchor=tk.CENTER)
        self.customer_tree.column("phone", width=120, anchor=tk.CENTER)
        self.customer_tree.column("email", width=200, anchor=tk.CENTER)
        self.customer_tree.column("address", width=250, anchor=tk.CENTER)
        self.customer_tree.column("reg_date", width=100, anchor=tk.CENTER)

        self.customer_tree.heading("customer_id", text="Customer ID")  # Translated
        self.customer_tree.heading("first_name", text="First Name")  # Translated
        self.customer_tree.heading("last_name", text="Last Name")  # Translated
        self.customer_tree.heading("phone", text="Phone Number")  # Translated
        self.customer_tree.heading("email", text="Email")  # Translated
        self.customer_tree.heading("address", text="Address")  # Translated
        self.customer_tree.heading("reg_date", text="Registration Date")  # Translated

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.customer_frame, orient=tk.VERTICAL, command=self.customer_tree.yview)
        self.customer_tree.configure(yscroll=scrollbar.set)

        # Layout
        self.customer_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_inventory_table(self):
        # Create inventory table
        columns = ("ingredient_id", "name", "quantity", "exp_date", "purchase_date")
        self.inventory_tree = ttk.Treeview(self.inventory_frame, columns=columns, show="headings")

        # Set column widths and headings
        self.inventory_tree.column("ingredient_id", width=100, anchor=tk.CENTER)
        self.inventory_tree.column("name", width=150, anchor=tk.CENTER)
        self.inventory_tree.column("quantity", width=100, anchor=tk.CENTER)
        self.inventory_tree.column("exp_date", width=120, anchor=tk.CENTER)
        self.inventory_tree.column("purchase_date", width=120, anchor=tk.CENTER)

        self.inventory_tree.heading("ingredient_id", text="Ingredient ID")  # Translated
        self.inventory_tree.heading("name", text="Ingredient Name")  # Translated
        self.inventory_tree.heading("quantity", text="Quantity")  # Translated
        self.inventory_tree.heading("exp_date", text="Expiration Date")  # Translated
        self.inventory_tree.heading("purchase_date", text="Purchase Date")  # Translated

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.inventory_frame, orient=tk.VERTICAL, command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscroll=scrollbar.set)

        # Layout
        self.inventory_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_order_table(self):
        # Create order table
        columns = ("order_id", "customer_id", "order_date", "delivery_date", "status", "total_amount")
        self.order_tree = ttk.Treeview(self.order_frame, columns=columns, show="headings")

        # Set column widths and headings
        self.order_tree.column("order_id", width=100, anchor=tk.CENTER)
        self.order_tree.column("customer_id", width=100, anchor=tk.CENTER)
        self.order_tree.column("order_date", width=150, anchor=tk.CENTER)
        self.order_tree.column("delivery_date", width=150, anchor=tk.CENTER)
        self.order_tree.column("status", width=100, anchor=tk.CENTER)
        self.order_tree.column("total_amount", width=120, anchor=tk.CENTER)

        self.order_tree.heading("order_id", text="Order ID")  # Translated
        self.order_tree.heading("customer_id", text="Customer ID")  # Translated
        self.order_tree.heading("order_date", text="Order Date")  # Translated
        self.order_tree.heading("delivery_date", text="Delivery Date")  # Translated
        self.order_tree.heading("status", text="Order Status")  # Translated
        self.order_tree.heading("total_amount", text="Total Amount")  # Translated

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.order_frame, orient=tk.VERTICAL, command=self.order_tree.yview)
        self.order_tree.configure(yscroll=scrollbar.set)

        # Layout
        self.order_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_budget_table(self):
        # Create budget table
        columns = ("expense_id", "type", "name", "amount", "date")
        self.budget_tree = ttk.Treeview(self.budget_frame, columns=columns, show="headings")

        # Set column widths and headings
        self.budget_tree.column("expense_id", width=100, anchor=tk.CENTER)
        self.budget_tree.column("type", width=100, anchor=tk.CENTER)
        self.budget_tree.column("name", width=150, anchor=tk.CENTER)
        self.budget_tree.column("amount", width=120, anchor=tk.CENTER)
        self.budget_tree.column("date", width=120, anchor=tk.CENTER)

        self.budget_tree.heading("expense_id", text="Expense ID")  # Translated
        self.budget_tree.heading("type", text="Expense Type")  # Translated
        self.budget_tree.heading("name", text="Expense Name")  # Translated
        self.budget_tree.heading("amount", text="Amount")  # Translated
        self.budget_tree.heading("date", text="Date")  # Translated

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.budget_frame, orient=tk.VERTICAL, command=self.budget_tree.yview)
        self.budget_tree.configure(yscroll=scrollbar.set)

        # Layout
        self.budget_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def get_db_connection(self):
        # Database connection configuration - modify as needed
        connection = None
        try:
            connection = mysql.connector.connect(
                host='localhost',  # Database host
                database='restaurant_test1',  # Database name
                user='root',       # Database username
                password=self.db_config['password'],  # Use password from login
                charset='utf8mb4'
            )
        except Error as e:
            messagebox.showerror("Database Connection Error", f"Failed to connect to database: {str(e)}")  # Translated
        return connection

    def clear_treeview(self, tree):
        # Clear table data
        for item in tree.get_children():
            tree.delete(item)

    def load_customer_data(self):
        # Load customer data
        connection = self.get_db_connection()
        if connection is None:
            return

        try:
            cursor = connection.cursor()
            query = """SELECT customer_id, first_name, last_name, customer_phone_number, 
                          customer_email, customer_address, customer_registration_date 
                       FROM customer ORDER BY customer_id"""
            cursor.execute(query)
            records = cursor.fetchall()

            self.clear_treeview(self.customer_tree)
            for row in records:
                self.customer_tree.insert('', tk.END, values=row)
        except Error as e:
            messagebox.showerror("Data Loading Error", f"Failed to load customer data: {str(e)}")  # Translated
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def load_inventory_data(self):
        # Load inventory data
        connection = self.get_db_connection()
        if connection is None:
            return

        try:
            cursor = connection.cursor()
            query = """SELECT i.ingredient_id, i.ingredient_name, ip.quantity_on_hand, 
                          ip.ingredient_expiration_date, ip.purchase_date 
                       FROM ingredient i
                       JOIN ingredient_purchase ip ON i.ingredient_id = ip.ingredient_id
                       ORDER BY i.ingredient_id"""
            cursor.execute(query)
            records = cursor.fetchall()

            self.clear_treeview(self.inventory_tree)
            for row in records:
                self.inventory_tree.insert('', tk.END, values=row)
        except Error as e:
            messagebox.showerror("Data Loading Error", f"Failed to load inventory data: {str(e)}")  # Translated
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def load_order_data(self):
        # Load order data
        connection = self.get_db_connection()
        if connection is None:
            return

        try:
            cursor = connection.cursor()
            query = """SELECT co.customer_order_id, co.customer_id, co.customer_order_date, 
                          co.customer_delivery_date, co.customer_order_status, 
                          SUM(oli.meal_price * oli.customer_quantity_ordered) as total_amount
                       FROM customer_order co
                       JOIN order_line_item oli ON co.customer_order_id = oli.customer_order_id
                       GROUP BY co.customer_order_id
                       ORDER BY co.customer_order_id"""
            cursor.execute(query)
            records = cursor.fetchall()

            self.clear_treeview(self.order_tree)
            for row in records:
                # Format currency display
                formatted_row = list(row)
                formatted_row[-1] = f"${formatted_row[-1]:.2f}" if formatted_row[-1] else "$0.00"
                self.order_tree.insert('', tk.END, values=formatted_row)
        except Error as e:
            messagebox.showerror("Data Loading Error", f"Failed to load order data: {str(e)}")  # Translated
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def load_budget_data(self):
        # Load budget data
        connection = self.get_db_connection()
        if connection is None:
            return

        try:
            cursor = connection.cursor()
            query = """SELECT expense_id, expense_type, expense_name, expense_amount, expense_date 
                       FROM expense ORDER BY expense_date DESC"""
            cursor.execute(query)
            records = cursor.fetchall()

            self.clear_treeview(self.budget_tree)
            for row in records:
                # Format currency display
                formatted_row = list(row)
                formatted_row[-2] = f"${formatted_row[-2]:.2f}"
                self.budget_tree.insert('', tk.END, values=formatted_row)
        except Error as e:
            messagebox.showerror("Data Loading Error", f"Failed to load budget data: {str(e)}")  # Translated
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def refresh_all_data(self):
        # Refresh all data
        self.load_customer_data()
        self.load_inventory_data()
        self.load_order_data()
        self.load_budget_data()
        messagebox.showinfo("Refresh Successful", "All data has been refreshed successfully")  # Translated

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantDataViewer(root)
    root.iconbitmap("logo.ico")
    root.mainloop()