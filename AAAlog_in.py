import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import subprocess
import os
import sys
import mysql.connector


class MainApp:
    """系统主界面 - 展示餐厅信息和菜品"""

    def __init__(self, root):
        self.team_font = None
        self.root = root
        self.root.title("Intelligent Restaurant Management System")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f5f5f5")

        # 设置窗口图标
        self.set_window_icon("logo.ico")

        # 创建主框架
        main_frame = ttk.Frame(root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 顶部栏 - 包含Logo和登录按钮
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill="x", pady=(0, 20))

        # 右侧登录按钮
        login_btn = tk.Button(
            header_frame,
            text="Log In",
            bg="#4CAF50",
            fg="white",
            font=("Microsoft YaHei", 10, "bold"),
            padx=15,
            pady=5,
            command=self.open_login
        )
        login_btn.pack(side="right")

        # 系统标题
        title_label = ttk.Label(
            main_frame,
            text="Intelligent Restaurant Management System",
            font=("Microsoft YaHei", 20, "bold"),
            foreground="#2c3e50"
        )
        title_label.pack(pady=(10, 30))

        # Add team logo and description
        team_frame = ttk.Frame(main_frame)
        team_frame.pack(pady=(0, 20))

        try:
            # Try to load team logo
            logo_img = Image.open("big_logo.png")
            logo_img = logo_img.resize((150, 40), Image.LANCZOS)  # Resize logo
            self.team_logo = ImageTk.PhotoImage(logo_img)  # 使用不同的变量名

            # Display logo
            logo_label = tk.Label(team_frame, image=self.team_logo, bg="#f5f5f5")
            logo_label.pack(side="left", padx=(0, 15))

            # Team description text
            team_text = tk.Label(
                team_frame,
                text="Focus on solutions for the catering industry",
                font=("Microsoft YaHei", 14),
                bg="#f5f5f5",
                justify="left",
            )
            team_text.pack(side="left")

        except Exception as e:
            # If logo not found, display text only
            team_text = tk.Label(
                team_frame,
                text="Specializing in restaurant solutions",
                bg="#f5f5f5",
                justify="center",
                font=("Microsoft YaHei", 14)  # 直接指定字体
            )
            team_text.pack()
            print(f"Failed to load logo: {str(e)}")

        # 菜品列表
        dish_names = ["Clam Chowder", "Lobster Roll", "Apple Pie", "Pot Roast", "Cornbread"]
        dish_images = [
            "clam_chowder.ico",  # 请替换为实际图片路径
            "Lobster_Roll.png",  # 请替换为实际图片路径
            "Apple_Pie.png",  # 请替换为实际图片路径
            "Pot_Roast.png",  # 请替换为实际图片路径
            "Cornbread.png"  # 请替换为实际图片路径
        ]

        # 创建菜品容器框架
        dishes_container = ttk.Frame(main_frame)
        dishes_container.pack(fill="both", expand=True, pady=20)

        # 创建菜品展示
        for i, (name, img_path) in enumerate(zip(dish_names, dish_images)):
            dish_frame = ttk.Frame(dishes_container)
            dish_frame.grid(row=i // 3, column=i % 3, padx=15, pady=15, sticky="nsew")

            # 菜品图片
            try:
                dish_img = Image.open(img_path)
                dish_img = dish_img.resize((150, 150), Image.LANCZOS)
                dish_photo = ImageTk.PhotoImage(dish_img)
                dish_label = tk.Label(dish_frame, image=dish_photo)
                dish_label.image = dish_photo  # 保持引用
                dish_label.pack(pady=(0, 10))
            except Exception as e:
                # 使用占位符
                placeholder = tk.Label(dish_frame, text="Image Placeholder",
                                       bg="#e0e0e0", width=25, height=8)
                placeholder.pack(pady=(0, 10))
                print(f"Failed to load dish image: {str(e)}")

            # 菜品名称
            ttk.Label(
                dish_frame,
                text=name,
                font=("Microsoft YaHei", 10, "bold"),
                foreground="#333333"
            ).pack()

        # 设置网格列权重使菜品均匀分布
        for col in range(3):
            dishes_container.columnconfigure(col, weight=1)

    def set_window_icon(self, icon_path):
        """设置窗口图标"""
        try:
            self.root.iconbitmap(icon_path)
        except:
            try:
                logo_img = Image.open(icon_path)
                logo_img = logo_img.resize((32, 32), Image.LANCZOS)
                self.icon = ImageTk.PhotoImage(logo_img)
                self.root.iconphoto(False, self.icon)
            except Exception as e:
                print(f"Failed to set window icon: {str(e)}")

    def open_login(self):
        """打开登录窗口"""
        self.root.destroy()  # 关闭主界面
        login_root = tk.Tk()
        LoginWindow(login_root)
        login_root.mainloop()


class LoginWindow:
    """登录窗口"""

    def __init__(self, master):
        self.master = master
        self.master.title("Employee Login")
        self.master.geometry("500x500")  # 增加高度以容纳新输入框
        self.master.configure(bg="#f5f5f5")
        self.master.resizable(False, False)

        # 设置窗口图标
        self.set_window_icon("logo.ico")

        # 创建主框架
        main_frame = ttk.Frame(master, padding=30)
        main_frame.pack(fill="both", expand=True)

        # 标题
        title_label = ttk.Label(
            main_frame,
            text="Employee Login",
            font=("Microsoft YaHei", 20, "bold"),
            foreground="#2c3e50"
        )
        title_label.pack(pady=(0, 30))

        # 职位选择
        role_frame = ttk.Frame(main_frame)
        role_frame.pack(fill="x", pady=10)

        ttk.Label(
            role_frame,
            text="Position:",
            font=("Microsoft YaHei", 12)
        ).pack(side="left", padx=(0, 10))

        self.role_var = tk.StringVar()
        roles = ["Admin", "Server", "Manager", "Accountant"]
        role_combobox = ttk.Combobox(
            role_frame,
            textvariable=self.role_var,
            values=roles,
            state="readonly",
            font=("Microsoft YaHei", 12),
            width=15
        )
        role_combobox.pack(side="left")
        role_combobox.current(0)

        # 密码输入
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill="x", pady=10)

        ttk.Label(
            password_frame,
            text="Password:",
            font=("Microsoft YaHei", 12)
        ).pack(side="left", padx=(0, 10))

        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(
            password_frame,
            textvariable=self.password_var,
            show="*",
            font=("Microsoft YaHei", 12),
            width=20
        )
        password_entry.pack(side="left")

        # 新增：MySQL密码输入
        mysql_frame = ttk.Frame(main_frame)
        mysql_frame.pack(fill="x", pady=10)

        ttk.Label(
            mysql_frame,
            text="MySQL Password:",
            font=("Microsoft YaHei", 12)
        ).pack(side="left", padx=(0, 10))

        self.mysql_password_var = tk.StringVar()
        mysql_entry = ttk.Entry(
            mysql_frame,
            textvariable=self.mysql_password_var,
            show="*",
            font=("Microsoft YaHei", 12),
            width=20
        )
        mysql_entry.pack(side="left")

        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=30)

        # 登录按钮
        login_btn = tk.Button(
            button_frame,
            text="Login",
            bg="#4CAF50",
            fg="white",
            font=("Microsoft YaHei", 12, "bold"),
            padx=20,
            pady=5,
            command=self.login
        )
        login_btn.pack(side="left", padx=(0, 20))

        # 返回按钮
        back_btn = tk.Button(
            button_frame,
            text="Back",
            bg="#9e9e9e",
            fg="white",
            font=("Microsoft YaHei", 12, "bold"),
            padx=20,
            pady=5,
            command=self.back_to_main
        )
        back_btn.pack(side="left")

    def set_window_icon(self, icon_path):
        """设置窗口图标"""
        try:
            self.master.iconbitmap(icon_path)
        except:
            try:
                logo_img = Image.open(icon_path)
                logo_img = logo_img.resize((32, 32), Image.LANCZOS)
                self.icon = ImageTk.PhotoImage(logo_img)
                self.master.iconphoto(False, self.icon)
            except Exception as e:
                print(f"Failed to set window icon: {str(e)}")

    def login(self):
        """处理登录逻辑"""
        role = self.role_var.get()
        password = self.password_var.get()
        mysql_password = self.mysql_password_var.get()  # 获取MySQL密码

        # 验证密码
        if not os.environ.get('APP_LOGIN_PASSWORD') or password != os.environ.get('APP_LOGIN_PASSWORD'):
            messagebox.showerror("Login Failed", "Incorrect password. Please try again.")
            return

        # 验证MySQL密码
        if not mysql_password:
            messagebox.showerror("Database Error", "MySQL password cannot be empty")
            return

        # 检测MySQL连接
        try:
            # 尝试连接MySQL数据库
            connection = mysql.connector.connect(
                host='localhost',
                database='restaurant_test1',
                user='root',
                password=mysql_password
            )
            if connection.is_connected():
                connection.close()  # 连接成功后关闭连接
            else:
                messagebox.showerror("Database Error", "Failed to connect to MySQL database")
                return
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to MySQL: {str(e)}")
            return

        # 打开系统子界面，传递MySQL密码
        self.master.destroy()
        system_root = tk.Tk()
        SystemApp(system_root, role, mysql_password)  # 传递MySQL密码
        system_root.mainloop()

    def back_to_main(self):
        """返回主界面"""
        self.master.destroy()
        main_root = tk.Tk()
        MainApp(main_root)
        main_root.mainloop()


