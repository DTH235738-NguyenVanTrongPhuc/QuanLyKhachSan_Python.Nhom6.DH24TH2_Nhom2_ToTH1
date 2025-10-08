"""
HỆ THỐNG QUẢN LÝ KHÁCH SẠN - SQL SERVER
Đơn giản hóa - Sử dụng SQL Server Authentication
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pyodbc  # Thư viện kết nối SQL Server
from datetime import datetime, timedelta
import hashlib

class HotelManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản Lý Khách Sạn")
        self.root.geometry("1200x700")
        
        # Biến lưu user đăng nhập
        self.current_user = None
        
        # Kết nối SQL Server
        self.connect_database()
        
        # Tạo bảng nếu chưa có
        self.create_tables()
        
        # Tạo tài khoản admin mặc định
        self.create_admin()
        
        # Hiển thị màn hình đăng nhập
        self.login_screen()
    
    def connect_database(self):
        """Kết nối SQL Server với SQL Authentication"""
        try:
            # Cấu hình kết nối
            server = 'localhost'  # Hoặc tên server của bạn
            database = 'HotelDB'  # Tên database
            username = 'sa'  # Username SQL Server
            password = 'YourPassword123'  # Password SQL Server
            
            # Chuỗi kết nối
            conn_str = (
                f'DRIVER={{SQL Server}};'
                f'SERVER={server};'
                f'DATABASE={database};'
                f'UID={username};'
                f'PWD={password}'
            )
            
            # Kết nối
            self.conn = pyodbc.connect(conn_str)
            self.cursor = self.conn.cursor()
            print("Kết nối SQL Server thành công")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể kết nối SQL Server:\n{str(e)}")
            self.root.destroy()
    
    def create_tables(self):
        """Tạo các bảng trong database"""
        
        # Bảng Users - Người dùng
        self.cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name='users')
            CREATE TABLE users (
                user_id INT IDENTITY(1,1) PRIMARY KEY,
                username NVARCHAR(50) UNIQUE NOT NULL,
                password NVARCHAR(255) NOT NULL,
                full_name NVARCHAR(100) NOT NULL,
                created_at DATETIME DEFAULT GETDATE()
            )
        """)
        
        # Bảng Rooms - Phòng
        self.cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name='rooms')
            CREATE TABLE rooms (
                room_id INT IDENTITY(1,1) PRIMARY KEY,
                room_number NVARCHAR(20) UNIQUE NOT NULL,
                room_type NVARCHAR(50) NOT NULL,
                price DECIMAL(18,2) NOT NULL,
                status NVARCHAR(20) DEFAULT N'Trống'
            )
        """)
        
        # Bảng Customers - Khách hàng
        self.cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name='customers')
            CREATE TABLE customers (
                customer_id INT IDENTITY(1,1) PRIMARY KEY,
                full_name NVARCHAR(100) NOT NULL,
                phone NVARCHAR(20) NOT NULL,
                id_card NVARCHAR(20) UNIQUE NOT NULL
            )
        """)
        
        # Bảng Bookings - Đặt phòng
        self.cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name='bookings')
            CREATE TABLE bookings (
                booking_id INT IDENTITY(1,1) PRIMARY KEY,
                customer_id INT NOT NULL,
                room_id INT NOT NULL,
                check_in DATE NOT NULL,
                check_out DATE NOT NULL,
                total_price DECIMAL(18,2) NOT NULL,
                status NVARCHAR(20) DEFAULT N'Đã đặt',
                created_at DATETIME DEFAULT GETDATE(),
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                FOREIGN KEY (room_id) REFERENCES rooms(room_id)
            )
        """)
        
        self.conn.commit()
        print("Tạo bảng thành công")
    
    def create_admin(self):
        """Tạo tài khoản admin mặc định"""
        try:
            # Mã hóa mật khẩu
            password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
            
            # Thêm admin
            self.cursor.execute("""
                IF NOT EXISTS (SELECT * FROM users WHERE username='admin')
                INSERT INTO users (username, password, full_name)
                VALUES (?, ?, ?)
            """, ('admin', password_hash, N'Quản trị viên'))
            
            self.conn.commit()
        except:
            pass
    
    def login_screen(self):
        """Màn hình đăng nhập"""
        # Xóa các widget cũ
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame đăng nhập
        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Tiêu đề
        tk.Label(frame, text="QUẢN LÝ KHÁCH SẠN", 
                font=('Arial', 20, 'bold')).pack(pady=20)
        
        # Username
        tk.Label(frame, text="Tên đăng nhập:", font=('Arial', 11)).pack()
        self.username_entry = tk.Entry(frame, font=('Arial', 11), width=30)
        self.username_entry.pack(pady=5)
        
        # Password
        tk.Label(frame, text="Mật khẩu:", font=('Arial', 11)).pack()
        self.password_entry = tk.Entry(frame, font=('Arial', 11), width=30, show='*')
        self.password_entry.pack(pady=5)
        
        # Nút đăng nhập
        tk.Button(frame, text="Đăng Nhập", font=('Arial', 11),
                 width=20, command=self.login).pack(pady=20)
        
        # Hướng dẫn
        tk.Label(frame, text="Mặc định: admin / admin123", 
                font=('Arial', 9)).pack()
        
        # Enter để đăng nhập
        self.password_entry.bind('<Return>', lambda e: self.login())
    
    def login(self):
        """Xử lý đăng nhập"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Lỗi", "Nhập đầy đủ thông tin!")
            return
        
        # Mã hóa password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Kiểm tra đăng nhập
        self.cursor.execute("""
            SELECT user_id, username, full_name 
            FROM users 
            WHERE username=? AND password=?
        """, (username, password_hash))
        
        user = self.cursor.fetchone()
        
        if user:
            self.current_user = user.username
            messagebox.showinfo("Thành công", f"Chào {user.full_name}!")
            self.main_screen()
        else:
            messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")
    
    def main_screen(self):
        """Màn hình chính"""
        # Xóa widgets cũ
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Frame(self.root)
        header.pack(fill='x', pady=5)
        
        tk.Label(header, text="HỆ THỐNG QUẢN LÝ KHÁCH SẠN", 
                font=('Arial', 16, 'bold')).pack(side='left', padx=20)
        
        tk.Label(header, text=f"User: {self.current_user}", 
                font=('Arial', 10)).pack(side='right', padx=10)
        
        tk.Button(header, text="Đăng xuất", 
                 command=self.logout).pack(side='right', padx=10)
        
        # Menu bên trái
        menu_frame = tk.Frame(self.root, width=200)
        menu_frame.pack(side='left', fill='y', padx=5, pady=5)
        
        # Các nút menu
        buttons = [
            ("Trang Chủ", self.dashboard),
            ("Quản Lý Phòng", self.room_management),
            ("Quản Lý Khách", self.customer_management),
            ("Đặt Phòng", self.booking_management),
            ("Báo Cáo", self.reports)
        ]
        
        for text, command in buttons:
            tk.Button(menu_frame, text=text, font=('Arial', 10),
                     width=18, command=command).pack(pady=5)
        
        # Frame nội dung
        self.content = tk.Frame(self.root)
        self.content.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        # Hiển thị dashboard
        self.dashboard()
    
    def logout(self):
        """Đăng xuất"""
        if messagebox.askyesno("Xác nhận", "Bạn muốn đăng xuất?"):
            self.current_user = None
            self.login_screen()
    
    def clear_content(self):
        """Xóa nội dung frame"""
        for widget in self.content.winfo_children():
            widget.destroy()
    
    def dashboard(self):
        """Trang chủ - Thống kê"""
        self.clear_content()
        
        tk.Label(self.content, text="TỔNG QUAN KHÁCH SẠN", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Frame thống kê
        stats = tk.Frame(self.content)
        stats.pack(pady=20)
        
        # Đếm phòng
        self.cursor.execute("SELECT COUNT(*) FROM rooms")
        total_rooms = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM rooms WHERE status=N'Trống'")
        empty_rooms = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM rooms WHERE status=N'Đang sử dụng'")
        occupied = self.cursor.fetchone()[0]
        
        # Đếm khách hàng
        self.cursor.execute("SELECT COUNT(*) FROM customers")
        total_customers = self.cursor.fetchone()[0]
        
        # Đếm đặt phòng hôm nay
        self.cursor.execute("""
            SELECT COUNT(*) FROM bookings 
            WHERE CAST(created_at AS DATE) = CAST(GETDATE() AS DATE)
        """)
        today_bookings = self.cursor.fetchone()[0]
        
        # Hiển thị thống kê
        info = [
            f"Tổng số phòng: {total_rooms}",
            f"Phòng trống: {empty_rooms}",
            f"Đang sử dụng: {occupied}",
            f"Khách hàng: {total_customers}",
            f"Đặt phòng hôm nay: {today_bookings}"
        ]
        
        for text in info:
            tk.Label(stats, text=text, font=('Arial', 12)).pack(pady=5)
        
        # Danh sách đặt phòng gần đây
        tk.Label(self.content, text="Đặt Phòng Gần Đây", 
                font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Treeview
        tree_frame = tk.Frame(self.content)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Khách hàng', 'Phòng', 'Check-in', 'Trạng thái')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')
        
        # Lấy dữ liệu
        self.cursor.execute("""
            SELECT TOP 15 b.booking_id, c.full_name, r.room_number, 
                   b.check_in, b.status
            FROM bookings b
            JOIN customers c ON b.customer_id = c.customer_id
            JOIN rooms r ON b.room_id = r.room_id
            ORDER BY b.created_at DESC
        """)
        
        for row in self.cursor.fetchall():
            tree.insert('', 'end', values=row)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True)
    
    def room_management(self):
        """Quản lý phòng"""
        self.clear_content()
        
        tk.Label(self.content, text="QUẢN LÝ PHÒNG", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Nút chức năng
        btn_frame = tk.Frame(self.content)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Thêm Phòng", 
                 command=self.add_room).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Sửa Phòng", 
                 command=self.edit_room).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Xóa Phòng", 
                 command=self.delete_room).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Làm Mới", 
                 command=self.room_management).pack(side='left', padx=5)
        
        # Treeview
        tree_frame = tk.Frame(self.content)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Số Phòng', 'Loại', 'Giá', 'Trạng Thái')
        self.room_tree = ttk.Treeview(tree_frame, columns=columns, 
                                      show='headings', height=20)
        
        for col in columns:
            self.room_tree.heading(col, text=col)
            self.room_tree.column(col, width=120, anchor='center')
        
        # Lấy dữ liệu
        self.cursor.execute("""
            SELECT room_id, room_number, room_type, price, status
            FROM rooms
            ORDER BY room_number
        """)
        
        for row in self.cursor.fetchall():
            values = list(row)
            values[3] = f"{row[3]:,.0f}"  # Format giá
            self.room_tree.insert('', 'end', values=values)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', 
                                 command=self.room_tree.yview)
        self.room_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.room_tree.pack(side='left', fill='both', expand=True)
    
    def add_room(self):
        """Thêm phòng mới"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Thêm Phòng")
        dialog.geometry("350x300")
        
        # Form nhập liệu
        tk.Label(dialog, text="Số Phòng:").grid(row=0, column=0, padx=10, pady=10)
        number_entry = tk.Entry(dialog, width=25)
        number_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Loại Phòng:").grid(row=1, column=0, padx=10, pady=10)
        type_combo = ttk.Combobox(dialog, width=23, 
                                  values=['Standard', 'Deluxe', 'Suite', 'VIP'])
        type_combo.grid(row=1, column=1, padx=10, pady=10)
        type_combo.set('Standard')
        
        tk.Label(dialog, text="Giá (VNĐ):").grid(row=2, column=0, padx=10, pady=10)
        price_entry = tk.Entry(dialog, width=25)
        price_entry.grid(row=2, column=1, padx=10, pady=10)
        
        def save():
            number = number_entry.get()
            room_type = type_combo.get()
            price = price_entry.get()
            
            if not number or not price:
                messagebox.showerror("Lỗi", "Nhập đầy đủ thông tin!")
                return
            
            try:
                # Thêm phòng
                self.cursor.execute("""
                    INSERT INTO rooms (room_number, room_type, price)
                    VALUES (?, ?, ?)
                """, (number, room_type, float(price)))
                
                self.conn.commit()
                messagebox.showinfo("Thành công", "Đã thêm phòng!")
                dialog.destroy()
                self.room_management()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể thêm: {str(e)}")
        
        tk.Button(dialog, text="Lưu", width=15, 
                 command=save).grid(row=3, column=0, columnspan=2, pady=20)
    
    def edit_room(self):
        """Sửa thông tin phòng"""
        selected = self.room_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Chọn phòng cần sửa!")
            return
        
        item = self.room_tree.item(selected[0])
        room_data = item['values']
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Sửa Phòng")
        dialog.geometry("350x350")
        
        tk.Label(dialog, text="Số Phòng:").grid(row=0, column=0, padx=10, pady=10)
        number_label = tk.Label(dialog, text=room_data[1])
        number_label.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Loại Phòng:").grid(row=1, column=0, padx=10, pady=10)
        type_combo = ttk.Combobox(dialog, width=23, 
                                  values=['Standard', 'Deluxe', 'Suite', 'VIP'])
        type_combo.set(room_data[2])
        type_combo.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Giá (VNĐ):").grid(row=2, column=0, padx=10, pady=10)
        price_entry = tk.Entry(dialog, width=25)
        price_entry.insert(0, room_data[3].replace(',', ''))
        price_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Trạng Thái:").grid(row=3, column=0, padx=10, pady=10)
        status_combo = ttk.Combobox(dialog, width=23, 
                                    values=['Trống', 'Đang sử dụng', 'Bảo trì'])
        status_combo.set(room_data[4])
        status_combo.grid(row=3, column=1, padx=10, pady=10)
        
        def update():
            room_type = type_combo.get()
            price = price_entry.get()
            status = status_combo.get()
            
            try:
                # Cập nhật
                self.cursor.execute("""
                    UPDATE rooms 
                    SET room_type=?, price=?, status=?
                    WHERE room_id=?
                """, (room_type, float(price), status, room_data[0]))
                
                self.conn.commit()
                messagebox.showinfo("Thành công", "Đã cập nhật!")
                dialog.destroy()
                self.room_management()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật: {str(e)}")
        
        tk.Button(dialog, text="Cập Nhật", width=15, 
                 command=update).grid(row=4, column=0, columnspan=2, pady=20)
    
    def delete_room(self):
        """Xóa phòng"""
        selected = self.room_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Chọn phòng cần xóa!")
            return
        
        item = self.room_tree.item(selected[0])
        room_id = item['values'][0]
        room_number = item['values'][1]
        
        if messagebox.askyesno("Xác nhận", f"Xóa phòng {room_number}?"):
            try:
                self.cursor.execute("DELETE FROM rooms WHERE room_id=?", (room_id,))
                self.conn.commit()
                messagebox.showinfo("Thành công", "Đã xóa phòng!")
                self.room_management()
            except:
                messagebox.showerror("Lỗi", "Không thể xóa phòng đã có đặt!")
    
    def customer_management(self):
        """Quản lý khách hàng"""
        self.clear_content()
        
        tk.Label(self.content, text="QUẢN LÝ KHÁCH HÀNG", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Nút chức năng
        btn_frame = tk.Frame(self.content)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Thêm Khách", 
                 command=self.add_customer).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Sửa Thông Tin", 
                 command=self.edit_customer).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Xóa Khách", 
                 command=self.delete_customer).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Làm Mới", 
                 command=self.customer_management).pack(side='left', padx=5)
        
        # Treeview
        tree_frame = tk.Frame(self.content)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Họ Tên', 'Điện Thoại', 'CMND')
        self.customer_tree = ttk.Treeview(tree_frame, columns=columns, 
                                         show='headings', height=20)
        
        for col in columns:
            self.customer_tree.heading(col, text=col)
            self.customer_tree.column(col, width=150, anchor='center')
        
        # Lấy dữ liệu
        self.cursor.execute("""
            SELECT customer_id, full_name, phone, id_card
            FROM customers
            ORDER BY customer_id DESC
        """)
        
        for row in self.cursor.fetchall():
            self.customer_tree.insert('', 'end', values=row)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', 
                                 command=self.customer_tree.yview)
        self.customer_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.customer_tree.pack(side='left', fill='both', expand=True)
    
    def add_customer(self):
        """Thêm khách hàng"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Thêm Khách Hàng")
        dialog.geometry("350x250")
        
        tk.Label(dialog, text="Họ Tên:").grid(row=0, column=0, padx=10, pady=10)
        name_entry = tk.Entry(dialog, width=25)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Điện Thoại:").grid(row=1, column=0, padx=10, pady=10)
        phone_entry = tk.Entry(dialog, width=25)
        phone_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="CMND/CCCD:").grid(row=2, column=0, padx=10, pady=10)
        id_entry = tk.Entry(dialog, width=25)
        id_entry.grid(row=2, column=1, padx=10, pady=10)
        
        def save():
            name = name_entry.get()
            phone = phone_entry.get()
            id_card = id_entry.get()
            
            if not name or not phone or not id_card:
                messagebox.showerror("Lỗi", "Nhập đầy đủ thông tin!")
                return
            
            try:
                self.cursor.execute("""
                    INSERT INTO customers (full_name, phone, id_card)
                    VALUES (?, ?, ?)
                """, (name, phone, id_card))
                
                self.conn.commit()
                messagebox.showinfo("Thành công", "Đã thêm khách hàng!")
                dialog.destroy()
                self.customer_management()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể thêm: {str(e)}")
        
        tk.Button(dialog, text="Lưu", width=15, 
                 command=save).grid(row=3, column=0, columnspan=2, pady=20)
    
    def edit_customer(self):
        """Sửa thông tin khách hàng"""
        selected = self.customer_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Chọn khách hàng cần sửa!")
            return
        
        item = self.customer_tree.item(selected[0])
        data = item['values']
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Sửa Thông Tin")
        dialog.geometry("350x250")
        
        tk.Label(dialog, text="Họ Tên:").grid(row=0, column=0, padx=10, pady=10)
        name_entry = tk.Entry(dialog, width=25)
        name_entry.insert(0, data[1])
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Điện Thoại:").grid(row=1, column=0, padx=10, pady=10)
        phone_entry = tk.Entry(dialog, width=25)
        phone_entry.insert(0, data[2])
        phone_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="CMND:").grid(row=2, column=0, padx=10, pady=10)
        id_label = tk.Label(dialog, text=data[3])
        id_label.grid(row=2, column=1, padx=10, pady=10)
        
        def update():
            name = name_entry.get()
            phone = phone_entry.get()
            
            try:
                self.cursor.execute("""
                    UPDATE customers 
                    SET full_name=?, phone=?
                    WHERE customer_id=?
                """, (name, phone, data[0]))
                
                self.conn.commit()
                messagebox.showinfo("Thành công", "Đã cập nhật!")
                dialog.destroy()
                self.customer_management()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật: {str(e)}")
        
        tk.Button(dialog, text="Cập Nhật", width=15, 
                 command=update).grid(row=3, column=0, columnspan=2, pady=20)
    
    def delete_customer(self):
        """Xóa khách hàng"""
        selected = self.customer_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Chọn khách hàng cần xóa!")
            return
        
        item = self.customer_tree.item(selected[0])
        customer_id = item['values'][0]
        name = item['values'][1]
        
        if messagebox.askyesno("Xác nhận", f"Xóa khách hàng {name}?"):
            try:
                self.cursor.execute("DELETE FROM customers WHERE customer_id=?", 
                                  (customer_id,))
                self.conn.commit()
                messagebox.showinfo("Thành công", "Đã xóa!")
                self.customer_management()
            except:
                messagebox.showerror("Lỗi", "Không thể xóa khách đã có đặt phòng!")
    
    def booking_management(self):
        """Quản lý đặt phòng"""
        self.clear_content()
        
        tk.Label(self.content, text="QUẢN LÝ ĐẶT PHÒNG", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Nút chức năng
        btn_frame = tk.Frame(self.content)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Đặt Phòng Mới", 
                 command=self.add_booking).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Check-in", 
                 command=self.checkin).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Check-out", 
                 command=self.checkout).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Hủy Đặt", 
                 command=self.cancel_booking).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Làm Mới", 
                 command=self.booking_management).pack(side='left', padx=5)
        
        # Treeview
        tree_frame = tk.Frame(self.content)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Khách', 'Phòng', 'Check-in', 'Check-out', 'Giá', 'Trạng thái')
        self.booking_tree = ttk.Treeview(tree_frame, columns=columns, 
                                        show='headings', height=20)
        
        for col in columns:
            self.booking_tree.heading(col, text=col)
            self.booking_tree.column(col, width=110, anchor='center')
        
        # Lấy dữ liệu
        self.cursor.execute("""
            SELECT b.booking_id, c.full_name, r.room_number, 
                   b.check_in, b.check_out, b.total_price, b.status
            FROM bookings b
            JOIN customers c ON b.customer_id = c.customer_id
            JOIN rooms r ON b.room_id = r.room_id
            ORDER BY b.booking_id DESC
        """)
        
        for row in self.cursor.fetchall():
            values = list(row)
            values[5] = f"{row[5]:,.0f}"  # Format giá
            self.booking_tree.insert('', 'end', values=values)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', 
                                 command=self.booking_tree.yview)
        self.booking_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.booking_tree.pack(side='left', fill='both', expand=True)
    
    def add_booking(self):
        """Thêm đặt phòng mới"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Đặt Phòng Mới")
        dialog.geometry("400x400")
        
        # Lấy danh sách khách hàng
        self.cursor.execute("SELECT customer_id, full_name, phone FROM customers")
        customers = self.cursor.fetchall()
        customer_dict = {f"{c.full_name} - {c.phone}": c.customer_id for c in customers}
        
        # Lấy phòng trống
        self.cursor.execute("""
            SELECT room_id, room_number, room_type, price 
            FROM rooms WHERE status=N'Trống'
        """)
        rooms = self.cursor.fetchall()
        room_dict = {f"{r.room_number} - {r.room_type} ({r.price:,.0f})": 
                     (r.room_id, r.price) for r in rooms}
        
        tk.Label(dialog, text="Khách Hàng:").grid(row=0, column=0, padx=10, pady=10)
        customer_combo = ttk.Combobox(dialog, width=30, 
                                      values=list(customer_dict.keys()))
        customer_combo.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Phòng:").grid(row=1, column=0, padx=10, pady=10)
        room_combo = ttk.Combobox(dialog, width=30, 
                                  values=list(room_dict.keys()))
        room_combo.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Check-in (YYYY-MM-DD):").grid(row=2, column=0, 
                                                              padx=10, pady=10)
        checkin_entry = tk.Entry(dialog, width=32)
        checkin_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        checkin_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Check-out (YYYY-MM-DD):").grid(row=3, column=0, 
                                                               padx=10, pady=10)
        checkout_entry = tk.Entry(dialog, width=32)
        checkout_entry.insert(0, (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'))
        checkout_entry.grid(row=3, column=1, padx=10, pady=10)
        
        total_label = tk.Label(dialog, text="Tổng tiền: 0", font=('Arial', 11, 'bold'))
        total_label.grid(row=4, column=0, columnspan=2, pady=10)
        
        def calculate_total(event=None):
            """Tính tổng tiền"""
            try:
                if not room_combo.get() or not checkin_entry.get() or not checkout_entry.get():
                    return
                
                room_info = room_dict.get(room_combo.get())
                if not room_info:
                    return
                
                price = room_info[1]
                checkin = datetime.strptime(checkin_entry.get(), '%Y-%m-%d')
                checkout = datetime.strptime(checkout_entry.get(), '%Y-%m-%d')
                days = (checkout - checkin).days
                
                if days > 0:
                    total = price * days
                    total_label.config(text=f"Tổng tiền: {total:,.0f} VNĐ ({days} ngày)")
            except:
                pass
        
        room_combo.bind('<<ComboboxSelected>>', calculate_total)
        checkin_entry.bind('<KeyRelease>', calculate_total)
        checkout_entry.bind('<KeyRelease>', calculate_total)
        
        def save():
            if not customer_combo.get() or not room_combo.get():
                messagebox.showerror("Lỗi", "Chọn khách hàng và phòng!")
                return
            
            try:
                customer_id = customer_dict[customer_combo.get()]
                room_id, price = room_dict[room_combo.get()]
                checkin = checkin_entry.get()
                checkout = checkout_entry.get()
                
                # Tính số ngày
                checkin_date = datetime.strptime(checkin, '%Y-%m-%d')
                checkout_date = datetime.strptime(checkout, '%Y-%m-%d')
                days = (checkout_date - checkin_date).days
                
                if days <= 0:
                    messagebox.showerror("Lỗi", "Ngày check-out phải sau check-in!")
                    return
                
                total = price * days
                
                # Thêm đặt phòng
                self.cursor.execute("""
                    INSERT INTO bookings (customer_id, room_id, check_in, 
                                        check_out, total_price)
                    VALUES (?, ?, ?, ?, ?)
                """, (customer_id, room_id, checkin, checkout, total))
                
                # Cập nhật trạng thái phòng
                self.cursor.execute("""
                    UPDATE rooms SET status=N'Đã đặt' WHERE room_id=?
                """, (room_id,))
                
                self.conn.commit()
                messagebox.showinfo("Thành công", 
                                  f"Đặt phòng thành công!\nTổng: {total:,.0f} VNĐ")
                dialog.destroy()
                self.booking_management()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể đặt phòng: {str(e)}")
        
        tk.Button(dialog, text="Đặt Phòng", width=20, 
                 command=save).grid(row=5, column=0, columnspan=2, pady=20)
    
    def checkin(self):
        """Check-in"""
        selected = self.booking_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Chọn đặt phòng cần check-in!")
            return
        
        item = self.booking_tree.item(selected[0])
        booking_id = item['values'][0]
        status = item['values'][6]
        
        if status != 'Đã đặt':
            messagebox.showwarning("Cảnh báo", "Chỉ check-in đặt phòng 'Đã đặt'!")
            return
        
        if messagebox.askyesno("Xác nhận", "Xác nhận check-in?"):
            # Lấy room_id
            self.cursor.execute("SELECT room_id FROM bookings WHERE booking_id=?", 
                              (booking_id,))
            room_id = self.cursor.fetchone()[0]
            
            # Cập nhật trạng thái
            self.cursor.execute("""
                UPDATE bookings SET status=N'Đang sử dụng' WHERE booking_id=?
            """, (booking_id,))
            
            self.cursor.execute("""
                UPDATE rooms SET status=N'Đang sử dụng' WHERE room_id=?
            """, (room_id,))
            
            self.conn.commit()
            messagebox.showinfo("Thành công", "Check-in thành công!")
            self.booking_management()
    
    def checkout(self):
        """Check-out"""
        selected = self.booking_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Chọn đặt phòng cần check-out!")
            return
        
        item = self.booking_tree.item(selected[0])
        booking_id = item['values'][0]
        status = item['values'][6]
        
        if status != 'Đang sử dụng':
            messagebox.showwarning("Cảnh báo", "Chỉ check-out phòng 'Đang sử dụng'!")
            return
        
        if messagebox.askyesno("Xác nhận", "Xác nhận check-out?"):
            # Lấy room_id
            self.cursor.execute("SELECT room_id FROM bookings WHERE booking_id=?", 
                              (booking_id,))
            room_id = self.cursor.fetchone()[0]
            
            # Cập nhật trạng thái
            self.cursor.execute("""
                UPDATE bookings SET status=N'Đã hoàn thành' WHERE booking_id=?
            """, (booking_id,))
            
            self.cursor.execute("""
                UPDATE rooms SET status=N'Trống' WHERE room_id=?
            """, (room_id,))
            
            self.conn.commit()
            messagebox.showinfo("Thành công", "Check-out thành công!")
            self.booking_management()
    
    def cancel_booking(self):
        """Hủy đặt phòng"""
        selected = self.booking_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Chọn đặt phòng cần hủy!")
            return
        
        item = self.booking_tree.item(selected[0])
        booking_id = item['values'][0]
        customer = item['values'][1]
        
        if messagebox.askyesno("Xác nhận", f"Hủy đặt phòng của {customer}?"):
            # Lấy room_id
            self.cursor.execute("SELECT room_id FROM bookings WHERE booking_id=?", 
                              (booking_id,))
            room_id = self.cursor.fetchone()[0]
            
            # Cập nhật trạng thái
            self.cursor.execute("""
                UPDATE bookings SET status=N'Đã hủy' WHERE booking_id=?
            """, (booking_id,))
            
            self.cursor.execute("""
                UPDATE rooms SET status=N'Trống' WHERE room_id=?
            """, (room_id,))
            
            self.conn.commit()
            messagebox.showinfo("Thành công", "Đã hủy đặt phòng!")
            self.booking_management()
    
    def reports(self):
        """Báo cáo thống kê"""
        self.clear_content()
        
        tk.Label(self.content, text="BÁO CÁO THỐNG KÊ", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Frame chọn báo cáo
        btn_frame = tk.Frame(self.content)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Doanh Thu Theo Tháng", width=25,
                 command=self.monthly_revenue).pack(pady=5)
        
        tk.Button(btn_frame, text="Tỷ Lệ Lấp Đầy Phòng", width=25,
                 command=self.room_occupancy).pack(pady=5)
        
        tk.Button(btn_frame, text="Top Khách Hàng", width=25,
                 command=self.top_customers).pack(pady=5)
        
        # Frame hiển thị kết quả
        self.report_frame = tk.Frame(self.content)
        self.report_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    def monthly_revenue(self):
        """Báo cáo doanh thu theo tháng"""
        for widget in self.report_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.report_frame, text="DOANH THU 6 THÁNG GẦN NHẤT", 
                font=('Arial', 12, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(self.report_frame)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('Tháng', 'Số Đặt', 'Doanh Thu')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200, anchor='center')
        
        # Lấy dữ liệu 6 tháng
        self.cursor.execute("""
            SELECT FORMAT(created_at, 'MM/yyyy') as month,
                   COUNT(*) as total_bookings,
                   SUM(total_price) as revenue
            FROM bookings
            WHERE created_at >= DATEADD(MONTH, -6, GETDATE())
            GROUP BY FORMAT(created_at, 'MM/yyyy'), 
                     FORMAT(created_at, 'yyyy-MM')
            ORDER BY FORMAT(created_at, 'yyyy-MM') DESC
        """)
        
        total = 0
        for row in self.cursor.fetchall():
            values = (row[0], row[1], f"{row[2]:,.0f}")
            tree.insert('', 'end', values=values)
            total += row[2]
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True)
        
        tk.Label(self.report_frame, text=f"Tổng: {total:,.0f} VNĐ",
                font=('Arial', 11, 'bold')).pack(pady=10)
    
    def room_occupancy(self):
        """Tỷ lệ lấp đầy phòng"""
        for widget in self.report_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.report_frame, text="TỶ LỆ LẤP ĐẦY THEO LOẠI PHÒNG", 
                font=('Arial', 12, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(self.report_frame)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('Loại Phòng', 'Tổng', 'Đang Dùng', 'Tỷ Lệ')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor='center')
        
        # Lấy dữ liệu
        self.cursor.execute("""
            SELECT room_type,
                   COUNT(*) as total,
                   SUM(CASE WHEN status=N'Đang sử dụng' THEN 1 ELSE 0 END) as occupied
            FROM rooms
            GROUP BY room_type
        """)
        
        for row in self.cursor.fetchall():
            rate = (row[2] / row[1] * 100) if row[1] > 0 else 0
            values = (row[0], row[1], row[2], f"{rate:.1f}%")
            tree.insert('', 'end', values=values)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True)
    
    def top_customers(self):
        """Top khách hàng"""
        for widget in self.report_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.report_frame, text="TOP 10 KHÁCH HÀNG", 
                font=('Arial', 12, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(self.report_frame)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('Tên', 'Số Lần', 'Tổng Chi')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200, anchor='center')
        
        # Lấy dữ liệu
        self.cursor.execute("""
            SELECT TOP 10 c.full_name,
                   COUNT(b.booking_id) as total,
                   SUM(b.total_price) as spent
            FROM customers c
            LEFT JOIN bookings b ON c.customer_id = b.customer_id
            GROUP BY c.full_name
            HAVING COUNT(b.booking_id) > 0
            ORDER BY spent DESC
        """)
        
        for row in self.cursor.fetchall():
            values = (row[0], row[1], f"{row[2]:,.0f}")
            tree.insert('', 'end', values=values)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True)
    
    def __del__(self):
        """Đóng kết nối khi thoát"""
        try:
            self.conn.close()
        except:
            pass

# Chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = HotelManagement(root)
    root.mainloop()