import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

class EmployeeView:
    def __init__(self, parent, db, current_user_role=None):
        self.db = db
        self.current_user_role = current_user_role
        self.tab = ttk.Frame(parent)
        self.create_widgets()
        self.load_data()

    # ------------------------------------------------------------
    def create_widgets(self):
        # Thông tin nhân viên
        frame_info = tk.LabelFrame(self.tab, text="Thông tin nhân viên")
        frame_info.pack(padx=10, pady=10, fill="x")

        tk.Label(frame_info, text="Mã số").grid(row=0, column=0, padx=5, pady=5)
        self.entry_maso = tk.Entry(frame_info, width=10)
        self.entry_maso.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_info, text="Họ lót").grid(row=0, column=2, padx=5, pady=5)
        self.entry_holot = tk.Entry(frame_info, width=20)
        self.entry_holot.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_info, text="Tên").grid(row=0, column=4, padx=5, pady=5)
        self.entry_ten = tk.Entry(frame_info, width=15)
        self.entry_ten.grid(row=0, column=5, padx=5, pady=5)

        self.gender_var = tk.StringVar(value="Nam")
        tk.Label(frame_info, text="Giới tính").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Radiobutton(frame_info, text="Nam", variable=self.gender_var, value="Nam").grid(row=1, column=1, padx=5, sticky="w")
        tk.Radiobutton(frame_info, text="Nữ", variable=self.gender_var, value="Nữ").grid(row=1, column=2, padx=5, sticky="w")

        tk.Label(frame_info, text="Ngày sinh").grid(row=1, column=3, padx=5, pady=5)
        self.date_entry = DateEntry(frame_info, width=12, background="darkblue",
                                    foreground="white", date_pattern="yyyy-mm-dd")
        self.date_entry.grid(row=1, column=4, padx=5, pady=5)

        tk.Label(frame_info, text="Chức vụ").grid(row=1, column=5, padx=5, pady=5)
        self.cbb_chucvu = ttk.Combobox(frame_info, values=["Trưởng phòng", "Nhân viên"], width=18)
        self.cbb_chucvu.grid(row=1, column=6, padx=5, pady=5)

        tk.Label(frame_info, text="Email").grid(row=2, column=0, padx=5, pady=5)
        self.entry_email = tk.Entry(frame_info, width=20)
        self.entry_email.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_info, text="Password").grid(row=2, column=2, padx=5, pady=5)
        self.entry_password = tk.Entry(frame_info, width=20, show="*")
        self.entry_password.grid(row=2, column=3, padx=5, pady=5)

        # Treeview hiển thị danh sách nhân viên
        columns = ("maso", "holot", "ten", "phai", "ngaysinh", "chucvu", "email")
        self.tree = ttk.Treeview(self.tab, columns=columns, show="headings", height=15)

        headings = {
            "maso": "MÃ SỐ",
            "holot": "HỌ LÓT",
            "ten": "TÊN",
            "phai": "GIỚI TÍNH",
            "ngaysinh": "NGÀY SINH",
            "chucvu": "CHỨC VỤ",
            "email": "EMAIL"
        }
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=110)

        self.tree.pack(padx=10, pady=10, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Các nút chức năng
        frame_btn = tk.Frame(self.tab)
        frame_btn.pack(pady=5)

        buttons = [
            ("Thêm", self.add_employee, "#4CAF50"),
            ("Sửa", self.edit_employee, "#2196F3"),
            ("Lưu", self.save_employee, "#FF9800"),
            ("Xóa", self.delete_employee, "#f44336"),
            ("Làm mới", self.refresh_data, "#607D8B")
        ]
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(frame_btn, text=text, width=8, bg=color, fg="white",
                            command=lambda c=command, t=text: self.button_action(c, t))
            btn.grid(row=0, column=i, padx=5)

    # ------------------------------------------------------------
    def check_role(self, action_name):
        if self.current_user_role != "Trưởng phòng":
            messagebox.showwarning("Cảnh báo", f"⚠ Chỉ Trưởng phòng mới có thể {action_name}!")
            return False
        return True

    def button_action(self, func, name):
        if name in ["Thêm", "Sửa", "Xóa", "Lưu"] and not self.check_role(name.lower()):
            return
        func()

    # ------------------------------------------------------------
    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        cur = self.db.get_cursor()
        cur.execute("SELECT maso, holot, ten, phai, ngaysinh, chucvu, email FROM nhanvien")
        for row in cur.fetchall():
            clean_row = []
            for val in row:
                if isinstance(val, tuple):
                    val = val[0]
                elif hasattr(val, "strftime"):
                    val = val.strftime("%Y-%m-%d")
                clean_row.append(val)
            self.tree.insert("", tk.END, values=clean_row)

    # ------------------------------------------------------------
    def add_employee(self):
        if not all([self.entry_maso.get(), self.entry_holot.get(), self.entry_ten.get(),
                    self.cbb_chucvu.get(), self.entry_email.get(), self.entry_password.get()]):
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin")
            return
        try:
            cur = self.db.get_cursor()
            cur.execute(
                "INSERT INTO nhanvien (maso, holot, ten, phai, ngaysinh, chucvu, email, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (self.entry_maso.get(), self.entry_holot.get(), self.entry_ten.get(),
                 self.gender_var.get(), self.date_entry.get(), self.cbb_chucvu.get(),
                 self.entry_email.get(), self.entry_password.get())
            )
            self.db.commit()
            self.load_data()
            self.clear_form()
            messagebox.showinfo("Thành công", "Thêm nhân viên thành công")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm nhân viên: {str(e)}")

    # ------------------------------------------------------------
    def delete_employee(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên cần xóa")
            return
        maso = self.tree.item(sel)["values"][0]
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa nhân viên {maso}?"):
            try:
                cur = self.db.get_cursor()
                cur.execute("DELETE FROM nhanvien WHERE maso = ?", (maso,))
                self.db.commit()
                self.load_data()
                self.clear_form()
                messagebox.showinfo("Thành công", "Xóa nhân viên thành công")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa nhân viên: {str(e)}")

    # ------------------------------------------------------------
    def edit_employee(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên cần sửa")
            return
        v = self.tree.item(sel)["values"]
        self.entry_maso.delete(0, tk.END)
        self.entry_maso.insert(0, v[0])
        self.entry_maso.config(state="disabled")
        self.entry_holot.delete(0, tk.END)
        self.entry_holot.insert(0, v[1])
        self.entry_ten.delete(0, tk.END)
        self.entry_ten.insert(0, v[2])
        self.gender_var.set(v[3])
        self.date_entry.set_date(v[4])
        self.cbb_chucvu.set(v[5])
        self.entry_email.delete(0, tk.END)
        self.entry_email.insert(0, v[6] if len(v) > 6 else "")
        self.entry_password.delete(0, tk.END)

    # ------------------------------------------------------------
    def save_employee(self):
        try:
            cur = self.db.get_cursor()
            password_update = ""
            if self.entry_password.get():
                password_update = ", password = ?"
                params = (self.entry_holot.get(), self.entry_ten.get(), self.gender_var.get(),
                          self.date_entry.get(), self.cbb_chucvu.get(), self.entry_email.get(),
                          self.entry_password.get(), self.entry_maso.get())
            else:
                params = (self.entry_holot.get(), self.entry_ten.get(), self.gender_var.get(),
                          self.date_entry.get(), self.cbb_chucvu.get(), self.entry_email.get(),
                          self.entry_maso.get())

            query = f"""UPDATE nhanvien 
                        SET holot = ?, ten = ?, phai = ?, ngaysinh = ?, chucvu = ?, email = ?{password_update}
                        WHERE maso = ?"""
            cur.execute(query, params)
            self.db.commit()
            self.load_data()
            self.clear_form()
            messagebox.showinfo("Thành công", "Cập nhật thông tin thành công")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật: {str(e)}")

    # ------------------------------------------------------------
    def clear_form(self):
        self.entry_maso.config(state="normal")
        self.entry_maso.delete(0, tk.END)
        self.entry_holot.delete(0, tk.END)
        self.entry_ten.delete(0, tk.END)
        self.gender_var.set("Nam")
        self.date_entry.set_date(datetime.now())
        self.cbb_chucvu.set("")
        self.entry_email.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

    def refresh_data(self):
        self.load_data()
        self.clear_form()

    def on_select(self, event):
        self.edit_employee()
