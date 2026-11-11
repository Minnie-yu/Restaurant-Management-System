import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pymysql
from decimal import Decimal
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sys


class DBUtils:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            return True
        except pymysql.Error as e:
            messagebox.showerror("Database Connection Error", f"Failed to connect to database: {e}")
            return False

    def close(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                if query.strip().upper().startswith('SELECT'):
                    return cursor.fetchall()
                else:
                    self.connection.commit()
                    return cursor.rowcount
        except pymysql.Error as e:
            messagebox.showerror("Database Query Error", f"Error executing query: {e}")
            return None

    def get_income_data(self, start_date, end_date, status, customer_name):
        query = """
        SELECT
            co.customer_order_id AS order_id,
            c.first_name,
            c.last_name,
            co.customer_order_date AS order_date,
            SUM(oli.meal_price * oli.customer_quantity_ordered) AS total_amount,
            co.customer_order_status AS order_status
        FROM customer_order co
        JOIN customer c ON co.customer_id = c.customer_id
        JOIN order_line_item oli ON co.customer_order_id = oli.customer_order_id
        WHERE co.customer_order_date BETWEEN %s AND %s
        AND co.customer_order_status = %s
        AND (c.first_name LIKE %s OR c.last_name LIKE %s)
        GROUP BY co.customer_order_id
        """
        return self.execute_query(query, (start_date, end_date, status, f"%{customer_name}%", f"%{customer_name}%"))

    def get_order_details(self, order_id):
        query = """
        SELECT 
            m.meal_name, 
            oli.customer_quantity_ordered AS quantity,
            oli.meal_price AS price,
            (oli.customer_quantity_ordered * oli.meal_price) AS subtotal
        FROM order_line_item oli
        JOIN meal m ON oli.meal_id = m.meal_id
        WHERE oli.customer_order_id = %s
        """
        return self.execute_query(query, (order_id,))

    def get_variable_costs_data(self, start_date, end_date, meal_name):
        query = """
        SELECT
            co.customer_order_id AS order_id,
            m.meal_name,
            i.ingredient_name,
            SUM(mi.quantity_required * oli.customer_quantity_ordered) AS quantity_used,
            AVG(ip.unit_price) * SUM(mi.quantity_required * oli.customer_quantity_ordered) AS ingredient_cost
        FROM customer_order co
        JOIN order_line_item oli ON co.customer_order_id = oli.customer_order_id
        JOIN meal m ON oli.meal_id = m.meal_id
        JOIN meal_ingredient mi ON m.meal_id = mi.meal_id
        JOIN ingredient i ON mi.ingredient_id = i.ingredient_id
        JOIN ingredient_purchase ip ON i.ingredient_id = ip.ingredient_id
        WHERE co.customer_order_date BETWEEN %s AND %s
        AND co.customer_order_status = 'completed'
        AND m.meal_name LIKE %s
        GROUP BY co.customer_order_id, m.meal_id, i.ingredient_id
        ORDER BY co.customer_order_id
        """
        return self.execute_query(query, (start_date, end_date, f"%{meal_name}%"))

    def get_fixed_costs_data(self, expense_type):
        if expense_type == "all":
            query = "SELECT * FROM expense"
            return self.execute_query(query)
        else:
            query = "SELECT * FROM expense WHERE expense_type = %s"
            return self.execute_query(query, (expense_type,))

    @classmethod
    def from_args(cls, args):
        """从命令行参数创建实例"""
        if len(args) > 1:
            password = args[1]  # 获取命令行传入的密码
        else:
            password = os.environ.get('MYSQL_PASSWORD', '')  # 默认密码

        return cls(
            host='localhost',
            database='restaurant_test1',
            user='root',
            password=password
        )


class RestaurantManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Budget Management System")
        self.root.geometry("1400x800")

        # 设置窗口图标
        try:
            self.root.iconbitmap('restaurant.ico')
        except:
            pass

        self.db = DBUtils.from_args(sys.argv)

        # 检查数据库连接
        if not self.db.connect():
            messagebox.showerror("Error", "Database connection failed. Program will exit.")
            self.root.destroy()
            return

        # 创建主框架
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        # 创建左侧导航面板
        self.nav_frame = ttk.LabelFrame(self.main_frame, text="Navigation", width=100)
        self.nav_frame.pack(side="left", fill="y", padx=5, pady=5)

        # 创建导航按钮
        self.income_btn = ttk.Button(self.nav_frame, text="Revenue Management", command=self.show_income_tab)
        self.income_btn.pack(fill="x", padx=5, pady=5)

        self.variable_costs_btn = ttk.Button(self.nav_frame, text="Variable Costs",
                                             command=self.show_variable_costs_tab)
        self.variable_costs_btn.pack(fill="x", padx=5, pady=5)

        self.fixed_costs_btn = ttk.Button(self.nav_frame, text="Fixed Costs", command=self.show_fixed_costs_tab)
        self.fixed_costs_btn.pack(fill="x", padx=5, pady=5)

        # 创建右侧内容区域
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # 为每个标签页创建内容框架
        self.income_tab = ttk.Frame(self.content_frame)
        self.variable_costs_tab = ttk.Frame(self.content_frame)
        self.fixed_costs_tab = ttk.Frame(self.content_frame)

        # 初始化标签页
        self.create_income_tab()
        self.create_variable_costs_tab()
        self.create_fixed_costs_tab()

        # 默认显示收入标签页
        self.current_tab = self.income_tab
        self.current_tab.pack(fill="both", expand=True)

        # 初始化日期范围为2023年6月（与测试数据匹配）
        self.current_month_start = datetime.date(2023, 6, 1)
        self.current_month_end = datetime.date(2023, 6, 30)

        # 默认加载收入数据
        self.update_date_entries()
        self.query_income_data()

    def days_in_month(self, year, month):
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year
        return (datetime.date(next_year, next_month, 1) - datetime.timedelta(days=1)).day

    def update_date_entries(self):
        # 将日期选择器设置为默认2023年6月
        self.start_date_entry.set_date(self.current_month_start)
        self.var_start_date_entry.set_date(self.current_month_start)
        self.end_date_entry.set_date(self.current_month_end)
        self.var_end_date_entry.set_date(self.current_month_end)

    def show_income_tab(self):
        self.current_tab.pack_forget()
        self.current_tab = self.income_tab
        self.current_tab.pack(fill="both", expand=True)
        self.query_income_data()

    def show_variable_costs_tab(self):
        self.current_tab.pack_forget()
        self.current_tab = self.variable_costs_tab
        self.current_tab.pack(fill="both", expand=True)
        self.query_variable_costs_data()

    def show_fixed_costs_tab(self):
        self.current_tab.pack_forget()
        self.current_tab = self.fixed_costs_tab
        self.current_tab.pack(fill="both", expand=True)
        self.query_fixed_costs_data()

    def show_order_details(self, order_id):
        """显示订单明细的弹出窗口"""
        details = self.db.get_order_details(order_id)
        if not details:
            messagebox.showinfo("Order Details", f"No details found for Order ID: {order_id}")
            return

        # 创建弹出窗口
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Order Details - ID: {order_id}")
        detail_window.geometry("500x300")

        # 创建框架
        frame = ttk.Frame(detail_window)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 创建Treeview
        columns = ("Meal Name", "Quantity", "Unit Price", "Subtotal")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=8)

        # 设置列标题
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        # 调整列宽
        tree.column("Meal Name", width=150)
        tree.column("Quantity", width=80)
        tree.column("Unit Price", width=100)
        tree.column("Subtotal", width=100)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        # 放置Treeview和滚动条
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 填充数据
        total_amount = Decimal(0)
        for item in details:
            meal_name = item["meal_name"]
            quantity = item["quantity"]
            price = Decimal(str(item["price"]))
            subtotal = Decimal(str(item["subtotal"]))

            tree.insert("", "end", values=(
                meal_name,
                quantity,
                f"${price:.2f}",
                f"${subtotal:.2f}"
            ))
            total_amount += subtotal

        # 添加总计行
        tree.insert("", "end", values=("", "", "Total:", f"${total_amount:.2f}"), tags=("total",))
        tree.tag_configure("total", background="#e0e0e0", font=("Arial", 9, "bold"))

        # 添加关闭按钮
        close_btn = ttk.Button(detail_window, text="Close", command=detail_window.destroy)
        close_btn.pack(pady=10)

    def create_income_tab(self):
        # 创建筛选框架
        filter_frame = ttk.Frame(self.income_tab)
        filter_frame.pack(fill="x", padx=10, pady=10)

        # 日期范围筛选
        ttk.Label(filter_frame, text="Date Range:").grid(row=0, column=0, padx=5, pady=5)
        self.start_date_entry = DateEntry(filter_frame, date_pattern="yyyy-mm-dd")
        self.start_date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="to").grid(row=0, column=2, padx=5, pady=5)
        self.end_date_entry = DateEntry(filter_frame, date_pattern="yyyy-mm-dd")
        self.end_date_entry.grid(row=0, column=3, padx=5, pady=5)

        # 订单状态筛选
        ttk.Label(filter_frame, text="Order Status:").grid(row=0, column=4, padx=5, pady=5)
        self.status_var = tk.StringVar(value="completed")
        status_combobox = ttk.Combobox(filter_frame, textvariable=self.status_var,
                                       values=["pending", "processing", "completed", "cancelled"],
                                       state="readonly", width=12)
        status_combobox.grid(row=0, column=5, padx=5, pady=5)

        # 客户搜索
        ttk.Label(filter_frame, text="Customer Search:").grid(row=0, column=6, padx=5, pady=5)
        self.customer_search_var = tk.StringVar()
        customer_search_entry = ttk.Entry(filter_frame, textvariable=self.customer_search_var, width=20)
        customer_search_entry.grid(row=0, column=7, padx=5, pady=5)

        # 查询按钮
        query_button = ttk.Button(filter_frame, text="Query", command=self.query_income_data)
        query_button.grid(row=0, column=8, padx=5, pady=5)

        # 创建Treeview框架
        tree_frame = ttk.Frame(self.income_tab)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # 创建Treeview
        columns = ("Order ID", "Customer Name", "Order Date", "Total Amount", "Order Status")
        self.income_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")

        # 设置列标题
        for col in columns:
            self.income_tree.heading(col, text=col)
            if col == "Order ID":
                self.income_tree.column(col, width=100, anchor="center")
            elif col == "Customer Name":
                self.income_tree.column(col, width=150)
            elif col == "Order Date":
                self.income_tree.column(col, width=150, anchor="center")
            elif col == "Total Amount":
                self.income_tree.column(col, width=120, anchor="e")
            else:
                self.income_tree.column(col, width=120, anchor="center")

        # 添加滚动条
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.income_tree.yview)
        self.income_tree.configure(yscroll=scrollbar.set)

        # 放置Treeview和滚动条
        self.income_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 绑定订单ID点击事件
        self.income_tree.bind("<Button-1>", self.on_order_id_click)

        # 摘要框架
        summary_frame = ttk.Frame(self.income_tab)
        summary_frame.pack(fill="x", padx=10, pady=10)

        self.income_summary_var = tk.StringVar(value="Total Revenue: $0.00")
        ttk.Label(summary_frame, textvariable=self.income_summary_var, font=("Arial", 12, "bold")).pack(side="left")

    def on_order_id_click(self, event):
        """处理订单ID点击事件"""
        region = self.income_tree.identify("region", event.x, event.y)
        column = self.income_tree.identify_column(event.x)

        # 只处理在"Order ID"列上的点击
        if region == "cell" and column == "#1":
            item = self.income_tree.identify_row(event.y)
            if item:
                order_id = self.income_tree.item(item, "values")[0]
                self.show_order_details(order_id)
                return "break"  # 阻止事件继续传播

    def create_variable_costs_tab(self):
        # 创建筛选框架
        filter_frame = ttk.Frame(self.variable_costs_tab)
        filter_frame.pack(fill="x", padx=10, pady=10)

        # 日期范围筛选
        ttk.Label(filter_frame, text="Date Range:").grid(row=0, column=0, padx=5, pady=5)
        self.var_start_date_entry = DateEntry(filter_frame, date_pattern="yyyy-mm-dd")
        self.var_start_date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="to").grid(row=0, column=2, padx=5, pady=5)
        self.var_end_date_entry = DateEntry(filter_frame, date_pattern="yyyy-mm-dd")
        self.var_end_date_entry.grid(row=0, column=3, padx=5, pady=5)

        # 餐点名称搜索
        ttk.Label(filter_frame, text="Meal Search:").grid(row=0, column=4, padx=5, pady=5)
        self.meal_search_var = tk.StringVar()
        meal_search_entry = ttk.Entry(filter_frame, textvariable=self.meal_search_var, width=20)
        meal_search_entry.grid(row=0, column=5, padx=5, pady=5)

        # 查询按钮
        query_button = ttk.Button(filter_frame, text="Query", command=self.query_variable_costs_data)
        query_button.grid(row=0, column=6, padx=5, pady=5)

        # 创建Treeview框架
        tree_frame = ttk.Frame(self.variable_costs_tab)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # 创建Treeview
        columns = ("Order ID", "Meal Name", "Ingredient Name", "Quantity Used", "Ingredient Cost")
        self.var_costs_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        # 设置列标题
        for col in columns:
            self.var_costs_tree.heading(col, text=col)
            if col == "Order ID":
                self.var_costs_tree.column(col, width=100, anchor="center")
            elif col == "Meal Name" or col == "Ingredient Name":
                self.var_costs_tree.column(col, width=150)
            elif col == "Quantity Used":
                self.var_costs_tree.column(col, width=120, anchor="e")
            else:
                self.var_costs_tree.column(col, width=120, anchor="e")

        # 添加滚动条
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.var_costs_tree.yview)
        self.var_costs_tree.configure(yscroll=scrollbar.set)

        # 放置Treeview和滚动条
        self.var_costs_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 配置分割线样式
        self.var_costs_tree.tag_configure("separator", background="#e0e0e0", font=("Arial", 1))

        # 摘要框架
        summary_frame = ttk.Frame(self.variable_costs_tab)
        summary_frame.pack(fill="x", padx=10, pady=10)

        self.total_cost_var = tk.StringVar(value="Total Ingredient Cost: $0.00")
        self.gross_margin_var = tk.StringVar(value="Gross Margin: 0.00%")

        ttk.Label(summary_frame, textvariable=self.total_cost_var, font=("Arial", 12, "bold")).pack(side="left",
                                                                                                    padx=20)
        ttk.Label(summary_frame, textvariable=self.gross_margin_var, font=("Arial", 12, "bold")).pack(side="left",
                                                                                                      padx=20)

    def create_fixed_costs_tab(self):
        # 创建主框架
        main_frame = ttk.Frame(self.fixed_costs_tab)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill="both", expand=True)

        # 左侧面板：数据表格
        left_frame = ttk.LabelFrame(paned_window, text="Expense Details")
        paned_window.add(left_frame, weight=1)

        # 右侧面板：图表
        right_frame = ttk.LabelFrame(paned_window, text="Expense Distribution Charts")
        paned_window.add(right_frame, weight=1)

        # 左侧面板内容：筛选器和表格
        filter_frame = ttk.Frame(left_frame)
        filter_frame.pack(fill="x", padx=10, pady=10)

        # 支出类型筛选
        ttk.Label(filter_frame, text="Expense Type:").grid(row=0, column=0, padx=5, pady=5)
        self.expense_type_var = tk.StringVar(value="all")
        type_combobox = ttk.Combobox(filter_frame, textvariable=self.expense_type_var,
                                     values=["all", "salary", "utility", "other"],
                                     state="readonly", width=12)
        type_combobox.grid(row=0, column=1, padx=5, pady=5)

        # 查询按钮
        query_button = ttk.Button(filter_frame, text="Query", command=self.query_fixed_costs_data)
        query_button.grid(row=0, column=2, padx=5, pady=5)

        # 创建Treeview框架
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # 创建Treeview
        columns = ("Expense ID", "Expense Type", "Expense Name", "Amount", "Date")
        self.fixed_costs_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        # 设置列标题
        for col in columns:
            self.fixed_costs_tree.heading(col, text=col)
            if col == "Expense ID":
                self.fixed_costs_tree.column(col, width=80, anchor="center")
            elif col == "Expense Type" or col == "Expense Name":
                self.fixed_costs_tree.column(col, width=120)
            elif col == "Amount":
                self.fixed_costs_tree.column(col, width=80, anchor="e")
            else:
                self.fixed_costs_tree.column(col, width=100, anchor="center")

        # 添加滚动条
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.fixed_costs_tree.yview)
        self.fixed_costs_tree.configure(yscroll=scrollbar.set)

        # 放置Treeview和滚动条
        self.fixed_costs_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 摘要框架 - 月度固定支出
        summary_frame = ttk.Frame(left_frame)
        summary_frame.pack(fill="x", padx=10, pady=10)

        # 月度固定支出标签
        ttk.Label(summary_frame, text="Monthly Fixed Expenses:", font=("Arial", 12, "bold")).pack(side="left", padx=5)

        self.salary_total_var = tk.StringVar(value="Salary: $0.00")
        self.utility_total_var = tk.StringVar(value="Utilities: $0.00")
        self.other_total_var = tk.StringVar(value="Other: $0.00")
        self.fixed_total_var = tk.StringVar(value="Total: $0.00")

        # 使用框架组织汇总标签，避免过长
        totals_frame = ttk.Frame(summary_frame)
        totals_frame.pack(side="left", padx=10)

        ttk.Label(totals_frame, textvariable=self.salary_total_var, font=("Arial", 10)).pack(anchor="w")
        ttk.Label(totals_frame, textvariable=self.utility_total_var, font=("Arial", 10)).pack(anchor="w")
        ttk.Label(totals_frame, textvariable=self.other_total_var, font=("Arial", 10)).pack(anchor="w")

        ttk.Label(summary_frame, textvariable=self.fixed_total_var,
                  font=("Arial", 12, "bold"), foreground="blue").pack(side="right", padx=20)

        # 创建图表框架
        chart_frame = ttk.Frame(right_frame)
        chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 创建饼图框架并保存引用
        self.pie_frame = ttk.LabelFrame(chart_frame, text="Fixed Costs Distribution")
        self.pie_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # 添加占位标签
        ttk.Label(self.pie_frame, text="Pie chart will be displayed here").pack(expand=True)

        # 创建柱状图框架并保存引用
        self.bar_frame = ttk.LabelFrame(chart_frame, text="Fixed Costs Breakdown")
        self.bar_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # 添加占位标签
        ttk.Label(self.bar_frame, text="Bar chart will be displayed here").pack(expand=True)

        # 初始化图表占位符
        self.pie_canvas = None
        self.bar_canvas = None

    def update_charts(self, salary_total, utility_total, other_total):
        # 检查是否有数据
        if salary_total == 0 and utility_total == 0 and other_total == 0:
            return

        # 清除旧图表
        if self.pie_canvas:
            self.pie_canvas.get_tk_widget().destroy()
        if self.bar_canvas:
            self.bar_canvas.get_tk_widget().destroy()

        # 创建饼图
        pie_fig = plt.Figure(figsize=(8, 4), dpi=80)
        pie_ax = pie_fig.add_subplot(111)

        # 设置英文字体
        plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'sans-serif']
        plt.rcParams['axes.unicode_minus'] = False

        labels = ['Salary', 'Utilities', 'Other']
        sizes = [salary_total, utility_total, other_total]
        colors = ['#ff9999', '#66b3ff', '#99ff99']
        explode = (0.05, 0.05, 0.05)

        pie_ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                   autopct='%1.1f%%', shadow=True, startangle=90)
        pie_ax.axis('equal')
        pie_ax.set_title('Fixed Costs Distribution', fontsize=12)

        self.pie_canvas = FigureCanvasTkAgg(pie_fig, master=self.pie_frame)
        self.pie_canvas.draw()
        self.pie_canvas.get_tk_widget().pack(fill="both", expand=True)

        # 创建柱状图
        bar_fig = plt.Figure(figsize=(8, 4), dpi=80)
        bar_ax = bar_fig.add_subplot(111)

        categories = ['Salary', 'Utilities', 'Other']
        values = [salary_total, utility_total, other_total]
        colors = ['#ff9999', '#66b3ff', '#99ff99']

        bars = bar_ax.bar(categories, values, color=colors)
        bar_ax.set_title('Fixed Costs Breakdown', fontsize=12)
        bar_ax.set_ylabel('Amount ($)', fontsize=10)
        bar_ax.tick_params(axis='both', labelsize=9)

        # 在柱子上方添加数值标签
        for bar in bars:
            height = bar.get_height()
            bar_ax.annotate(f'${height:.2f}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=9)

        self.bar_canvas = FigureCanvasTkAgg(bar_fig, master=self.bar_frame)
        self.bar_canvas.draw()
        self.bar_canvas.get_tk_widget().pack(fill="both", expand=True)

    def query_income_data(self):
        # 清空表格
        for item in self.income_tree.get_children():
            self.income_tree.delete(item)

        # 获取筛选条件
        start_date = self.start_date_entry.get_date().strftime("%Y-%m-%d")
        end_date = self.end_date_entry.get_date().strftime("%Y-%m-%d") + " 23:59:59"
        status = self.status_var.get()
        customer_name = self.customer_search_var.get().strip()

        # 查询数据
        data = self.db.get_income_data(start_date, end_date, status, customer_name)

        # 计算总收入
        total_income = Decimal(0)

        # 填充表格
        if data:
            for row in data:
                order_id = row["order_id"]
                first_name = row["first_name"]
                last_name = row["last_name"]
                order_date = row["order_date"]
                total_amount = Decimal(str(row["total_amount"]))
                order_status = row["order_status"]
                customer_name = f"{first_name} {last_name}"

                # 格式化日期
                formatted_date = order_date.strftime("%Y-%m-%d %H:%M:%S")

                # 格式化金额
                formatted_amount = f"${total_amount:.2f}"

                self.income_tree.insert("", "end", values=(order_id, customer_name, formatted_date, formatted_amount,
                                                           order_status))
                total_income += total_amount
        else:
            # 插入无数据消息
            self.income_tree.insert("", "end", values=("", "No data", "", "", ""))

        # 更新摘要信息
        self.income_summary_var.set(f"Total Revenue: ${total_income:.2f}")
        self.current_income = total_income

    def query_variable_costs_data(self):
        # 清空表格
        for item in self.var_costs_tree.get_children():
            self.var_costs_tree.delete(item)

        # 获取筛选条件
        start_date = self.var_start_date_entry.get_date().strftime("%Y-%m-%d")
        end_date = self.var_end_date_entry.get_date().strftime("%Y-%m-%d") + " 23:59:59"
        meal_name = self.meal_search_var.get().strip()

        # 查询数据
        data = self.db.get_variable_costs_data(start_date, end_date, meal_name)

        # 计算总成本
        total_cost = Decimal(0)

        # 跟踪当前订单ID，用于添加分隔线
        current_order_id = None
        first_row = True

        # 填充表格
        if data:
            for row in data:
                order_id = row["order_id"]
                meal_name = row["meal_name"]
                ingredient_name = row["ingredient_name"]
                quantity_used = row["quantity_used"]
                ingredient_cost = Decimal(str(row["ingredient_cost"]))

                # 检查是否需要添加分隔线
                if order_id != current_order_id and not first_row:
                    # 添加分隔行
                    self.var_costs_tree.insert("", "end", values=("", "", "", "", ""), tags=("separator",))

                current_order_id = order_id
                first_row = False

                # 格式化数字
                formatted_quantity = f"{quantity_used:.2f}"
                formatted_cost = f"${ingredient_cost:.2f}"

                self.var_costs_tree.insert("", "end", values=(order_id, meal_name, ingredient_name, formatted_quantity,
                                                              formatted_cost))
                total_cost += ingredient_cost
        else:
            # 插入无数据消息
            self.var_costs_tree.insert("", "end", values=("", "No data", "", "", ""))

        # 更新摘要信息
        self.total_cost_var.set(f"Total Ingredient Cost: ${total_cost:.2f}")

        # 计算毛利率
        if hasattr(self, 'current_income') and self.current_income > 0:
            gross_margin = (self.current_income - total_cost) / self.current_income * 100
            self.gross_margin_var.set(f"Gross Margin: {gross_margin:.2f}%")
        else:
            self.gross_margin_var.set("Gross Margin: 0.00%")

    def query_fixed_costs_data(self):
        # 清空表格
        for item in self.fixed_costs_tree.get_children():
            self.fixed_costs_tree.delete(item)

        # 获取筛选条件
        expense_type = self.expense_type_var.get()

        # 查询数据 - 获取所有固定支出（无日期限制）
        data = self.db.get_fixed_costs_data(expense_type)

        # 计算类别总计
        salary_total = Decimal(0)
        utility_total = Decimal(0)
        other_total = Decimal(0)

        # 填充表格
        if data:
            for row in data:
                expense_id = row["expense_id"]
                expense_type = row["expense_type"]
                expense_name = row["expense_name"]
                expense_amount = Decimal(str(row["expense_amount"]))
                expense_date = row["expense_date"]

                # 格式化金额
                formatted_amount = f"${expense_amount:.2f}"

                # 格式化日期
                formatted_date = expense_date.strftime("%Y-%m-%d") if isinstance(expense_date,
                                                                                 datetime.date) else expense_date

                self.fixed_costs_tree.insert("", "end",
                                             values=(expense_id, expense_type, expense_name, formatted_amount,
                                                     formatted_date))

                # 累计类别总计
                if expense_type == 'salary':
                    salary_total += expense_amount
                elif expense_type == 'utility':
                    utility_total += expense_amount
                elif expense_type == 'other':
                    other_total += expense_amount
        else:
            # 插入无数据消息
            self.fixed_costs_tree.insert("", "end", values=("", "No data", "", "", ""))

        # 更新摘要信息
        total_fixed = salary_total + utility_total + other_total
        self.salary_total_var.set(f"Salary Total: ${salary_total:.2f}")
        self.utility_total_var.set(f"Utilities Total: ${utility_total:.2f}")
        self.other_total_var.set(f"Other Total: ${other_total:.2f}")
        self.fixed_total_var.set(f"Total Fixed Costs: ${total_fixed:.2f}")

        # 更新图表
        self.update_charts(float(salary_total), float(utility_total), float(other_total))


if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantManagementSystem(root)
    try:
        root.iconbitmap("logo.ico")
    except:
        pass
    root.mainloop()