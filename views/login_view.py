# login_view.py - Enhanced version for tab integration
import tkinter as tk
from tkinter import ttk, messagebox
import logging

class LoginView:
    def __init__(self, parent, db, on_login_success):
        self.parent = parent
        self.db = db
        self.on_login_success = on_login_success
        logging.info("🔐 Khởi tạo LoginView trong tab")
        self.tab = ttk.Frame(parent)
        self.create_widgets()

    def create_widgets(self):
        try:
            logging.info("🎨 Đang tạo giao diện đăng nhập trong tab...")
            
            # Main frame
            main_frame = tk.Frame(self.tab, bg="#ecf0f1")
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)

            # Header
            header_frame = tk.Frame(main_frame, bg="#3498db", height=80)
            header_frame.pack(fill="x", pady=(0, 20))
            header_frame.pack_propagate(False)
            
            tk.Label(header_frame, text="ĐĂNG NHẬP HỆ THỐNG", bg="#3498db", fg="white",
                    font=("Arial", 16, "bold")).pack(expand=True)

            # Login form
            form_frame = tk.Frame(main_frame, bg="#ecf0f1")
            form_frame.pack(expand=True)

            # Email field
            email_frame = tk.Frame(form_frame, bg="#ecf0f1")
            email_frame.pack(pady=15)
            
            tk.Label(email_frame, text="Email:", bg="#ecf0f1", 
                    font=("Arial", 11), width=10).pack(side="left")
            self.entry_email = ttk.Entry(email_frame, width=30, font=("Arial", 11))
            self.entry_email.pack(side="left", padx=5)
            self.entry_email.focus()

            # Password field
            password_frame = tk.Frame(form_frame, bg="#ecf0f1")
            password_frame.pack(pady=15)
            
            tk.Label(password_frame, text="Mật khẩu:", bg="#ecf0f1",
                    font=("Arial", 11), width=10).pack(side="left")
            self.entry_password = ttk.Entry(password_frame, width=30, show="*", font=("Arial", 11))
            self.entry_password.pack(side="left", padx=5)

            # Buttons frame
            btn_frame = tk.Frame(form_frame, bg="#ecf0f1")
            btn_frame.pack(pady=30)

            tk.Button(btn_frame, text="Đăng nhập", bg="#2ecc71", fg="white",
                     font=("Arial", 12, "bold"), width=15, height=2,
                     command=self.login).pack(side="left", padx=20)
            
            tk.Button(btn_frame, text="Đăng xuất", bg="#e74c3c", fg="white",
                     font=("Arial", 12, "bold"), width=15, height=2,
                     command=self.logout).pack(side="left", padx=20)

            # Bind Enter key to login
            self.entry_password.bind('<Return>', lambda e: self.login())
            
            # Default credentials hint
            hint_frame = tk.Frame(main_frame, bg="#ecf0f1")
            hint_frame.pack(fill="x", pady=10)
            
            hint_text = "Tài khoản mặc định: admin@khachsan.com / admin123"
            tk.Label(hint_frame, text=hint_text, bg="#ecf0f1", fg="#7f8c8d",
                    font=("Arial", 9)).pack()
            
            logging.info("✅ Đã tạo giao diện đăng nhập trong tab thành công")
            
        except Exception as e:
            logging.error(f"❌ Lỗi tạo giao diện đăng nhập: {str(e)}")
            messagebox.showerror("Lỗi", f"Không thể tạo giao diện đăng nhập: {str(e)}")

    def login(self):
        email = self.entry_email.get().strip()
        password = self.entry_password.get()

        logging.info(f"🔐 Đang thử đăng nhập với email: {email}")

        if not email or not password:
            logging.warning("⚠️ Email hoặc mật khẩu trống")
            messagebox.showerror("Lỗi", "Vui lòng nhập email và mật khẩu")
            return

        try:
            cur = self.db.get_cursor()
            cur.execute("SELECT maso, chucvu, holot, ten FROM nhanvien WHERE email=%s AND password=%s", 
                       (email, password))
            user = cur.fetchone()

            if user:
                user_id, role, holot, ten = user
                user_name = f"{holot} {ten}"
                logging.info(f"✅ Đăng nhập thành công: {user_name} ({user_id})")
                
                # Clear password field
                self.entry_password.delete(0, tk.END)
                
                # Call success callback
                self.on_login_success(user_id, role, user_name)
                
                messagebox.showinfo("Thành công", f"Đăng nhập thành công!\nXin chào {user_name}")
            else:
                logging.warning("❌ Đăng nhập thất bại: Email hoặc mật khẩu không đúng")
                messagebox.showerror("Lỗi", "Email hoặc mật khẩu không đúng")
        except Exception as e:
            logging.error(f"❌ Lỗi đăng nhập: {str(e)}")
            messagebox.showerror("Lỗi", f"Lỗi đăng nhập: {str(e)}")

    def logout(self):
        """Clear login form"""
        self.entry_email.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_email.focus()
        messagebox.showinfo("Thông báo", "Đã đăng xuất. Vui lòng đăng nhập lại để tiếp tục.")