class SystemApp:
    """系统子界面 - 功能模块入口"""

    def __init__(self, root, role, mysql_password):  # 增加mysql_password参数
        self.root = root
        self.root.title(f"Restaurant Management System - {role}")
        self.root.geometry("900x600")
        self.root.configure(bg="#f5f5f5")

        # 保存MySQL密码
        self.mysql_password = mysql_password

        # 设置窗口图标
        self.set_window_icon("logo.ico")

        # 当前用户角色
        self.current_role = role

        # 创建主框架
        main_frame = ttk.Frame(root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 欢迎信息
        welcome_frame = ttk.Frame(main_frame)
        welcome_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(
            welcome_frame,
            text=f"Welcome, {role}!",
            font=("Microsoft YaHei", 18, "bold"),
            foreground="#2c3e50"
        ).pack(side="left")

        # 返回按钮
        back_btn = tk.Button(
            welcome_frame,
            text="Back to Login",
            bg="#9e9e9e",
            fg="white",
            font=("Microsoft YaHei", 10, "bold"),
            padx=10,
            pady=3,
            command=self.back_to_login
        )
        back_btn.pack(side="right")

        # 模块按钮框架
        modules_frame = ttk.LabelFrame(
            main_frame,
            text="System Modules",
            padding=20
        )
        modules_frame.pack(fill="both", expand=True, pady=10)

        # 创建模块按钮
        self.create_module_buttons(modules_frame)

        # 状态栏
        self.status_var = tk.StringVar(value=f"Logged in as: {role}")
        status_bar = ttk.Label(
            root,
            textvariable=self.status_var,
            relief="sunken",
            anchor="w"
        )
        status_bar.pack(side="bottom", fill="x")

        # 系统信息
        info_frame = ttk.Frame(root)
        info_frame.pack(side="bottom", fill="x", pady=5)

        ttk.Label(
            info_frame,
            text="Restaurant Management System v3.0",
            font=("Microsoft YaHei", 9)
        ).pack(side="left", padx=10)

        ttk.Label(
            info_frame,
            text="Development Team: Nexolutions",
            font=("Microsoft YaHei", 9)
        ).pack(side="right", padx=10)

    def set_window_icon(self, icon_path):
        """设置窗口图标"""
        try:
            self.root.iconbitmap(icon_path)
        except:
            try:
                logo_img = Image.open(icon_path)
                logo_img = logo_img.resize((32, 32), Image.LANCZOS)
                self.icon = ImageTk.PhotoImage(logo_img)
                self.root.iconphoto(False, self.icon)
            except Exception as e:
                print(f"Failed to set window icon: {str(e)}")

    def create_module_buttons(self, parent_frame):
        """根据角色创建模块按钮"""
        # 所有可能的模块
        modules = [
            ("Order Tracking", "order_manage.py", "#f39c12"),
            ("Customer Management", "customer_manage.py", "#2ecc71"),
            ("Inventory Management", "inventory_manage.py", "#e74c3c"),
            ("Budget Management", "budget_manage.py", "#3498db"),
            ("Show Database", "show_database.py", "#9b59b6")
        ]

        # 根据角色确定可见模块
        visible_modules = []
        if self.current_role == "Admin":
            visible_modules = modules
        elif self.current_role == "Server":
            visible_modules = [modules[0], modules[1]]  # Order Tracking, Customer Management
        elif self.current_role == "Manager":
            visible_modules = modules[:4]  # 除Show Database外的所有模块
        elif self.current_role == "Accountant":
            visible_modules = [modules[2], modules[3]]  # Inventory Management, Budget Management

        # 创建按钮
        for i, (name, script, color) in enumerate(visible_modules):
            btn = tk.Button(
                parent_frame,
                text=name,
                bg=color,
                fg="white",
                font=("Microsoft YaHei", 12, "bold"),
                padx=15,
                pady=10,
                width=20,
                command=lambda s=script, n=name: self.open_module(s, n)
            )
            btn.grid(row=i // 3, column=i % 3, padx=15, pady=15)

        # 添加空白标签填充空单元格
        for i in range(len(visible_modules), 6):
            tk.Label(parent_frame, bg="#f5f5f5", width=20, height=3).grid(
                row=i // 3, column=i % 3, padx=15, pady=15
            )

    def open_module(self, module_file, module_name):
        """打开指定模块"""
        self.status_var.set(f"Opening {module_name}...")
        self.root.update()

        try:
            # 使用绝对路径确保能找到文件
            script_path = os.path.join(os.path.dirname(__file__), module_file)

            if os.path.exists(script_path):
                # 使用子进程运行模块，传递MySQL密码
                if sys.platform == "win32":
                    # 在Windows上，使用CREATE_NO_WINDOW标志避免显示控制台窗口
                    subprocess.Popen(
                        [sys.executable, script_path, self.mysql_password],
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                else:
                    # 在非Windows系统上
                    subprocess.Popen([sys.executable, script_path, self.mysql_password])
                self.status_var.set(f"{module_name} opened successfully")
            else:
                messagebox.showerror("Error", f"File not found: {script_path}")
                self.status_var.set("Error: File not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open {module_name}: {str(e)}")
            self.status_var.set(f"Error: Failed to open {module_name}")

    def back_to_login(self):
        """返回登录界面"""
        self.root.destroy()
        login_root = tk.Tk()
        LoginWindow(login_root)
        login_root.mainloop()


if __name__ == "__main__":
    # 启动系统主界面
    root = tk.Tk()
    app = MainApp(root)
    root.iconbitmap("logo.ico")
    root.mainloop()