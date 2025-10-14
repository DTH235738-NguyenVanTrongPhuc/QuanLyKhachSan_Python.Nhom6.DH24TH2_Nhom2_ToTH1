import psycopg2
from tkinter import messagebox
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            self.create_tables()
            return self.connection
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối Neon:\n{str(e)}")
            return None

    def create_tables(self):
        tables = [
            '''CREATE TABLE IF NOT EXISTS nhanvien (
                maso VARCHAR(50) PRIMARY KEY,
                holot VARCHAR(100),
                ten VARCHAR(50),
                phai VARCHAR(10),
                ngaysinh DATE,
                chucvu VARCHAR(50)
            )''',
            '''CREATE TABLE IF NOT EXISTS khachhang (
                makh VARCHAR(50) PRIMARY KEY,
                hoten VARCHAR(100),
                sdt VARCHAR(20),
                cmnd VARCHAR(20)
            )''',
            '''CREATE TABLE IF NOT EXISTS phong (
                maphong VARCHAR(50) PRIMARY KEY,
                loaiphong VARCHAR(50),
                trangthai VARCHAR(50),
                gia NUMERIC(10,2)
            )''',
            '''CREATE TABLE IF NOT EXISTS datphong (
                madat VARCHAR(50) PRIMARY KEY,
                makh VARCHAR(50),
                maphong VARCHAR(50),
                ngaydat DATE,
                ngaytra DATE
            )'''
        ]
        
        cur = self.connection.cursor()
        for table in tables:
            cur.execute(table)
        self.connection.commit()

    def get_cursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()