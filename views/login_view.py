# views/login_view.py
import tkinter as tk
from tkinter import messagebox
import logging

logger = logging.getLogger(__name__)

class LoginView:
    def __init__(self, notebook, db, on_login_success):
        self.db = db
        self.on_login_success = on_login_success

        # Tạo tab giao diện đăng nhập
        self.tab = tk.Frame(notebook, bg="#ecf0f1")
        self.create_login_ui()

    # ------------------------------------------------------------
    def create_login_ui(self):
        header_frame = tk.Frame(self.tab, bg="#3498db", height=70)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="ĐĂNG NHẬP HỆ THỐNG", bg="#3498db",
                 fg="white", font=("Arial", 16, "bold")).pack(pady=15)

        form_frame = tk.Frame(self.tab, bg="#ecf0f1")
        form_frame.pack(pady=60)

        # Email
        tk.Label(form_frame, text="Email:", font=("Arial", 11), bg="#ecf0f1")\
            .grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.email_entry = tk.Entry(form_frame, width=35, font=("Arial", 11))
        self.email_entry.grid(row=0, column=1, padx=10, pady=10)

        # Mật khẩu
        tk.Label(form_frame, text="Mật khẩu:", font=("Arial", 11), bg="#ecf0f1")\
            .grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = tk.Entry(form_frame, show="*", width=35, font=("Arial", 11))
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Nút
        button_frame = tk.Frame(form_frame, bg="#ecf0f1")
        button_frame.grid(row=2, columnspan=2, pady=20)

        tk.Button(button_frame, text="Đăng nhập", bg="#2ecc71", fg="white",
                  font=("Arial", 11, "bold"), width=12, command=self.login)\
            .grid(row=0, column=0, padx=10)

        tk.Button(button_frame, text="Xóa ô nhập", bg="#e74c3c", fg="white",
                  font=("Arial", 11, "bold"), width=12, command=self.clear_fields)\
            .grid(row=0, column=1, padx=10)

        # Ghi chú
        tk.Label(self.tab, text="Tài khoản mặc định: admin@khachsan.com / admin123",
                 bg="#ecf0f1", fg="gray", font=("Arial", 9, "italic"))\
            .pack(side="bottom", pady=10)

    # ------------------------------------------------------------
    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập email và mật khẩu!")
            return

        try:
            conn = self.db.connection
            if conn is None:
                messagebox.showerror("Lỗi", "Không thể kết nối đến cơ sở dữ liệu.")
                return

            cursor = conn.cursor()

            query = """
                SELECT maso, chucvu, ten, password
                FROM nhanvien
                WHERE LTRIM(RTRIM(email)) = ?
            """
            cursor.execute(query, (email,))
            user = cursor.fetchone()

            if user:
                maso, chucvu, ten, stored_password = user
                # so sánh password
                if password == stored_password:  # Nếu chưa hash
                    logger.info(f" Đăng nhập thành công: {ten} ({maso}) - {chucvu}")
                    messagebox.showinfo("Thành công", f"Xin chào {ten} ({chucvu})!")

                    # Gọi callback với vai trò chính xác
                    if self.on_login_success:
                        self.on_login_success(maso, chucvu, ten)

                else:
                    logger.warning(f" Sai mật khẩu cho email={email}")
                    messagebox.showerror("Sai thông tin", "Email hoặc mật khẩu không đúng.")
            else:
                logger.warning(f" Không tìm thấy user với email={email}")
                messagebox.showerror("Sai thông tin", "Email hoặc mật khẩu không đúng.")

        except Exception as e:
            logger.error(f" Lỗi đăng nhập: {e}", exc_info=True)
            messagebox.showerror("Lỗi đăng nhập", f"Lỗi đăng nhập: {e}")

    # ------------------------------------------------------------
    def clear_fields(self):
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
