"""
HỆ THỐNG QUẢN LÝ KHÁCH SẠN - SQL SERVER VERSION
Ứng dụng desktop quản lý khách sạn
Sử dụng: Tkinter + SQL Server
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pyodbc
from datetime import datetime, timedelta
import hashlib
import re

class HotelManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("🏨 Hệ Thống Quản Lý Khách Sạn")
        self.root.geometry("1400x800")
        
        # Maximize window
        try:
            self.root.state('zoomed')
        except:
            try:
                self.root.attributes('-zoomed', True)
            except:
                self.root.state('normal')
        
        self.current_user = None
        self.current_user_role = None
        
        # Kết nối SQL Server
        if not self.connect_database():
            messagebox.showerror("Lỗi", "Không thể kết nối đến SQL Server!")
            self.root.destroy()
            return
        
        # Khởi tạo database
        self.init_database()
        
        # Hiển thị màn hình đăng nhập
        self.show_login_screen()
    
    def connect_database(self):
        """Kết nối đến SQL Server"""
        try:
            # CẤU HÌNH KẾT NỐI - THAY ĐỔI THEO MÔI TRƯỜNG CỦA BẠN
            server = 'localhost\\SQLEXPRESS'  # hoặc 'localhost' hoặc IP server
            database = 'HotelManagement'
            
            # Tùy chọn 1: Windows Authentication (khuyến nghị)
            connection_string = f'''
                DRIVER={{ODBC Driver 17 for SQL Server}};
                SERVER={server};
                DATABASE={database};
                Trusted_Connection=yes;
            '''
            
            # Tùy chọn 2: SQL Server Authentication
            # username = 'sa'
            # password = 'your_password'
            # connection_string = f'''
            #     DRIVER={{ODBC Driver 17 for SQL Server}};
            #     SERVER={server};
            #     DATABASE={database};
            #     UID={username};
            #     PWD={password};
            # '''
            
            self.conn = pyodbc.connect(connection_string)
            self.cursor = self.conn.cursor()
            
            # Tạo database nếu chưa tồn tại
            try:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.commit()
            except:
                pass
            
            return True
            
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", f"Lỗi: {str(e)}\n\nVui lòng kiểm tra:\n1. SQL Server đã được cài đặt\n2. SQL Server Service đang chạy\n3. Cấu hình kết nối đúng")
            return False
    
    def init_database(self):
        """Khởi tạo các bảng trong database"""
        try:
            # Bảng Users
            self.cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
                CREATE TABLE users (
                    user_id INT IDENTITY(1,1) PRIMARY KEY,
                    username NVARCHAR(50) UNIQUE NOT NULL,
                    password NVARCHAR(100) NOT NULL,
                    full_name NVARCHAR(100) NOT NULL,
                    role NVARCHAR(20) NOT NULL,
                    email NVARCHAR(100),
                    phone NVARCHAR(20),
                    created_at DATETIME DEFAULT GETDATE()
                )
            ''')
            
            # Bảng Rooms
            self.cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='rooms' AND xtype='U')
                CREATE TABLE rooms (
                    room_id INT IDENTITY(1,1) PRIMARY KEY,
                    room_number NVARCHAR(10) UNIQUE NOT NULL,
                    room_type NVARCHAR(20) NOT NULL,
                    price DECIMAL(18,2) NOT NULL,
                    status NVARCHAR(20) DEFAULT N'Trống',
                    floor INT,
                    description NVARCHAR(500),
                    created_at DATETIME DEFAULT GETDATE()
                )
            ''')
            
            # Bảng Customers
            self.cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='customers' AND xtype='U')
                CREATE TABLE customers (
                    customer_id INT IDENTITY(1,1) PRIMARY KEY,
                    full_name NVARCHAR(100) NOT NULL,
                    id_card NVARCHAR(20) UNIQUE NOT NULL,
                    phone NVARCHAR(20) NOT NULL,
                    email NVARCHAR(100),
                    address NVARCHAR(200),
                    created_at DATETIME DEFAULT GETDATE()
                )
            ''')
            
            # Bảng Bookings
            self.cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='bookings' AND xtype='U')
                CREATE TABLE bookings (
                    booking_id INT IDENTITY(1,1) PRIMARY KEY,
                    customer_id INT NOT NULL,
                    room_id INT NOT NULL,
                    check_in DATE NOT NULL,
                    check_out DATE NOT NULL,
                    total_price DECIMAL(18,2) NOT NULL,
                    deposit DECIMAL(18,2) DEFAULT 0,
                    status NVARCHAR(20) DEFAULT N'Đã đặt',
                    notes NVARCHAR(500),
                    created_at DATETIME DEFAULT GETDATE(),
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
                )
            ''')
            
            # Bảng Payments
            self.cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='payments' AND xtype='U')
                CREATE TABLE payments (
                    payment_id INT IDENTITY(1,1) PRIMARY KEY,
                    booking_id INT NOT NULL,
                    amount DECIMAL(18,2) NOT NULL,
                    payment_date DATETIME DEFAULT GETDATE(),
                    payment_method NVARCHAR(50) NOT NULL,
                    notes NVARCHAR(500),
                    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
                )
            ''')
            
            # Bảng Services
            self.cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='services' AND xtype='U')
                CREATE TABLE services (
                    service_id INT IDENTITY(1,1) PRIMARY KEY,
                    booking_id INT NOT NULL,
                    service_name NVARCHAR(100) NOT NULL,
                    price DECIMAL(18,2) NOT NULL,
                    quantity INT DEFAULT 1,
                    service_date DATETIME DEFAULT GETDATE(),
                    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
                )
            ''')
            
            self.conn.commit()
            
            # Tạo tài khoản admin mặc định
            self.create_default_admin()
            
            # Tạo dữ liệu mẫu
            self.create_sample_data()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khởi tạo database: {str(e)}")
    
    def create_default_admin(self):
        """Tạo tài khoản admin mặc định"""
        try:
            # Kiểm tra xem admin đã tồn tại chưa
            self.cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
            if self.cursor.fetchone()[0] == 0:
                password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
                self.cursor.execute('''
                    INSERT INTO users (username, password, full_name, role, email, phone)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', ('admin', password_hash, 'Administrator', 'Admin', 'admin@hotel.com', '0123456789'))
                self.conn.commit()
        except Exception as e:
            pass
    
    def create_sample_data(self):
        """Tạo dữ liệu mẫu cho phòng"""
        try:
            self.cursor.execute('SELECT COUNT(*) FROM rooms')
            if self.cursor.fetchone()[0] == 0:
                rooms_data = [
                    ('101', 'Standard', 500000, N'Trống', 1, N'Phòng đơn tiêu chuẩn'),
                    ('102', 'Standard', 500000, N'Trống', 1, N'Phòng đơn tiêu chuẩn'),
                    ('201', 'Deluxe', 800000, N'Trống', 2, N'Phòng đôi cao cấp'),
                    ('202', 'Deluxe', 800000, N'Trống', 2, N'Phòng đôi cao cấp'),
                    ('301', 'Suite', 1500000, N'Trống', 3, N'Phòng Suite sang trọng'),
                    ('302', 'VIP', 2000000, N'Trống', 3, N'Phòng VIP đặc biệt'),
                ]
                
                for room in rooms_data:
                    self.cursor.execute('''
                        INSERT INTO rooms (room_number, room_type, price, status, floor, description)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', room)
                
                self.conn.commit()
        except Exception as e:
            pass
    
    def hash_password(self, password):
        """Mã hóa mật khẩu"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def show_login_screen(self):
        """Hiển thị màn hình đăng nhập"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        login_frame = tk.Frame(self.root, bg='#2c3e50')
        login_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        title_label = tk.Label(login_frame, text="🏨 QUẢN LÝ KHÁCH SẠN", 
                               font=('Arial', 28, 'bold'), bg='#2c3e50', fg='white')
        title_label.pack(pady=20)
        
        form_frame = tk.Frame(login_frame, bg='#34495e', padx=40, pady=30)
        form_frame.pack(padx=20, pady=20)
        
        tk.Label(form_frame, text="Tên đăng nhập:", font=('Arial', 12), 
                bg='#34495e', fg='white').grid(row=0, column=0, sticky='w', pady=10)
        self.username_entry = tk.Entry(form_frame, font=('Arial', 12), width=25)
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)
        
        tk.Label(form_frame, text="Mật khẩu:", font=('Arial', 12), 
                bg='#34495e', fg='white').grid(row=1, column=0, sticky='w', pady=10)
        self.password_entry = tk.Entry(form_frame, font=('Arial', 12), width=25, show='*')
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)
        
        login_btn = tk.Button(form_frame, text="Đăng Nhập", font=('Arial', 12, 'bold'),
                             bg='#27ae60', fg='white', width=20, cursor='hand2',
                             command=self.login)
        login_btn.grid(row=2, column=0, columnspan=2, pady=20)
        
        info_label = tk.Label(login_frame, 
                            text="Tài khoản mặc định: admin / admin123",
                            font=('Arial', 10), bg='#2c3e50', fg='#ecf0f1')
        info_label.pack(pady=10)
        
        self.password_entry.bind('<Return>', lambda e: self.login())
        self.username_entry.focus()
    
    def login(self):
        """Xử lý đăng nhập"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        password_hash = self.hash_password(password)
        
        self.cursor.execute('''
            SELECT user_id, username, full_name, role 
            FROM users 
            WHERE username = ? AND password = ?
        ''', (username, password_hash))
        
        user = self.cursor.fetchone()
        
        if user:
            self.current_user = user[1]
            self.current_user_role = user[3]
            messagebox.showinfo("Thành công", f"Chào mừng {user[2]}!")
            self.show_main_screen()
        else:
            messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")
    
    def logout(self):
        """Đăng xuất"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đăng xuất?"):
            self.current_user = None
            self.current_user_role = None
            self.show_login_screen()
    
    def show_main_screen(self):
        """Hiển thị màn hình chính"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')
        
        tk.Label(header_frame, text="🏨 HỆ THỐNG QUẢN LÝ KHÁCH SẠN", 
                font=('Arial', 20, 'bold'), bg='#2c3e50', fg='white').pack(side='left', padx=20, pady=20)
        
        user_info = tk.Label(header_frame, text=f"👤 {self.current_user} ({self.current_user_role})", 
                            font=('Arial', 11), bg='#2c3e50', fg='white')
        user_info.pack(side='right', padx=10)
        
        logout_btn = tk.Button(header_frame, text="Đăng xuất", font=('Arial', 10),
                              bg='#e74c3c', fg='white', cursor='hand2',
                              command=self.logout)
        logout_btn.pack(side='right', padx=10)
        
        # Menu
        menu_frame = tk.Frame(self.root, bg='#34495e', width=200)
        menu_frame.pack(side='left', fill='y')
        
        menu_buttons = [
            ("🏠 Trang Chủ", self.show_dashboard),
            ("🛏️ Quản Lý Phòng", self.show_room_management),
            ("👥 Quản Lý Khách Hàng", self.show_customer_management),
            ("📅 Đặt Phòng", self.show_booking_management),
            ("💰 Thanh Toán", self.show_payment_management),
        ]
        
        for text, command in menu_buttons:
            btn = tk.Button(menu_frame, text=text, font=('Arial', 11),
                          bg='#34495e', fg='white', cursor='hand2',
                          width=20, height=2, anchor='w', padx=20,
                          relief='flat', command=command)
            btn.pack(fill='x', pady=2)
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#2c3e50'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='#34495e'))
        
        # Content
        self.content_frame = tk.Frame(self.root, bg='#ecf0f1')
        self.content_frame.pack(side='right', fill='both', expand=True)
        
        self.show_dashboard()
    
    def clear_content_frame(self):
        """Xóa nội dung frame chính"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Hiển thị dashboard - tương tự code SQLite nhưng có điều chỉnh query"""
        self.clear_content_frame()
        
        tk.Label(self.content_frame, text="📊 TRANG CHỦ - THỐNG KÊ TỔNG QUAN", 
                font=('Arial', 18, 'bold'), bg='#ecf0f1').pack(pady=20)
        
        stats_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        stats_frame.pack(pady=20, padx=20, fill='x')
        
        # Các thống kê
        self.cursor.execute('SELECT COUNT(*) FROM rooms')
        total_rooms = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM rooms WHERE status=N'Trống'")
        empty_rooms = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM rooms WHERE status=N'Đang sử dụng'")
        occupied_rooms = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(*) FROM customers')
        total_customers = self.cursor.fetchone()[0]
        
        today = datetime.now().strftime('%Y-%m-%d')
        self.cursor.execute("SELECT COUNT(*) FROM bookings WHERE CONVERT(DATE, created_at) = ?", (today,))
        today_bookings = self.cursor.fetchone()[0]
        
        current_month = datetime.now().strftime('%Y-%m')
        self.cursor.execute("""
            SELECT ISNULL(SUM(amount), 0) FROM payments 
            WHERE FORMAT(payment_date, 'yyyy-MM') = ?
        """, (current_month,))
        monthly_revenue = self.cursor.fetchone()[0]
        
        stats_data = [
            ("🏠 Tổng số phòng", total_rooms, "#3498db"),
            ("✅ Phòng trống", empty_rooms, "#27ae60"),
            ("🔴 Đang sử dụng", occupied_rooms, "#e74c3c"),
            ("👥 Khách hàng", total_customers, "#9b59b6"),
            ("📅 Đặt phòng hôm nay", today_bookings, "#f39c12"),
            ("💰 Doanh thu tháng", f"{monthly_revenue:,.0f} đ", "#16a085"),
        ]
        
        for i, (label, value, color) in enumerate(stats_data):
            card = tk.Frame(stats_frame, bg=color, width=200, height=120)
            card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky='nsew')
            
            tk.Label(card, text=label, font=('Arial', 11), 
                    bg=color, fg='white').pack(pady=10)
            tk.Label(card, text=str(value), font=('Arial', 20, 'bold'), 
                    bg=color, fg='white').pack(pady=5)
        
        for i in range(3):
            stats_frame.columnconfigure(i, weight=1)
    
    def show_room_management(self):
        """Quản lý phòng - Placeholder"""
        self.clear_content_frame()
        tk.Label(self.content_frame, text="🛏️ QUẢN LÝ PHÒNG", 
                font=('Arial', 18, 'bold'), bg='#ecf0f1').pack(pady=20)
        tk.Label(self.content_frame, text="Chức năng đang được phát triển...", 
                font=('Arial', 12), bg='#ecf0f1').pack(pady=20)
    
    def show_customer_management(self):
        """Quản lý khách hàng - Placeholder"""
        self.clear_content_frame()
        tk.Label(self.content_frame, text="👥 QUẢN LÝ KHÁCH HÀNG", 
                font=('Arial', 18, 'bold'), bg='#ecf0f1').pack(pady=20)
        tk.Label(self.content_frame, text="Chức năng đang được phát triển...", 
                font=('Arial', 12), bg='#ecf0f1').pack(pady=20)
    
    def show_booking_management(self):
        """Quản lý đặt phòng - Placeholder"""
        self.clear_content_frame()
        tk.Label(self.content_frame, text="📅 QUẢN LÝ ĐẶT PHÒNG", 
                font=('Arial', 18, 'bold'), bg='#ecf0f1').pack(pady=20)
        tk.Label(self.content_frame, text="Chức năng đang được phát triển...", 
                font=('Arial', 12), bg='#ecf0f1').pack(pady=20)
    
    def show_payment_management(self):
        """Quản lý thanh toán - Placeholder"""
        self.clear_content_frame()
        tk.Label(self.content_frame, text="💰 QUẢN LÝ THANH TOÁN", 
                font=('Arial', 18, 'bold'), bg='#ecf0f1').pack(pady=20)
        tk.Label(self.content_frame, text="Chức năng đang được phát triển...", 
                font=('Arial', 12), bg='#ecf0f1').pack(pady=20)
    
    def __del__(self):
        """Đóng kết nối khi thoát"""
        try:
            self.conn.close()
        except:
            pass

# Chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = HotelManagementSystem(root)
    root.mainloop()