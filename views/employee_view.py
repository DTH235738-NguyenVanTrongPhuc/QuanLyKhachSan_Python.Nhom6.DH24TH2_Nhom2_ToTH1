import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

class EmployeeView:
    def __init__(self, parent, db):
        self.db = db
        self.tab = ttk.Frame(parent)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Information frame
        frame_info = tk.LabelFrame(self.tab, text="Thông tin nhân viên")
        frame_info.pack(padx=10, pady=10, fill="x")

        # Form fields
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
        tk.Label(frame_info, text="Giới tính").grid(row=1, column=0, padx=0, pady=3, sticky="w")
        tk.Radiobutton(frame_info, text="Nam", variable=self.gender_var, value="Nam").grid(row=1, column=1, padx=5, sticky="w")
        tk.Radiobutton(frame_info, text="Nữ", variable=self.gender_var, value="Nữ").grid(row=1, column=2, padx=5, sticky="w")

        tk.Label(frame_info, text="Ngày sinh").grid(row=1, column=3, padx=5, pady=5)
        self.date_entry = DateEntry(frame_info, width=12, background="darkblue", 
                                  foreground="white", date_pattern="yyyy-mm-dd")
        self.date_entry.grid(row=1, column=4, padx=5, pady=5)

        tk.Label(frame_info, text="Chức vụ").grid(row=1, column=5, padx=5, pady=5)
        self.cbb_chucvu = ttk.Combobox(frame_info, values=["Trưởng phòng", "Phó phòng", 
                                                         "Nhân viên", "Lễ tân", "Bảo vệ"], width=18)
        self.cbb_chucvu.grid(row=1, column=6, padx=5, pady=5)

        # Treeview
        columns = ("maso", "holot", "ten", "phai", "ngaysinh", "chucvu")
        self.tree = ttk.Treeview(self.tab, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(padx=10, pady=10, fill="both")

        # Buttons
        frame_btn = tk.Frame(self.tab)
        frame_btn.pack(pady=5)
        
        buttons = [
            ("Thêm", self.add_employee, "#4CAF50"),
            ("Sửa", self.edit_employee, "#4CAF50"),
            ("Lưu", self.save_employee, "#4CAF50"),
            ("Xóa", self.delete_employee, "#4CAF50")
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            tk.Button(frame_btn, text=text, width=8, bg=color, fg="white",
                     command=command).grid(row=0, column=i, padx=5)

    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        cur = self.db.get_cursor()
        cur.execute("SELECT * FROM nhanvien")
        for row in cur.fetchall():
            self.tree.insert("", tk.END, values=row)

    def add_employee(self):
        try:
            cur = self.db.get_cursor()
            cur.execute("INSERT INTO nhanvien VALUES (%s, %s, %s, %s, %s, %s)", (
                self.entry_maso.get(), self.entry_holot.get(), self.entry_ten.get(),
                self.gender_var.get(), self.date_entry.get(), self.cbb_chucvu.get()
            ))
            self.db.commit()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def delete_employee(self):
        sel = self.tree.selection()
        if not sel: return
        maso = self.tree.item(sel)["values"][0]
        cur = self.db.get_cursor()
        cur.execute("DELETE FROM nhanvien WHERE maso=%s", (maso,))
        self.db.commit()
        self.load_data()

    def edit_employee(self):
        sel = self.tree.selection()
        if not sel: return
        v = self.tree.item(sel)["values"]
        self.entry_maso.delete(0, tk.END)
        self.entry_maso.insert(0, v[0])
        self.entry_holot.delete(0, tk.END)
        self.entry_holot.insert(0, v[1])
        self.entry_ten.delete(0, tk.END)
        self.entry_ten.insert(0, v[2])
        self.gender_var.set(v[3])
        self.date_entry.set_date(v[4])
        self.cbb_chucvu.set(v[5])

    def save_employee(self):
        cur = self.db.get_cursor()
        cur.execute("""UPDATE nhanvien SET holot=%s, ten=%s, phai=%s, 
                      ngaysinh=%s, chucvu=%s WHERE maso=%s""",
                   (self.entry_holot.get(), self.entry_ten.get(), self.gender_var.get(),
                    self.date_entry.get(), self.cbb_chucvu.get(), self.entry_maso.get()))
        self.db.commit()
        self.load_data()