import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from PIL import Image, ImageTk
import sys

class InventoryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Ingredient Inventory Management System")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)

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

        # Set application icon
        try:
            self.root.iconbitmap("restaurant_icon.ico")
        except:
            pass

        # Set Chinese font (kept for character support)
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", font=("Microsoft YaHei", 10), padding=6)
        self.style.configure("TLabel", font=("Microsoft YaHei", 10), background="#f0f0f0")
        self.style.configure("Treeview.Heading", font=("Microsoft YaHei", 10, "bold"))
        self.style.configure("Treeview", font=("Microsoft YaHei", 10), rowheight=25)
        self.style.map("Treeview", background=[("selected", "#a6d8ff")])



        # Create main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        # Create left menu bar
        self.create_menu()

        # Create right content area
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Create three sub-pages
        self.create_real_time_inventory_page()
        self.create_cogs_page()
        self.create_inventory_detail_page()

        # Default to show real-time inventory page
        self.show_page("real_time_inventory")

        # Initialize data storage
        self.ingredient_data = self.load_ingredient_data()
        self.real_time_inventory = self.initialize_real_time_inventory()
        self.inventory_detail = self.initialize_inventory_detail()

        # Load data
        self.load_real_time_inventory()
        self.load_cogs_data()
        self.load_inventory_data()

        # Set window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def connect_to_database(self):
        """Connect to MySQL database"""
        try:
            self.db_connection = mysql.connector.connect(
                host='localhost',
                database='restaurant_test1',
                user='root',  # Please replace with your MySQL username
                password=self.db_config['password'],  # Use password from login
            )
            if self.db_connection.is_connected():
                db_info = self.db_connection.server_info
                print(f"Successfully connected to MySQL server version: {db_info}")
        except Error as e:
            messagebox.showerror("Database Connection Error",
                                 f"Connection failed: {str(e)}Please check database configuration and try again.")
            self.db_connection = None


    def load_ingredient_data(self):
        """Load ingredient data from database"""
        connection = self.create_db_connection()
        if connection is None:
            return []

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT ingredient_id, ingredient_name FROM ingredient")
            ingredients = []
            for (ingredient_id, ingredient_name) in cursor:
                # Set unit based on ingredient name
                if "Clams" in ingredient_name:
                    unit = "kg"
                elif "Potatoes" in ingredient_name:
                    unit = "kg"
                elif "Onions" in ingredient_name:
                    unit = "kg"
                elif "Celery" in ingredient_name:
                    unit = "kg"
                elif "Cream" in ingredient_name:
                    unit = "L"
                elif "Bread Bowl" in ingredient_name:
                    unit = "pcs"
                elif "Lobster" in ingredient_name:
                    unit = "kg"
                elif "Mayonnaise" in ingredient_name:
                    unit = "bottle"
                elif "Butter" in ingredient_name:
                    unit = "kg"
                elif "Buns" in ingredient_name:
                    unit = "pcs"
                elif "Coleslaw" in ingredient_name:
                    unit = "kg"
                elif "Apples" in ingredient_name:
                    unit = "kg"
                elif "Cinnamon" in ingredient_name:
                    unit = "kg"
                elif "Nutmeg" in ingredient_name:
                    unit = "kg"
                elif "Flour" in ingredient_name:
                    unit = "kg"
                elif "Sugar" in ingredient_name:
                    unit = "kg"
                elif "Beef" in ingredient_name:
                    unit = "kg"
                elif "Carrots" in ingredient_name:
                    unit = "kg"
                elif "Wine" in ingredient_name:
                    unit = "bottle"
                elif "Bouillon" in ingredient_name:
                    unit = "pcs"
                elif "Cornmeal" in ingredient_name:
                    unit = "kg"
                elif "Buttermilk" in ingredient_name:
                    unit = "L"
                elif "Eggs" in ingredient_name:
                    unit = "pcs"
                elif "Peppers" in ingredient_name:
                    unit = "kg"
                elif "Sesame" in ingredient_name:
                    unit = "bundle"
                elif "Container" in ingredient_name:
                    unit = "pcs"
                else:
                    unit = "unit"

                ingredients.append({
                    "id": ingredient_id,
                    "name": ingredient_name,
                    "unit": unit
                })
            return ingredients
        except Error as e:
            messagebox.showerror("Database Error", f"Error loading ingredient data: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

    def initialize_real_time_inventory(self):
        """Initialize real-time inventory data from database"""
        connection = self.create_db_connection()
        if connection is None:
            return []

        cursor = connection.cursor()
        try:
            # Calculate total inventory for each ingredient
            query = """
            SELECT i.ingredient_id, i.ingredient_name, SUM(p.quantity_on_hand) AS total_quantity
            FROM ingredient_purchase p
            JOIN ingredient i ON p.ingredient_id = i.ingredient_id
            GROUP BY i.ingredient_id, i.ingredient_name
            """
            cursor.execute(query)

            inventory = []
            for (ingredient_id, ingredient_name, total_quantity) in cursor:
                # Set unit based on ingredient name
                if "Clams" in ingredient_name:
                    unit = "kg"
                elif "Potatoes" in ingredient_name:
                    unit = "kg"
                elif "Onions" in ingredient_name:
                    unit = "kg"
                elif "Celery" in ingredient_name:
                    unit = "kg"
                elif "Cream" in ingredient_name:
                    unit = "L"
                elif "Bread Bowl" in ingredient_name:
                    unit = "pcs"
                elif "Lobster" in ingredient_name:
                    unit = "kg"
                elif "Mayonnaise" in ingredient_name:
                    unit = "bottle"
                elif "Butter" in ingredient_name:
                    unit = "kg"
                elif "Buns" in ingredient_name:
                    unit = "pcs"
                elif "Coleslaw" in ingredient_name:
                    unit = "kg"
                elif "Apples" in ingredient_name:
                    unit = "kg"
                elif "Cinnamon" in ingredient_name:
                    unit = "kg"
                elif "Nutmeg" in ingredient_name:
                    unit = "kg"
                elif "Flour" in ingredient_name:
                    unit = "kg"
                elif "Sugar" in ingredient_name:
                    unit = "kg"
                elif "Beef" in ingredient_name:
                    unit = "kg"
                elif "Carrots" in ingredient_name:
                    unit = "kg"
                elif "Wine" in ingredient_name:
                    unit = "bottle"
                elif "Bouillon" in ingredient_name:
                    unit = "pcs"
                elif "Cornmeal" in ingredient_name:
                    unit = "kg"
                elif "Buttermilk" in ingredient_name:
                    unit = "L"
                elif "Eggs" in ingredient_name:
                    unit = "pcs"
                elif "Peppers" in ingredient_name:
                    unit = "kg"
                elif "Sesame" in ingredient_name:
                    unit = "bundle"
                elif "Container" in ingredient_name:
                    unit = "pcs"
                else:
                    unit = "unit"

                inventory.append({
                    "id": ingredient_id,
                    "name": ingredient_name,
                    "quantity": total_quantity,
                    "unit": unit
                })
            return inventory
        except Error as e:
            messagebox.showerror("Database Error", f"Error loading real-time inventory: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

    def initialize_inventory_detail(self):
        """Initialize inventory detail data from database"""
        connection = self.create_db_connection()
        if connection is None:
            return []

        cursor = connection.cursor()
        try:
            query = """
            SELECT 
                p.ingredient_purchase_id,
                p.ingredient_id,
                i.ingredient_name,
                p.quantity_on_hand,
                p.ingredient_expiration_date,
                p.purchase_date
            FROM ingredient_purchase p
            JOIN ingredient i ON p.ingredient_id = i.ingredient_id
            """
            cursor.execute(query)

            inventory_detail = []
            for row in cursor:
                purchase_id = row[0]
                ingredient_id = row[1]
                ingredient_name = row[2]
                quantity = row[3]
                expiration_date = row[4].strftime("%Y-%m-%d") if row[4] else ""
                purchase_date = row[5].strftime("%Y-%m-%d") if row[5] else ""

                inventory_detail.append({
                    "purchase_id": purchase_id,
                    "ingredient_id": ingredient_id,
                    "ingredient_name": ingredient_name,
                    "quantity": quantity,
                    "expiration_date": expiration_date,
                    "purchase_date": purchase_date
                })
            return inventory_detail
        except Error as e:
            messagebox.showerror("Database Error", f"Error loading inventory detail: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

    def create_menu(self):
        """Create left menu bar"""
        menu_frame = ttk.Frame(self.main_frame, width=200)
        menu_frame.pack(side="left", fill="y", padx=10, pady=10)
        menu_frame.pack_propagate(False)

        # Menu title
        title_label = ttk.Label(menu_frame, text="Inventory System", font=("Microsoft YaHei", 14, "bold"))
        title_label.pack(pady=(20, 30))

        # Menu buttons
        menu_items = [
            ("Real-time Inventory", "real_time_inventory", "#4e73df"),
            ("Dish COGS", "cogs", "#1cc88a"),
            ("Inventory Details", "inventory_detail", "#36b9cc")
        ]

        for text, page, color in menu_items:
            btn = tk.Button(menu_frame, text=text, font=("Microsoft YaHei", 11),
                            bg=color, fg="white", bd=0, padx=10, pady=12,
                            command=lambda p=page: self.show_page(p),
                            cursor="hand2", relief="flat")
            btn.pack(fill="x", pady=5, ipady=5)

        # Exit button
        exit_btn = tk.Button(menu_frame, text="Exit System", font=("Microsoft YaHei", 11),
                             bg="#e74a3b", fg="white", bd=0, padx=10, pady=12,
                             command=self.on_close, cursor="hand2", relief="flat")
        exit_btn.pack(fill="x", pady=5, ipady=5, side="bottom")

        # System info
        info_frame = ttk.Frame(menu_frame)
        info_frame.pack(side="bottom", fill="x", pady=10)

        today = datetime.now().strftime("%Y-%m-%d")
        ttk.Label(info_frame, text=f"System Date: {today}", font=("Microsoft YaHei", 9)).pack(anchor="w")
        ttk.Label(info_frame, text="Version: 2.0", font=("Microsoft YaHei", 9)).pack(anchor="w")

    def create_real_time_inventory_page(self):
        """Create real-time inventory page"""
        self.real_time_inventory_frame = ttk.Frame(self.content_frame)

        # Title
        title_frame = ttk.Frame(self.real_time_inventory_frame)
        title_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(title_frame, text="Real-time Inventory", font=("Microsoft YaHei", 16, "bold")).pack(side="left")

        # Search box
        search_frame = ttk.Frame(title_frame)
        search_frame.pack(side="right", padx=10)

        self.realtime_search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.realtime_search_var, width=30)
        search_entry.pack(side="left", padx=(0, 5))
        search_entry.bind("<Return>", lambda e: self.search_real_time_inventory())

        ttk.Button(search_frame, text="Search", command=self.search_real_time_inventory).pack(side="left")
        ttk.Button(search_frame, text="Refresh", command=self.load_real_time_inventory).pack(side="left", padx=5)

        # Create canvas with scrollbar
        canvas = tk.Canvas(self.real_time_inventory_frame)
        scrollbar = ttk.Scrollbar(self.real_time_inventory_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        scrollbar.pack(side="right", fill="y")

        # Inventory cards container
        self.inventory_cards_frame = ttk.Frame(self.scrollable_frame)
        self.inventory_cards_frame.pack(fill="both", expand=True)

    def create_cogs_page(self):
        """Create dish COGS page"""
        self.cogs_frame = ttk.Frame(self.content_frame)

        # Title
        title_frame = ttk.Frame(self.cogs_frame)
        title_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(title_frame, text="Dish Cost of Goods Sold (COGS)", font=("Microsoft YaHei", 16, "bold")).pack(
            side="left")

        # Control buttons
        btn_frame = ttk.Frame(title_frame)
        btn_frame.pack(side="right", padx=10)

        ttk.Button(btn_frame, text="Refresh Data", command=self.load_cogs_data).pack(side="left", padx=5)

        # Create canvas with scrollbar
        canvas = tk.Canvas(self.cogs_frame)
        scrollbar = ttk.Scrollbar(self.cogs_frame, orient="vertical", command=canvas.yview)
        self.scrollable_cogs_frame = ttk.Frame(canvas)

        self.scrollable_cogs_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_cogs_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        scrollbar.pack(side="right", fill="y")

        # Dish COGS display container
        self.cogs_container = ttk.Frame(self.scrollable_cogs_frame)
        self.cogs_container.pack(fill="both", expand=True)

    def create_inventory_detail_page(self):
        """Create inventory details page"""
        self.inventory_detail_frame = ttk.Frame(self.content_frame)

        # Title
        title_frame = ttk.Frame(self.inventory_detail_frame)
        title_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(title_frame, text="Inventory Details", font=("Microsoft YaHei", 16, "bold")).pack(side="left")

        # Control buttons
        btn_frame = ttk.Frame(title_frame)
        btn_frame.pack(side="right", padx=10)

        ttk.Button(btn_frame, text="Add Record", command=self.add_inventory).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Edit Selected", command=self.edit_inventory).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Refresh Data", command=self.load_inventory_data).pack(side="left", padx=5)

        # Search box
        search_frame = ttk.Frame(self.inventory_detail_frame)
        search_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(search_frame, text="Search Ingredient:").pack(side="left")
        self.inventory_search = ttk.Entry(search_frame)
        self.inventory_search.pack(side="left", padx=5, fill="x", expand=True)
        self.inventory_search.bind("<Return>", lambda e: self.search_inventory())

        ttk.Button(search_frame, text="Search", command=self.search_inventory).pack(side="left", padx=5)

        # Create Treeview
        columns = ("purchase_id", "ingredient_id", "ingredient_name", "quantity", "expiration_date",
                   "purchase_date")
        self.inventory_tree = ttk.Treeview(self.inventory_detail_frame, columns=columns, show="headings",
                                           selectmode="browse")

        # Set column widths and headings
        self.inventory_tree.column("purchase_id", width=80, anchor="center")
        self.inventory_tree.column("ingredient_id", width=80, anchor="center")
        self.inventory_tree.column("ingredient_name", width=150, anchor="w")
        self.inventory_tree.column("quantity", width=100, anchor="center")
        self.inventory_tree.column("expiration_date", width=120, anchor="center")
        self.inventory_tree.column("purchase_date", width=120, anchor="center")

        self.inventory_tree.heading("purchase_id", text="Purchase ID")
        self.inventory_tree.heading("ingredient_id", text="Ingredient ID")
        self.inventory_tree.heading("ingredient_name", text="Ingredient Name")
        self.inventory_tree.heading("quantity", text="Quantity")
        self.inventory_tree.heading("expiration_date", text="Expiration Date")
        self.inventory_tree.heading("purchase_date", text="Purchase Date")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.inventory_detail_frame, orient="vertical", command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscroll=scrollbar.set)

        self.inventory_tree.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        scrollbar.pack(side="right", fill="y")

        # Bind double-click event
        self.inventory_tree.bind("<Double-1>", lambda event: self.edit_inventory())

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.inventory_detail_frame, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(side="bottom", fill="x")

    def show_page(self, page_name):
        """Show specified page"""
        if page_name == "real_time_inventory":
            self.real_time_inventory_frame.pack(fill="both", expand=True)
            self.cogs_frame.pack_forget()
            self.inventory_detail_frame.pack_forget()
        elif page_name == "cogs":
            self.cogs_frame.pack(fill="both", expand=True)
            self.real_time_inventory_frame.pack_forget()
            self.inventory_detail_frame.pack_forget()
        elif page_name == "inventory_detail":
            self.inventory_detail_frame.pack(fill="both", expand=True)
            self.real_time_inventory_frame.pack_forget()
            self.cogs_frame.pack_forget()

    def create_db_connection(self):
        """Create database connection"""
        connection = None
        try:
            connection = mysql.connector.connect(**self.db_config)
        except Error as e:
            messagebox.showerror("Database Connection Error", f"Error: {e}")
        return connection

    def load_real_time_inventory(self):
        """Load real-time inventory data"""
        # Reload real-time inventory from database
        self.real_time_inventory = self.initialize_real_time_inventory()

        # Clear existing cards
        for widget in self.inventory_cards_frame.winfo_children():
            widget.destroy()

        # Apply search filter
        search_query = self.realtime_search_var.get().strip().lower()
        filtered_ingredients = [ing for ing in self.real_time_inventory
                                if not search_query or search_query in ing["name"].lower()]

        # Create cards
        rows = 3
        cols = 4
        for i, ingredient in enumerate(filtered_ingredients):
            row = i // cols
            col = i % cols

            card = tk.Frame(self.inventory_cards_frame, bg="#ffffff", bd=1, relief="groove")
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            # Set grid row/column weights
            self.inventory_cards_frame.grid_rowconfigure(row, weight=1)
            self.inventory_cards_frame.grid_columnconfigure(col, weight=1)

            # Card content
            name_label = tk.Label(card, text=ingredient["name"], font=("Microsoft YaHei", 12, "bold"),
                                  bg="#ffffff", fg="#333333")
            name_label.pack(pady=(15, 5))

            qty_label = tk.Label(card, text=f"Quantity: {ingredient['quantity']} {ingredient['unit']}",
                                 font=("Microsoft YaHei", 14), bg="#ffffff", fg="#4e73df")
            qty_label.pack(pady=5)

            # Add progress bar
            progress_value = min(100, ingredient["quantity"] / 5)
            progress = ttk.Progressbar(card, orient="horizontal", length=150, mode="determinate",
                                       value=progress_value)
            progress.pack(pady=10)

            # Set progress bar color
            if ingredient["quantity"] > 100:
                progress_style = "green.Horizontal.TProgressbar"
            elif ingredient["quantity"] > 50:
                progress_style = "yellow.Horizontal.TProgressbar"
            else:
                progress_style = "red.Horizontal.TProgressbar"

            progress.configure(style=progress_style)

            # Add status label
            status = "Sufficient" if ingredient["quantity"] > 100 else "Normal" if ingredient[
                                                                                       "quantity"] > 50 else "Low"
            status_color = "#1cc88a" if status == "Sufficient" else "#f6c23e" if status == "Normal" else "#e74a3b"
            status_label = tk.Label(card, text=f"Status: {status}", font=("Microsoft YaHei", 10),
                                    bg="#ffffff", fg=status_color)
            status_label.pack(pady=(0, 15))

    def search_real_time_inventory(self):
        """Search real-time inventory"""
        self.load_real_time_inventory()

    def load_cogs_data(self):
        """Load dish COGS data"""
        # Clear existing content
        for widget in self.cogs_container.winfo_children():
            widget.destroy()

        # Load dish data from database
        connection = self.create_db_connection()
        if connection is None:
            return

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT meal_id, meal_name, meal_price FROM meal")
            meals = []
            for (meal_id, meal_name, meal_price) in cursor:
                # Simplified handling: use fixed cost and profit margin
                if "Clam" in meal_name:
                    cogs = "$19.85"
                    profit_margin = "34%"
                elif "Lobster" in meal_name:
                    cogs = "$24.50"
                    profit_margin = "46%"
                elif "Apple" in meal_name:
                    cogs = "$12.30"
                    profit_margin = "51%"
                elif "Roast" in meal_name:
                    cogs = "$28.75"
                    profit_margin = "43%"
                elif "Cornbread" in meal_name:
                    cogs = "$8.20"
                    profit_margin = "45%"
                else:
                    cogs = "$0.00"
                    profit_margin = "0%"

                meals.append({
                    "name": meal_name,
                    "avg_price": f"${meal_price:.2f}",
                    "cogs": cogs,
                    "profit_margin": profit_margin
                })
        except Error as e:
            messagebox.showerror("Database Error", f"Error loading dish data: {e}")
        finally:
            cursor.close()
            connection.close()

        # Create dish cards
        for i, meal in enumerate(meals):
            card = tk.Frame(self.cogs_container, bg="#ffffff", bd=1, relief="groove")
            card.pack(fill="x", padx=10, pady=10)

            # Dish name
            name_frame = tk.Frame(card, bg="#4e73df")
            name_frame.pack(fill="x", pady=(0, 10))

            name_label = tk.Label(name_frame, text=meal["name"], font=("Microsoft YaHei", 14, "bold"),
                                  bg="#4e73df", fg="white", padx=10, pady=5)
            name_label.pack(side="left")

            # Dish info
            info_frame = tk.Frame(card, bg="#ffffff")
            info_frame.pack(fill="x", padx=10, pady=5)

            # Price info
            price_frame = tk.Frame(info_frame, bg="#ffffff")
            price_frame.pack(side="left", padx=10, pady=5, fill="both", expand=True)

            tk.Label(price_frame, text=f"Avg Price: {meal['avg_price']}", anchor="w",
                     font=("Microsoft YaHei", 10), bg="#ffffff").pack(fill="x")

            # Cost info
            cost_frame = tk.Frame(info_frame, bg="#ffffff")
            cost_frame.pack(side="left", padx=10, pady=5, fill="both", expand=True)

            tk.Label(cost_frame, text=f"COGS: {meal['cogs']}", anchor="w",
                     font=("Microsoft YaHei", 10), bg="#ffffff").pack(fill="x")
            tk.Label(cost_frame, text=f"Profit Margin: {meal['profit_margin']}", anchor="w",
                     font=("Microsoft YaHei", 10), bg="#ffffff").pack(fill="x")

    def load_inventory_data(self, search_query=""):
        """Load inventory detail data"""
        # Reload inventory detail from database
        self.inventory_detail = self.initialize_inventory_detail()

        # Clear existing data
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)

        # Apply search filter
        filtered_data = []
        for record in self.inventory_detail:
            if not search_query or search_query.lower() in record["ingredient_name"].lower():
                filtered_data.append((
                    record["purchase_id"],
                    record["ingredient_id"],
                    record["ingredient_name"],
                    record["quantity"],
                    record["expiration_date"],
                    record["purchase_date"]
                ))

        # Insert data into Treeview
        for record in filtered_data:
            self.inventory_tree.insert("", "end", values=record)

        # Update status bar
        self.status_var.set(f"Found {len(filtered_data)} records | Last update: {datetime.now().strftime('%H:%M:%S')}")

    def search_inventory(self):
        """Search inventory"""
        query = self.inventory_search.get().strip()
        self.load_inventory_data(query)

    def add_inventory(self):
        """Add inventory record"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Inventory Record")
        dialog.geometry("400x350")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # Form fields
        fields = [
            ("Ingredient", "combo", [ing["name"] for ing in self.ingredient_data]),
            ("Quantity", "number"),
            ("Unit Price", "number"),
            ("Expiration Date (YYYY-MM-DD)", "text", datetime.now().strftime('%Y-%m-%d')),
            ("Purchase Date (YYYY-MM-DD)", "text", datetime.now().strftime('%Y-%m-%d'))
        ]

        entries = []
        for i, (label, field_type, *args) in enumerate(fields):
            ttk.Label(dialog, text=label).grid(row=i, column=0, padx=10, pady=10, sticky="w")

            if field_type == "combo":
                var = tk.StringVar()
                combo = ttk.Combobox(dialog, textvariable=var, values=args[0])
                combo.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                if args[0]:
                    combo.current(0)
                entries.append(var)
            elif field_type == "text":
                default = args[0] if args else ""
                var = tk.StringVar(value=default)
                entry = ttk.Entry(dialog, textvariable=var)
                entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                entries.append(var)
            elif field_type == "number":
                var = tk.StringVar()
                entry = ttk.Entry(dialog, textvariable=var)
                entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                entries.append(var)

        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)

        def save_action():
            try:
                # Get form data
                ingredient_name = entries[0].get().strip()
                quantity = int(entries[1].get().strip())
                unit_price = float(entries[2].get().strip())
                expiration_date = entries[3].get().strip()
                purchase_date = entries[4].get().strip()

                # Validate data
                if not ingredient_name:
                    messagebox.showerror("Error", "Ingredient name cannot be empty")
                    return

                if quantity <= 0:
                    messagebox.showerror("Error", "Quantity must be greater than 0")
                    return

                # Find ingredient ID
                ingredient = next((ing for ing in self.ingredient_data if ing["name"] == ingredient_name), None)
                if not ingredient:
                    messagebox.showerror("Error", f"Ingredient not found: {ingredient_name}")
                    return

                ingredient_id = ingredient["id"]

                # Connect to database
                connection = self.create_db_connection()
                if connection is None:
                    return

                cursor = connection.cursor()
                try:
                    # Insert new record to database
                    query = """
                    INSERT INTO ingredient_purchase 
                    (ingredient_id, unit_price, quantity_on_hand, ingredient_expiration_date, purchase_date)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (ingredient_id, unit_price, quantity, expiration_date, purchase_date))
                    connection.commit()

                    messagebox.showinfo("Success", "Inventory record added successfully")
                    dialog.destroy()

                    # Refresh data
                    self.load_inventory_data()
                    self.load_real_time_inventory()

                    # Update status bar
                    self.status_var.set(f"Record added | Last update: {datetime.now().strftime('%H:%M:%S')}")

                except Error as e:
                    connection.rollback()
                    messagebox.showerror("Database Error", f"Error adding record: {e}")
                finally:
                    cursor.close()
                    connection.close()

            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")

        ttk.Button(btn_frame, text="Save", command=save_action).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=10)

    def edit_inventory(self):
        """Edit selected inventory record"""
        selected_item = self.inventory_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record first")
            return

        item = self.inventory_tree.item(selected_item[0])
        values = item["values"]
        purchase_id = values[0]

        # Find record
        record = next((rec for rec in self.inventory_detail if rec["purchase_id"] == purchase_id), None)
        if not record:
            messagebox.showerror("Error", "Selected record not found")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Inventory Record")
        dialog.geometry("400x350")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # Form fields
        fields = [
            ("Ingredient", "text", record["ingredient_name"], True),  # Read-only
            ("Quantity", "number", record["quantity"]),
            ("Unit Price", "number", "0.00"),  # Placeholder, actual data will be fetched
            ("Expiration Date (YYYY-MM-DD)", "text", record["expiration_date"]),
            ("Purchase Date (YYYY-MM-DD)", "text", record["purchase_date"])
        ]

        entries = []
        for i, (label, field_type, default, *readonly) in enumerate(fields):
            ttk.Label(dialog, text=label).grid(row=i, column=0, padx=10, pady=10, sticky="w")

            if field_type == "text":
                var = tk.StringVar(value=default)
                entry = ttk.Entry(dialog, textvariable=var)
                if readonly and readonly[0]:
                    entry.config(state="readonly")
                entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                entries.append(var)
            elif field_type == "number":
                var = tk.StringVar(value=str(default))
                entry = ttk.Entry(dialog, textvariable=var)
                entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                entries.append(var)

        # Get actual unit price
        connection = self.create_db_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT unit_price FROM ingredient_purchase WHERE ingredient_purchase_id = %s",
                               (purchase_id,))
                unit_price = cursor.fetchone()[0]
                entries[2].set(str(unit_price))  # Set unit price field value
            except Error as e:
                messagebox.showerror("Database Error", f"Error fetching unit price: {e}")
            finally:
                cursor.close()
                connection.close()

        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)

        def update_action():
            try:
                # Get form data
                quantity = int(entries[1].get().strip())
                unit_price = float(entries[2].get().strip())
                expiration_date = entries[3].get().strip()
                purchase_date = entries[4].get().strip()

                # Validate data
                if quantity <= 0:
                    messagebox.showerror("Error", "Quantity must be greater than 0")
                    return

                # Connect to database
                connection = self.create_db_connection()
                if connection is None:
                    return

                cursor = connection.cursor()
                try:
                    # Update database record
                    query = """
                    UPDATE ingredient_purchase 
                    SET 
                        quantity_on_hand = %s,
                        unit_price = %s,
                        ingredient_expiration_date = %s,
                        purchase_date = %s
                    WHERE ingredient_purchase_id = %s
                    """
                    cursor.execute(query, (quantity, unit_price, expiration_date, purchase_date, purchase_id))
                    connection.commit()

                    messagebox.showinfo("Success", "Inventory record updated successfully")
                    dialog.destroy()

                    # Refresh data
                    self.load_inventory_data()
                    self.load_real_time_inventory()

                    # Update status bar
                    self.status_var.set(f"Record updated | Last update: {datetime.now().strftime('%H:%M:%S')}")

                except Error as e:
                    connection.rollback()
                    messagebox.showerror("Database Error", f"Error updating record: {e}")
                finally:
                    cursor.close()
                    connection.close()

            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")

        ttk.Button(btn_frame, text="Update", command=update_action).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=10)

    def on_close(self):
        """Close application"""
        if messagebox.askokcancel("Exit", "Are you sure you want to exit the system?"):
            self.root.destroy()


if __name__ == "__main__":
    # Create custom progress bar styles
    root = tk.Tk()

    # Create custom progress bar styles
    style = ttk.Style()
    style.configure("green.Horizontal.TProgressbar", background='#1cc88a')
    style.configure("yellow.Horizontal.TProgressbar", background='#f6c23e')
    style.configure("red.Horizontal.TProgressbar", background='#e74a3b')

    app = InventoryManagementSystem(root)
    root.iconbitmap("logo.ico")
    root.mainloop()