import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
from mysql.connector import Error
from datetime import datetime, date, timedelta
import csv
import os
import sys


class OrderTrackingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Order Tracking System")
        self.root.geometry("1200x800")

        # Set font
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        self.style.configure("Treeview", font=("Arial", 10))
        self.style.configure(".", font=("Arial", 10))

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

        self.connect_to_database()

        # Create main interface
        self.create_main_interface()

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

    def create_main_interface(self):
        """Create main interface"""
        # 创建标签页控件
        self.tab_control = ttk.Notebook(self.root)

        # 创建订单管理标签页
        self.order_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.order_tab, text="Order Management")

        # 创建订单跟踪标签页
        self.tracking_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tracking_tab, text="Order Tracking")

        # 创建报表标签页
        self.report_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.report_tab, text="Report Generation")

        self.tab_control.pack(expand=1, fill="both")

        # 初始化各个标签页内容
        self.init_order_tab()
        self.init_tracking_tab()
        self.init_report_tab()

    def init_order_tab(self):
        """Initialize Order Management tab"""
        # 创建订单表单框架
        order_frame = ttk.LabelFrame(self.order_tab, text="Create New Order")
        order_frame.pack(fill="x", padx=10, pady=5)

        # 客户选择
        ttk.Label(order_frame, text="Select Customer:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.customer_var = tk.StringVar()
        self.customer_combobox = ttk.Combobox(order_frame, textvariable=self.customer_var, width=40)
        self.customer_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ttk.Button(order_frame, text="Refresh Customer List", command=self.load_customers).grid(row=0, column=2, padx=5,
                                                                                                pady=5)

        # 订单日期
        ttk.Label(order_frame, text="Order Date:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.order_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        ttk.Entry(order_frame, textvariable=self.order_date_var, width=20).grid(row=1, column=1, padx=5, pady=5,
                                                                                sticky="w")

        # 配送日期
        ttk.Label(order_frame, text="Delivery Date:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.delivery_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        ttk.Entry(order_frame, textvariable=self.delivery_date_var, width=20).grid(row=1, column=3, padx=5, pady=5,
                                                                                   sticky="w")

        # 配送地址
        ttk.Label(order_frame, text="Delivery Address:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.delivery_address_var = tk.StringVar()
        ttk.Entry(order_frame, textvariable=self.delivery_address_var, width=60).grid(row=2, column=1, columnspan=3,
                                                                                      padx=5, pady=5, sticky="w")

        # 订单状态
        ttk.Label(order_frame, text="Order Status:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.status_var = tk.StringVar(value="pending")
        status_combobox = ttk.Combobox(order_frame, textvariable=self.status_var,
                                       values=["pending", "processing", "completed"], state="readonly",
                                       width=15)
        status_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # 菜品选择区域
        items_frame = ttk.LabelFrame(self.order_tab, text="Order Items")
        items_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # 菜品选择
        ttk.Label(items_frame, text="Select Meal:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.meal_var = tk.StringVar()
        self.meal_combobox = ttk.Combobox(items_frame, textvariable=self.meal_var, width=30)
        self.meal_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ttk.Button(items_frame, text="Refresh Meal List", command=self.load_meals).grid(row=0, column=2, padx=5, pady=5)

        # 数量
        ttk.Label(items_frame, text="Quantity:").grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.quantity_var = tk.IntVar(value=1)
        ttk.Spinbox(items_frame, from_=1, to=100, textvariable=self.quantity_var, width=5).grid(row=0, column=4, padx=5,
                                                                                                pady=5, sticky="w")

        # 添加按钮
        ttk.Button(items_frame, text="Add to Order", command=self.add_meal_to_order).grid(row=0, column=5, padx=5,
                                                                                          pady=5)

        # 订单菜品表格
        columns = ("meal_id", "meal_name", "quantity", "unit_price", "total")
        self.order_items_tree = ttk.Treeview(items_frame, columns=columns, show="headings", height=8)
        for col in columns:
            self.order_items_tree.heading(col, text=col)
            self.order_items_tree.column(col, width=100)
        self.order_items_tree.grid(row=1, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")

        # 添加滚动条
        scrollbar = ttk.Scrollbar(items_frame, orient="vertical", command=self.order_items_tree.yview)
        self.order_items_tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=6, sticky="ns")

        # 删除选中菜品按钮
        ttk.Button(items_frame, text="Remove Selected Item", command=self.remove_selected_item).grid(row=2, column=0,
                                                                                                     padx=5, pady=5,
                                                                                                     sticky="w")

        # 总计金额
        ttk.Label(items_frame, text="Order Total:").grid(row=2, column=4, padx=5, pady=5, sticky="e")
        self.total_amount_var = tk.StringVar(value="0.00")
        ttk.Label(items_frame, textvariable=self.total_amount_var, font=("Arial", 12, "bold")).grid(row=2, column=5,
                                                                                                    padx=5, pady=5,
                                                                                                    sticky="w")

        # 保存订单按钮
        ttk.Button(self.order_tab, text="Save Order", command=self.save_order).pack(pady=10)

        # 加载初始数据
        self.load_customers()
        self.load_meals()

    def init_tracking_tab(self):
        """Initialize Order Tracking tab"""
        # 查询框架
        query_frame = ttk.LabelFrame(self.tracking_tab, text="Order Search")
        query_frame.pack(fill="x", padx=10, pady=5)

        # 状态筛选
        ttk.Label(query_frame, text="Order Status:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.track_status_var = tk.StringVar(value="all")
        status_combobox = ttk.Combobox(query_frame, textvariable=self.track_status_var,
                                       values=["all", "pending", "processing", "completed"], width=15)
        status_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # 日期范围
        ttk.Label(query_frame, text="Start Date:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.start_date_var = tk.StringVar(value=(date.today() - timedelta(days=30)).strftime("%Y-%m-%d"))
        ttk.Entry(query_frame, textvariable=self.start_date_var, width=15).grid(row=0, column=3, padx=5, pady=5,
                                                                                sticky="w")

        ttk.Label(query_frame, text="End Date:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.end_date_var = tk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        ttk.Entry(query_frame, textvariable=self.end_date_var, width=15).grid(row=0, column=5, padx=5, pady=5,
                                                                              sticky="w")

        # 查询按钮
        ttk.Button(query_frame, text="Search Orders", command=self.search_orders).grid(row=0, column=6, padx=5, pady=5)

        # 订单列表
        orders_frame = ttk.LabelFrame(self.tracking_tab, text="Order List")
        orders_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("order_id", "customer", "order_date", "status", "total_amount")
        self.orders_tree = ttk.Treeview(orders_frame, columns=columns, show="headings", height=15)
        self.orders_tree.heading("order_id", text="Order ID")
        self.orders_tree.heading("customer", text="Customer")
        self.orders_tree.heading("order_date", text="Order Date")
        self.orders_tree.heading("status", text="Status")
        self.orders_tree.heading("total_amount", text="Total Amount")

        self.orders_tree.column("order_id", width=80)
        self.orders_tree.column("customer", width=150)
        self.orders_tree.column("order_date", width=120)
        self.orders_tree.column("status", width=100)
        self.orders_tree.column("total_amount", width=100)

        self.orders_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(orders_frame, orient="vertical", command=self.orders_tree.yview)
        self.orders_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # 订单详情和状态变更
        action_frame = ttk.LabelFrame(self.tracking_tab, text="Order Actions")
        action_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(action_frame, text="View Order Details", command=self.view_order_details).grid(row=0, column=0,
                                                                                                  padx=5, pady=5)

        ttk.Label(action_frame, text="Change Order Status:").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.new_status_var = tk.StringVar()
        status_combobox = ttk.Combobox(action_frame, textvariable=self.new_status_var,
                                       values=["pending", "processing", "completed"], width=15)
        status_combobox.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        ttk.Button(action_frame, text="Update Status", command=self.update_order_status).grid(row=0, column=3, padx=5,
                                                                                              pady=5)

        # 初始加载订单
        self.search_orders()

    def init_report_tab(self):
        """Initialize Report tab"""
        # 报表查询框架
        report_query_frame = ttk.LabelFrame(self.report_tab, text="Report Query")
        report_query_frame.pack(fill="x", padx=10, pady=5)

        # 报表类型
        ttk.Label(report_query_frame, text="Report Type:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.report_type_var = tk.StringVar(value="daily")
        report_type_combobox = ttk.Combobox(report_query_frame, textvariable=self.report_type_var,
                                            values=["daily", "weekly", "monthly"], width=15)
        report_type_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # 日期范围
        ttk.Label(report_query_frame, text="Start Date:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.report_start_date_var = tk.StringVar(value=(date.today() - timedelta(days=30)).strftime("%Y-%m-%d"))
        ttk.Entry(report_query_frame, textvariable=self.report_start_date_var, width=15).grid(row=0, column=3, padx=5,
                                                                                              pady=5, sticky="w")

        ttk.Label(report_query_frame, text="End Date:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.report_end_date_var = tk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        ttk.Entry(report_query_frame, textvariable=self.report_end_date_var, width=15).grid(row=0, column=5, padx=5,
                                                                                            pady=5, sticky="w")

        # 查询和导出按钮
        ttk.Button(report_query_frame, text="Generate Report", command=self.generate_report).grid(row=0, column=6,
                                                                                                  padx=5, pady=5)
        ttk.Button(report_query_frame, text="Export CSV", command=self.export_report).grid(row=0, column=7, padx=5,
                                                                                           pady=5)

        # 报表展示
        report_frame = ttk.LabelFrame(self.report_tab, text="Report Data")
        report_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("meal_name", "quantity_sold", "order_count", "revenue")
        self.report_tree = ttk.Treeview(report_frame, columns=columns, show="headings", height=15)
        self.report_tree.heading("meal_name", text="Meal Name")
        self.report_tree.heading("quantity_sold", text="Quantity Sold")
        self.report_tree.heading("order_count", text="Order Count")
        self.report_tree.heading("revenue", text="Revenue")
        self.report_tree.column("meal_name", width=150)
        self.report_tree.column("quantity_sold", width=120)
        self.report_tree.column("order_count", width=120)
        self.report_tree.column("revenue", width=120)
        self.report_tree.pack(fill="both", expand=True, padx=5, pady=5)

    # Inventory management tab has been removed
    pass

    # The following are various function implementation methods
    def load_customers(self):
        """Load customer list into combobox"""
        if not self.db_connection or not self.db_connection.is_connected():
            self.connect_to_database()
            if not self.db_connection:
                return

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "SELECT customer_id, CONCAT(first_name, ' ', last_name, ' (', customer_phone_number, ')') FROM customer ORDER BY last_name")
            customers = cursor.fetchall()
            self.customer_combobox['values'] = [customer[1] for customer in customers]
            self.customer_dict = {customer[1]: customer[0] for customer in customers}
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load customers: {str(e)}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()

    def load_meals(self):
        """Load meal list into combobox"""
        if not self.db_connection or not self.db_connection.is_connected():
            self.connect_to_database()
            if not self.db_connection:
                return

        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT meal_id, meal_name, meal_price FROM meal ORDER BY meal_name")
            meals = cursor.fetchall()
            self.meal_combobox['values'] = [meal[1] for meal in meals]
            self.meal_dict = {meal[1]: (meal[0], meal[2]) for meal in meals}
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load meals: {str(e)}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()

    def add_meal_to_order(self):
        """Add meal to order"""
        meal_name = self.meal_var.get()
        if not meal_name or meal_name not in self.meal_dict:
            messagebox.showwarning("Input Error", "Please select a valid meal")
            return

        quantity = self.quantity_var.get()
        if quantity <= 0:
            messagebox.showwarning("Input Error", "Quantity must be greater than 0")
            return

        meal_id, unit_price = self.meal_dict[meal_name]
        total = quantity * unit_price

        # 检查是否已添加此菜品
        for item in self.order_items_tree.get_children():
            if self.order_items_tree.item(item, "values")[0] == str(meal_id):
                current_quantity = int(self.order_items_tree.item(item, "values")[2])
                new_quantity = current_quantity + quantity
                new_total = new_quantity * unit_price
                self.order_items_tree.item(item, values=(meal_id, meal_name, new_quantity, unit_price, new_total))
                self.update_total_amount()
                return

        # 添加新菜品到表格
        self.order_items_tree.insert('', 'end', values=(meal_id, meal_name, quantity, unit_price, total))
        self.update_total_amount()

    def remove_selected_item(self):
        """Remove selected item"""
        selected_items = self.order_items_tree.selection()
        if not selected_items:
            messagebox.showwarning("Selection Error", "Please select an item to remove first")
            return

        for item in selected_items:
            self.order_items_tree.delete(item)
        self.update_total_amount()

    def update_total_amount(self):
        """Update order total amount"""
        total = 0
        for item in self.order_items_tree.get_children():
            total += float(self.order_items_tree.item(item, "values")[4])
        self.total_amount_var.set(f"{total:.2f}")

    def save_order(self):
        """Save order to database"""
        if not self.db_connection or not self.db_connection.is_connected():
            self.connect_to_database()
            if not self.db_connection:
                return

        # 验证客户选择
        customer_name = self.customer_var.get()
        if not customer_name or customer_name not in self.customer_dict:
            messagebox.showwarning("Input Error", "Please select a valid customer")
            return
        customer_id = self.customer_dict[customer_name]

        # 验证订单日期
        try:
            order_date = datetime.strptime(self.order_date_var.get(), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            messagebox.showwarning("Date Error", "Invalid order date format (should be YYYY-MM-DD HH:MM:SS)")
            return

        # 验证配送日期
        try:
            delivery_date = datetime.strptime(self.delivery_date_var.get(), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            messagebox.showwarning("Date Error", "Invalid delivery date format")
            return

        # 验证配送地址
        delivery_address = self.delivery_address_var.get()
        if not delivery_address:
            messagebox.showwarning("Input Error", "Please enter delivery address")
            return

        # 验证订单菜品
        if not self.order_items_tree.get_children():
            messagebox.showwarning("Empty Order", "Please add at least one meal to the order")
            return

        # 验证库存
        if not self.check_inventory_for_order():
            return

        try:
            # 确保之前的事务已回滚
            self.db_connection.rollback()
            # 开始新事务
            self.db_connection.start_transaction()
            cursor = self.db_connection.cursor()

            # 插入订单主表
            order_status = self.status_var.get()
            total_amount = float(self.total_amount_var.get())

            order_sql = """
            INSERT INTO customer_order
            (customer_id, customer_order_date, customer_delivery_date, customer_delivery_address, customer_order_status)
            VALUES (%s, %s, %s, %s, %s)
            """
            order_data = (
                customer_id,
                order_date,
                delivery_date,
                delivery_address,
                order_status
            )
            cursor.execute(order_sql, order_data)
            order_id = cursor.lastrowid

            # 插入订单详情
            item_sql = """
            INSERT INTO order_line_item
            (customer_order_id, meal_id, meal_price, customer_quantity_ordered)
            VALUES (%s, %s, %s, %s)
            """
            for item in self.order_items_tree.get_children():
                values = self.order_items_tree.item(item, "values")
                meal_id = int(values[0])
                quantity = int(values[2])
                unit_price = float(values[3])
                item_data = (order_id, meal_id, unit_price, quantity)
                cursor.execute(item_sql, item_data)

            # 如果订单状态不是pending，更新库存
            if order_status != "pending":
                self.deduct_inventory_for_order(cursor, order_id)

            # 提交事务
            self.db_connection.commit()
            messagebox.showinfo("Success", f"Order #{order_id} created successfully!")

            # 清空订单表单
            self.clear_order_form()

            # 刷新订单跟踪标签页的订单列表
            self.search_orders()

        except Exception as e:
            # 回滚事务
            self.db_connection.rollback()
            messagebox.showerror("数据库错误", f"保存订单失败: {str(e)}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()

    def check_inventory_for_order(self):
        """Check if inventory is sufficient for order"""
        if not self.db_connection or not self.db_connection.is_connected():
            return False

        try:
            cursor = self.db_connection.cursor()

            # 检查每个菜品的库存
            for item in self.order_items_tree.get_children():
                values = self.order_items_tree.item(item, "values")
                meal_id = int(values[0])
                quantity = int(values[2])

                # 获取菜品所需食材
                cursor.execute("""
                SELECT mi.ingredient_id, mi.quantity_required, i.ingredient_name
                FROM meal_ingredient mi
                JOIN ingredient i ON mi.ingredient_id = i.ingredient_id
                WHERE mi.meal_id = %s
                """, (meal_id,))
                ingredients = cursor.fetchall()

                # 检查每种食材的库存
                for ingredient_id, qty_required, ingredient_name in ingredients:
                    total_required = qty_required * quantity

                    # 获取当前库存
                    cursor.execute("""
                    SELECT SUM(quantity_on_hand) FROM ingredient_purchase
                    WHERE ingredient_id = %s AND ingredient_expiration_date > CURDATE()
                    """, (ingredient_id,))
                    result = cursor.fetchone()
                    current_stock = result[0] if result[0] else 0

                    if current_stock < total_required:
                        messagebox.showwarning("Insufficient Inventory",
                                               f"Ingredient '{ingredient_name}' is insufficient!\nRequired: {total_required}, Current stock: {current_stock}")
                        return False

            return True

        except Error as e:
            messagebox.showerror("Database Error", f"Inventory check failed: {str(e)}")
            return False
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()

    def deduct_inventory_for_order(self, cursor, order_id):
        """Deduct inventory for order"""
        # 获取订单详情
        cursor.execute("""
        SELECT meal_id, customer_quantity_ordered
        FROM order_line_item
        WHERE customer_order_id = %s
        """, (order_id,))
        order_items = cursor.fetchall()

        # 处理每个菜品
        for meal_id, quantity in order_items:
            # 获取菜品所需食材
            cursor.execute("""
            SELECT ingredient_id, quantity_required
            FROM meal_ingredient
            WHERE meal_id = %s
            """, (meal_id,))
            ingredients = cursor.fetchall()

            # 扣减每种食材库存
            for ingredient_id, qty_required in ingredients:
                total_required = qty_required * quantity
                remaining = total_required

                # Deduct inventory by expiration date ascending (use soonest to expire first)
                cursor.execute("""
                SELECT ingredient_purchase_id, quantity_on_hand
                FROM ingredient_purchase
                WHERE ingredient_id = %s AND ingredient_expiration_date > CURDATE() AND quantity_on_hand > 0
                ORDER BY ingredient_expiration_date ASC
                """, (ingredient_id,))
                inventory_items = cursor.fetchall()

                for purchase_id, qty_available in inventory_items:
                    if remaining <= 0:
                        break

                    if qty_available <= remaining:
                        # Use up this inventory batch
                        cursor.execute("""
                        UPDATE ingredient_purchase
                        SET quantity_on_hand = 0
                        WHERE ingredient_purchase_id = %s
                        """, (purchase_id,))
                        remaining -= qty_available
                    else:
                        # Partially use this inventory batch
                        cursor.execute("""
                        UPDATE ingredient_purchase
                        SET quantity_on_hand = quantity_on_hand - %s
                        WHERE ingredient_purchase_id = %s
                        """, (remaining, purchase_id))
                        remaining = 0

                if remaining > 0:
                    raise Error(
                        f"Failed to deduct inventory, ingredient ID {ingredient_id} still lacks {remaining} quantity")

    def clear_order_form(self):
        """Clear order form"""
        # 清空菜品表格
        for item in self.order_items_tree.get_children():
            self.order_items_tree.delete(item)

        # 重置总金额
        self.total_amount_var.set("0.00")

        # 重置配送地址
        self.delivery_address_var.set("")

    def search_orders(self):
        """Search orders"""
        if not self.db_connection or not self.db_connection.is_connected():
            self.connect_to_database()
            if not self.db_connection:
                return

        # 清空现有订单
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)

        try:
            cursor = self.db_connection.cursor()
            status = self.track_status_var.get()
            start_date = self.start_date_var.get()
            end_date = self.end_date_var.get()

            # Build query SQL
            sql = """
            SELECT co.customer_order_id, CONCAT(c.first_name, ' ', c.last_name), co.customer_order_date, co.customer_order_status, 
            SUM(oli.meal_price * oli.customer_quantity_ordered) as total_amount
            FROM customer_order co
            JOIN customer c ON co.customer_id = c.customer_id
            LEFT JOIN order_line_item oli ON co.customer_order_id = oli.customer_order_id
            WHERE co.customer_order_date BETWEEN %s AND %s
            """
            params = [start_date, end_date + " 23:59:59"]

            # Add status filter
            if status != "all":
                sql += " AND co.customer_order_status = %s"
                params.append(status)

            sql += " GROUP BY co.customer_order_id, c.first_name, c.last_name, co.customer_order_date, co.customer_order_status"
            cursor.execute(sql, params)
            orders = cursor.fetchall()

            # 添加到表格
            for order in orders:
                order_id, customer_name, order_date, status, total_amount = order
                # 格式化日期
                formatted_date = order_date.strftime("%Y-%m-%d %H:%M") if order_date else ""
                # 格式化金额
                formatted_amount = f"{total_amount:.2f}" if total_amount else "0.00"
                self.orders_tree.insert('', 'end',
                                        values=(order_id, customer_name, formatted_date, status, formatted_amount))

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to search orders: {str(e)}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()

    def view_order_details(self):
        selected_item = self.orders_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an order first")
            return

        order_id = self.orders_tree.item(selected_item[0], "values")[0]

        # 查询订单详情
        if not self.db_connection or not self.db_connection.is_connected():
            self.connect_to_database()
            if not self.db_connection:
                return

        try:
            cursor = self.db_connection.cursor()
            # 查询订单基本信息
            cursor.execute("""
                SELECT co.customer_order_id, c.first_name, c.last_name, co.customer_order_date, 
                       co.customer_delivery_date, co.customer_delivery_address, co.customer_order_status
                FROM customer_order co
                JOIN customer c ON co.customer_id = c.customer_id
                WHERE co.customer_order_id = %s
            """, (order_id,))
            order = cursor.fetchone()

            if not order:
                messagebox.showinfo("Notice", "Order information not found")
                return

            # 查询订单项
            cursor.execute("""
                SELECT m.meal_name, oli.customer_quantity_ordered, oli.meal_price, 
                       (oli.meal_price * oli.customer_quantity_ordered) as total
                FROM order_line_item oli
                JOIN meal m ON oli.meal_id = m.meal_id
                WHERE oli.customer_order_id = %s
            """, (order_id,))
            items = cursor.fetchall()

            # 创建弹窗显示详情
            detail_window = tk.Toplevel(self.root)
            detail_window.title(f"Order Details #{order_id}")
            detail_window.geometry("600x500")

            # 配置网格布局权重
            detail_window.grid_rowconfigure(7, weight=1)
            detail_window.grid_columnconfigure(0, weight=1)

            # 显示订单信息
            order_date_str = order[3].strftime("%Y-%m-%d %H:%M") if order[3] else "Not set"
            delivery_date_str = order[4].strftime("%Y-%m-%d") if order[4] else "Not set"

            ttk.Label(detail_window, text=f"Order ID: {order[0]}").grid(row=0, column=0, sticky="w", padx=10, pady=5)
            ttk.Label(detail_window, text=f"Customer: {order[1]} {order[2]}").grid(row=1, column=0, sticky="w", padx=10,
                                                                                   pady=5)
            ttk.Label(detail_window, text=f"Order Date: {order_date_str}").grid(row=2, column=0, sticky="w", padx=10,
                                                                                pady=5)
            ttk.Label(detail_window, text=f"Delivery Date: {delivery_date_str}").grid(row=3, column=0, sticky="w",
                                                                                      padx=10, pady=5)
            ttk.Label(detail_window, text=f"Delivery Address: {order[5]}").grid(row=4, column=0, sticky="w", padx=10,
                                                                                pady=5)
            ttk.Label(detail_window, text=f"Order Status: {order[6]}").grid(row=5, column=0, sticky="w", padx=10,
                                                                            pady=5)

            # 显示订单项
            ttk.Label(detail_window, text="Order Items:", font=('Arial', 10, 'bold')).grid(row=6, column=0, sticky="w",
                                                                                           padx=10, pady=10)
            columns = ("meal", "quantity", "price", "total")
            tree = ttk.Treeview(detail_window, columns=columns, show="headings", height=10)

            # 设置列宽
            tree.column("meal", width=200)
            tree.column("quantity", width=100)
            tree.column("price", width=100)
            tree.column("total", width=100)

            for col in columns:
                tree.heading(col, text=col)

            # 添加滚动条
            scrollbar = ttk.Scrollbar(detail_window, orient="vertical", command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            tree.grid(row=7, column=0, padx=10, pady=5, sticky="nsew")
            scrollbar.grid(row=7, column=1, sticky="ns")

            # 插入订单项数据
            total = 0
            if not items:
                messagebox.showinfo("Notice", "This order has no order items data")
            else:
                for item in items:
                    tree.insert('', 'end', values=item)
                    total += item[3]

                ttk.Label(detail_window, text=f"Total Amount: {total:.2f}", font=('Arial', 10, 'bold')).grid(row=8,
                                                                                                             column=0,
                                                                                                             sticky="e",
                                                                                                             padx=10,
                                                                                                             pady=10)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to query order details: {str(e)}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()

    def update_order_status(self):
        """Update order status"""
        selected_items = self.orders_tree.selection()
        if not selected_items:
            messagebox.showwarning("Selection Error", "Please select an order to update first")
            return

        order_id = self.orders_tree.item(selected_items[0], "values")[0]
        new_status = self.new_status_var.get()

        if not new_status:
            messagebox.showwarning("Input Error", "Please select a new order status")
            return

        if not self.db_connection or not self.db_connection.is_connected():
            self.connect_to_database()
            if not self.db_connection:
                return

        try:
            cursor = self.db_connection.cursor()

            # 获取当前状态
            cursor.execute("SELECT customer_order_status FROM customer_order WHERE customer_order_id = %s", (order_id,))
            current_status = cursor.fetchone()[0]

            # Check if status transition is valid
            valid_transitions = {
                "pending": ["processing"],
                "processing": ["completed"],
                "completed": [],
                "cancelled": []
            }

            if new_status not in valid_transitions[current_status]:
                messagebox.showwarning("Status Error",
                                       f"Cannot change status from '{current_status}' to '{new_status}'")
                return

            # 确保之前的事务已回滚
            self.db_connection.rollback()
            # 开始新事务
            self.db_connection.start_transaction()

            # 更新订单状态
            cursor.execute(
                "UPDATE customer_order SET customer_order_status = %s WHERE customer_order_id = %s",
                (new_status, order_id)
            )

            # 如果状态变为processing或completed，处理库存
            if new_status == "processing":
                # 检查库存
                if not self.check_inventory_for_order_id(cursor, order_id):
                    self.db_connection.rollback()
                    return
                # 扣减库存
                self.deduct_inventory_for_order(cursor, order_id)

            # 提交事务
            self.db_connection.commit()
            messagebox.showinfo("Success", f"Order #{order_id} status updated to '{new_status}'")

            # 刷新订单列表
            self.search_orders()

        except Exception as e:
            # 回滚事务
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to update order status: {str(e)}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()

    def check_inventory_for_order_id(self, cursor, order_id):
        """Check inventory by order ID"""
        # 获取订单菜品
        cursor.execute("""
        SELECT meal_id, customer_quantity_ordered
        FROM order_line_item
        WHERE customer_order_id = %s
        """, (order_id,))
        order_items = cursor.fetchall()

        # 检查每个菜品的库存
        for meal_id, quantity in order_items:
            # 获取菜品所需食材
            cursor.execute("""
            SELECT mi.ingredient_id, mi.quantity_required, i.ingredient_name
            FROM meal_ingredient mi
            JOIN ingredient i ON mi.ingredient_id = i.ingredient_id
            WHERE mi.meal_id = %s
            """, (meal_id,))
            ingredients = cursor.fetchall()

            # 检查每种食材的库存
            for ingredient_id, qty_required, ingredient_name in ingredients:
                total_required = qty_required * quantity

                # 获取当前库存
                cursor.execute("""
                SELECT SUM(quantity_on_hand) FROM ingredient_purchase
                WHERE ingredient_id = %s AND ingredient_expiration_date > CURDATE()
                """, (ingredient_id,))
                result = cursor.fetchone()
                current_stock = result[0] if result[0] else 0

                if current_stock < total_required:
                    messagebox.showwarning("Insufficient inventory",
                                           f"Ingredient '{ingredient_name}' Insufficient inventory\nneed: {total_required}, Current inventory: {current_stock}")
                    return False

        return True

    def restore_inventory_for_order(self, cursor, order_id):
        """Restore inventory occupied by order"""
        # Implement inventory restoration logic
        # Note: In actual projects, an inventory change log table is required for accurate restoration
        messagebox.showinfo("Notice",
                            "Inventory restoration requires an inventory change log table. Currently only updating order status.")

    def update_report_dates(self, event):
        """Update report start and end dates based on selected report type"""
        from datetime import date, timedelta
        report_type = self.report_type_var.get()
        today = date.today()

        if report_type == "daily":
            # Set to today
            self.report_start_date_var.set(today.strftime("%Y-%m-%d"))
            self.report_end_date_var.set(today.strftime("%Y-%m-%d"))
        elif report_type == "weekly":
            # Set to Monday to Sunday of current week
            monday = today - timedelta(days=today.weekday())
            sunday = monday + timedelta(days=6)
            self.report_start_date_var.set(monday.strftime("%Y-%m-%d"))
            self.report_end_date_var.set(sunday.strftime("%Y-%m-%d"))
        elif report_type == "monthly":
            # Set to first and last day of current month
            first_day = date(today.year, today.month, 1)
            # Get last day of month
            if today.month == 12:
                next_month = date(today.year + 1, 1, 1)
            else:
                next_month = date(today.year, today.month + 1, 1)
            last_day = next_month - timedelta(days=1)
            self.report_start_date_var.set(first_day.strftime("%Y-%m-%d"))
            self.report_end_date_var.set(last_day.strftime("%Y-%m-%d"))
        # For custom type, dates remain as user input

    def generate_report(self):
        """Generate report"""
        if not self.db_connection or not self.db_connection.is_connected():
            self.connect_to_database()
            if not self.db_connection:
                return

        # Clear existing report data
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)

        try:
            cursor = self.db_connection.cursor()
            start_date = self.report_start_date_var.get()
            end_date = self.report_end_date_var.get()

            # SQL query to get meal sales statistics
            sql = """
            SELECT 
                m.meal_name,
                SUM(oli.customer_quantity_ordered) as quantity_sold,
                COUNT(DISTINCT co.customer_order_id) as order_count,
                SUM(oli.customer_quantity_ordered * oli.meal_price) as revenue
            FROM 
                customer_order co
            JOIN 
                order_line_item oli ON co.customer_order_id = oli.customer_order_id
            JOIN 
                meal m ON oli.meal_id = m.meal_id
            WHERE 
                co.customer_order_date BETWEEN %s AND %s
            GROUP BY 
                m.meal_id, m.meal_name
            ORDER BY 
                revenue DESC
            """
            cursor.execute(sql, (start_date, end_date + " 23:59:59"))
            results = cursor.fetchall()

            # Add to report
            for row in results:
                meal_name, quantity_sold, order_count, revenue = row
                formatted_quantity = f"{quantity_sold}" if quantity_sold else "0"
                formatted_order_count = f"{order_count}" if order_count else "0"
                formatted_revenue = f"{revenue:.2f}" if revenue else "0.00"

                self.report_tree.insert('', 'end', values=(meal_name, formatted_quantity, formatted_order_count,
                                                           formatted_revenue))

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to generate report: {str(e)}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()

    def export_report(self):
        """Export Report to CSV"""
        if not self.report_tree.get_children():
            messagebox.showwarning("No Data", "The report has no data to export")
            return

        # Get desktop path
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        filename = os.path.join(desktop_path, f"order_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)

                # Write header
                headers = [self.report_tree.heading(col, "text") for col in self.report_tree['columns']]
                writer.writerow(headers)

                # Write data
                for item in self.report_tree.get_children():
                    row = self.report_tree.item(item, "values")
                    writer.writerow(row)

            messagebox.showinfo("Success", f"Report exported to:\n{filename}")

        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export report: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = OrderTrackingSystem(root)
    root.iconbitmap("logo.ico")
    root.mainloop()