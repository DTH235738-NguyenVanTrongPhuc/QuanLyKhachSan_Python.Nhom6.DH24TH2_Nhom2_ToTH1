# database.py - Enhanced version with logging
import psycopg2
from tkinter import messagebox
import logging
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            logging.info(f"🔗 Đang kết nối database: {DB_CONFIG['host']}/{DB_CONFIG['database']}")
            self.connection = psycopg2.connect(**DB_CONFIG)
            logging.info("✅ Kết nối database thành công")
            self.create_tables()
            self.create_default_data()
            return self.connection
        except Exception as e:
            logging.error(f"❌ Lỗi kết nối database: {str(e)}")
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối database:\n{str(e)}")
            return None

    def create_tables(self):
        logging.info("🗃️ Đang tạo bảng...")
        tables = [
            '''CREATE TABLE IF NOT EXISTS nhanvien (
                maso VARCHAR(50) PRIMARY KEY,
                holot VARCHAR(100),
                ten VARCHAR(50),
                phai VARCHAR(10),
                ngaysinh DATE,
                chucvu VARCHAR(50),
                email VARCHAR(100) UNIQUE,
                password VARCHAR(100),
                trangthai VARCHAR(20) DEFAULT 'Active'
            )''',
            '''CREATE TABLE IF NOT EXISTS khachhang (
                makh VARCHAR(50) PRIMARY KEY,
                hoten VARCHAR(100),
                sdt VARCHAR(20),
                cmnd VARCHAR(20),
                ngaytao DATE DEFAULT CURRENT_DATE
            )''',
            '''CREATE TABLE IF NOT EXISTS loaiphong (
                maloai VARCHAR(50) PRIMARY KEY,
                tenloai VARCHAR(100),
                gia NUMERIC(10,2),
                mota TEXT
            )''',
            '''CREATE TABLE IF NOT EXISTS phong (
                maphong VARCHAR(50) PRIMARY KEY,
                maloai VARCHAR(50) REFERENCES loaiphong(maloai),
                trangthai VARCHAR(50) DEFAULT 'Trống',
                ghichu TEXT
            )''',
            '''CREATE TABLE IF NOT EXISTS datphong (
                madat VARCHAR(50) PRIMARY KEY,
                makh VARCHAR(50) REFERENCES khachhang(makh),
                maphong VARCHAR(50) REFERENCES phong(maphong),
                manv VARCHAR(50) REFERENCES nhanvien(maso),
                ngaydat DATE,
                ngaytra DATE,
                trangthai VARCHAR(20) DEFAULT 'Active',
                ngaytao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )'''
        ]
        
        cur = self.connection.cursor()
        for i, table in enumerate(tables):
            try:
                cur.execute(table)
                logging.info(f"✅ Đã tạo bảng {i+1}/{len(tables)}")
            except Exception as e:
                logging.error(f"❌ Lỗi tạo bảng {i+1}: {e}")
        
        self.connection.commit()
        logging.info("✅ Hoàn thành tạo bảng")

    def create_default_data(self):
        logging.info("📝 Đang tạo dữ liệu mặc định...")
        cur = self.connection.cursor()
        
        # Create default manager account if not exists
        cur.execute("SELECT COUNT(*) FROM nhanvien WHERE chucvu='Trưởng phòng'")
        if cur.fetchone()[0] == 0:
            logging.info("👨‍💼 Tạo tài khoản admin mặc định")
            cur.execute("""
                INSERT INTO nhanvien (maso, holot, ten, phai, ngaysinh, chucvu, email, password) 
                VALUES ('AD001', 'Admin', 'System', 'Nam', '2000-01-01', 'Trưởng phòng', 'admin@khachsan.com', 'admin123')
            """)
        
        # Create room types if not exist
        cur.execute("SELECT COUNT(*) FROM loaiphong")
        if cur.fetchone()[0] == 0:
            logging.info("🏨 Tạo loại phòng mặc định")
            room_types = [
                ('LP01', 'Phòng Đơn', 500000, 'Phòng dành cho 1 người'),
                ('LP02', 'Phòng Đôi', 800000, 'Phòng dành cho 2 người'),
                ('LP03', 'Phòng VIP', 1200000, 'Phòng cao cấp')
            ]
            for room_type in room_types:
                cur.execute("INSERT INTO loaiphong VALUES (%s, %s, %s, %s)", room_type)
        
        self.connection.commit()
        logging.info("✅ Hoàn thành tạo dữ liệu mặc định")

    def get_cursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()