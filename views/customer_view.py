import tkinter as tk
from tkinter import ttk, messagebox

class CustomerView:
    def __init__(self, parent, db):
        self.db = db
        self.tab = ttk.Frame(parent)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        frame_info = tk.LabelFrame(self.tab, text="Thông tin khách hàng")
        frame_info.pack(padx=10, pady=10, fill="x")

        # Form fields
        tk.Label(frame_info, text="Mã KH").grid(row=0, column=0, padx=5, pady=5)
        self.entry_makh = tk.Entry(frame_info, width=10)
        self.entry_makh.grid(row=0, column=1, padx=5)

        tk.Label(frame_info, text="Họ tên").grid(row=0, column=2, padx=5)
        self.entry_hoten = tk.Entry(frame_info, width=25)
        self.entry_hoten.grid(row=0, column=3, padx=5)

        tk.Label(frame_info, text="SĐT").grid(row=1, column=0, padx=5)
        self.entry_sdt = tk.Entry(frame_info, width=15)
        self.entry_sdt.grid(row=1, column=1, padx=5)

        tk.Label(frame_info, text="CMND").grid(row=1, column=2, padx=5)
        self.entry_cmnd = tk.Entry(frame_info, width=15)
        self.entry_cmnd.grid(row=1, column=3, padx=5)

        # Treeview
        self.tree = ttk.Treeview(self.tab, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col.upper())
        self.tree.pack(padx=10, pady=10, fill="both")

        # Buttons
        frame_btn = tk.Frame(self.tab)
        frame_btn.pack(pady=5)
        
        buttons = [
            ("Thêm", self.add_customer, "#4CAF50"),
            ("Sửa", self.edit_customer, "#4CAF50"),
            ("Lưu", self.save_customer, "#4CAF50"),
            ("Xóa", self.delete_customer, "#4CAF50")
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            tk.Button(frame_btn, text=text, width=8, bg=color, fg="white",
                     command=command).grid(row=0, column=i, padx=5)

    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        cur = self.db.get_cursor()
        cur.execute("SELECT * FROM khachhang")
        for row in cur.fetchall():
            self.tree.insert("", tk.END, values=row)

    def add_customer(self):
        try:
            cur = self.db.get_cursor()
            cur.execute("INSERT INTO khachhang VALUES (%s, %s, %s, %s)",
                       (self.entry_makh.get(), self.entry_hoten.get(), 
                        self.entry_sdt.get(), self.entry_cmnd.get()))
            self.db.commit()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def edit_customer(self):
        sel = self.tree.selection()
        if not sel: return
        v = self.tree.item(sel)["values"]
        self.entry_makh.delete(0, tk.END)
        self.entry_makh.insert(0, v[0])
        self.entry_hoten.delete(0, tk.END)
        self.entry_hoten.insert(0, v[1])
        self.entry_sdt.delete(0, tk.END)
        self.entry_sdt.insert(0, v[2])
        self.entry_cmnd.delete(0, tk.END)
        self.entry_cmnd.insert(0, v[3])

    def save_customer(self):
        cur = self.db.get_cursor()
        cur.execute("UPDATE khachhang SET hoten=%s, sdt=%s, cmnd=%s WHERE makh=%s",
                   (self.entry_hoten.get(), self.entry_sdt.get(), 
                    self.entry_cmnd.get(), self.entry_makh.get()))
        self.db.commit()
        self.load_data()

    def delete_customer(self):
        sel = self.tree.selection()
        if not sel: return
        makh = self.tree.item(sel)["values"][0]
        cur = self.db.get_cursor()
        cur.execute("DELETE FROM khachhang WHERE makh=%s", (makh,))
        self.db.commit()
        self.load_data()