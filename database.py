# database.py - Phiên bản hoàn chỉnh ổn định cho SQL Server
import pyodbc
from tkinter import messagebox
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    # ---------------------------------------------------------
    def connect(self):
        """Kết nối SQL Server"""
        try:
            conn_str = (
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=LAPTOP-DN604OJP;"
                "DATABASE=QuanLyKhachSan1;"
                "UID=Admin;"
                "PWD=admin123;"
                "TrustServerCertificate=yes;"
                "Encrypt=no;"
                "CHARSET=UTF8;"

            )
            self.connection = pyodbc.connect(conn_str)
            logger.info(" Kết nối SQL Server thành công!")

            # Tạo bảng nếu chưa có
            self.create_tables()
            return self.connection

        except Exception as e:
            logger.error(f"Lỗi kết nối SQL Server: {str(e)}")
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối database:\n{str(e)}")
            self.connection = None
            return None

    # ---------------------------------------------------------
    def create_tables(self):
        """Tạo các bảng nếu chưa có"""
        cur = self.connection.cursor()
        tables = [
            '''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='nhanvien' AND xtype='U')
            CREATE TABLE nhanvien (
                maso VARCHAR(50) PRIMARY KEY,
                holot NVARCHAR(100),
                ten NVARCHAR(50),
                phai NVARCHAR(10),
                ngaysinh DATE,
                chucvu NVARCHAR(50),
                email NVARCHAR(100) UNIQUE,
                password NVARCHAR(100),
                trangthai NVARCHAR(20) DEFAULT N'Active'
            )
            ''',
            '''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='khachhang' AND xtype='U')
            CREATE TABLE khachhang (
                makh VARCHAR(50) PRIMARY KEY,
                hoten NVARCHAR(100),
                sdt NVARCHAR(20),
                cmnd NVARCHAR(20),
                ngaytao DATE DEFAULT GETDATE()
            )
            ''',
            '''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='loaiphong' AND xtype='U')
            CREATE TABLE loaiphong (
                maloai VARCHAR(50) PRIMARY KEY,
                tenloai NVARCHAR(100),
                gia DECIMAL(10,2),
                mota NVARCHAR(MAX)
            )
            ''',
            '''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='phong' AND xtype='U')
            CREATE TABLE phong (
                maphong VARCHAR(50) PRIMARY KEY,
                maloai VARCHAR(50) FOREIGN KEY REFERENCES loaiphong(maloai),
                trangthai NVARCHAR(50) DEFAULT N'Trống',
                ghichu NVARCHAR(MAX)
            )
            ''',
            '''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='datphong' AND xtype='U')
            CREATE TABLE datphong (
                madat VARCHAR(50) PRIMARY KEY,
                makh VARCHAR(50) FOREIGN KEY REFERENCES khachhang(makh),
                maphong VARCHAR(50) FOREIGN KEY REFERENCES phong(maphong),
                manv VARCHAR(50) FOREIGN KEY REFERENCES nhanvien(maso),
                ngaydat DATE,
                ngaytra DATE,
                trangthai NVARCHAR(20) DEFAULT N'Active',
                ngaytao DATETIME DEFAULT GETDATE()
            )
            '''
        ]

        for sql in tables:
            cur.execute(sql)
        self.connection.commit()
        logger.info(" Hoàn tất tạo bảng!")

    # ---------------------------------------------------------
    def get_cursor(self):
        if self.connection is None:
            raise Exception("Chưa kết nối database")
        return self.connection.cursor()

    def commit(self):
        if self.connection:
            self.connection.commit()

    # ---------------------------------------------------------
    # NHÂN VIÊN
    def them_nhanvien(self, maso, holot, ten, phai, ngaysinh, chucvu, email, password):
        try:
            cur = self.get_cursor()
            sql = (
                "INSERT INTO nhanvien (maso, holot, ten, phai, ngaysinh, chucvu, email, password) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            )
            print(" SQL:", sql)
            print("Params:", maso, holot, ten, phai, ngaysinh, chucvu, email, password)

            cur.execute(sql, (maso, holot, ten, phai, ngaysinh, chucvu, email, password))
            self.commit()
            logger.info(f"Đã thêm nhân viên {ten}")
        except Exception as e:
            logger.error(f"Lỗi thêm nhân viên: {e}")
            messagebox.showerror("Lỗi", f"Không thể thêm nhân viên:\n{e}")



    def sua_nhanvien(self, maso, holot, ten, phai, ngaysinh, chucvu, email):
        try:
            cur = self.get_cursor()
            cur.execute("""
                UPDATE nhanvien
                SET holot=?, ten=?, phai=?, ngaysinh=?, chucvu=?, email=?
                WHERE maso=?
            """, (holot, ten, phai, ngaysinh, chucvu, email, maso))
            self.commit()
            logger.info(f"Cập nhật nhân viên {maso}")
        except Exception as e:
            logger.error(f" Lỗi cập nhật nhân viên: {e}")

    def xoa_nhanvien(self, maso):
        try:
            cur = self.get_cursor()
            cur.execute("DELETE FROM nhanvien WHERE maso=?", (maso,))
            self.commit()
            logger.info(f" Đã xóa nhân viên {maso}")
        except Exception as e:
            logger.error(f" Lỗi xóa nhân viên: {e}")

    # ---------------------------------------------------------
    # KHÁCH HÀNG
    def them_khachhang(self, makh, hoten, sdt, cmnd):
        try:
            cur = self.get_cursor()
            cur.execute("""
                INSERT INTO khachhang (makh, hoten, sdt, cmnd)
                VALUES (?, ?, ?, ?)
            """, (makh, hoten, sdt, cmnd))
            self.commit()
            logger.info(f" Đã thêm khách hàng {hoten}")
        except Exception as e:
            logger.error(f" Lỗi thêm khách hàng: {e}")
            messagebox.showerror("Lỗi", f"Không thể thêm khách hàng:\n{e}")

    # ---------------------------------------------------------
    # LOẠI PHÒNG
    def them_loaiphong(self, maloai, tenloai, gia, mota):
        try:
            cur = self.get_cursor()
            cur.execute("""
                INSERT INTO loaiphong (maloai, tenloai, gia, mota)
                VALUES (?, ?, ?, ?)
            """, (maloai, tenloai, gia, mota))
            self.commit()
            logger.info(f" Đã thêm loại phòng {tenloai}")
        except Exception as e:
            logger.error(f" Lỗi thêm loại phòng: {e}")
            messagebox.showerror("Lỗi", f"Không thể thêm loại phòng:\n{e}")

    # ---------------------------------------------------------
    # PHÒNG
    def them_phong(self, maphong, maloai, ghichu):
        try:
            cur = self.get_cursor()
            cur.execute("""
                INSERT INTO phong (maphong, maloai, ghichu)
                VALUES (?, ?, ?)
            """, (maphong, maloai, ghichu))
            self.commit()
            logger.info(f" Đã thêm phòng {maphong}")
        except Exception as e:
            logger.error(f" Lỗi thêm phòng: {e}")
            messagebox.showerror("Lỗi", f"Không thể thêm phòng:\n{e}")

    # ---------------------------------------------------------
    # ĐẶT PHÒNG
    def them_datphong(self, madat, makh, maphong, manv, ngaydat, ngaytra):
        try:
            cur = self.get_cursor()
            cur.execute("""
                INSERT INTO datphong (madat, makh, maphong, manv, ngaydat, ngaytra)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (madat, makh, maphong, manv, ngaydat, ngaytra))
            self.commit()
            logger.info(f" Đã thêm đặt phòng {madat}")
        except Exception as e:
            logger.error(f" Lỗi thêm đặt phòng: {e}")
            messagebox.showerror("Lỗi", f"Không thể thêm đặt phòng:\n{e}")
    
    def sua_datphong(self, madat, makh, maphong, manv, ngaydat, ngaytra, trangthai):
        try:
            cur = self.get_cursor()
            cur.execute("""
                UPDATE datphong
                SET makh=?, maphong=?, manv=?, ngaydat=?, ngaytra=?, trangthai=?
                WHERE madat=?
            """, (makh, maphong, manv, ngaydat, ngaytra, trangthai, madat))
            self.commit()
            logger.info(f" Đã cập nhật đặt phòng {madat}")
        except Exception as e:
            logger.error(f" Lỗi cập nhật đặt phòng: {e}")
            messagebox.showerror("Lỗi", f"Không thể cập nhật đặt phòng:\n{e}")
