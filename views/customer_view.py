import tkinter as tk
from tkinter import ttk, messagebox

class CustomerView:
    def __init__(self, parent, db):
        # ! KHỞI TẠO VIEW KHÁCH HÀNG
        self.db = db
        self.tab = ttk.Frame(parent)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # ! TẠO CÁC WIDGET CHO GIAO DIỆN KHÁCH HÀNG
        frame_info = tk.LabelFrame(self.tab, text="Thông tin khách hàng")
        frame_info.pack(padx=10, pady=10, fill="x")

        # ! CÁC TRƯỜNG NHẬP LIỆU TRONG FORM
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

        # ! TREEVIEW VỚI CÁC CỘT ĐƯỢC NÂNG CẤP
        columns = ("makh", "hoten", "sdt", "cmnd")
        self.tree = ttk.Treeview(self.tab, columns=columns, show="headings", height=15)
        
        headings = {
            "makh": "MÃ KH",
            "hoten": "HỌ TÊN",
            "sdt": "SĐT",
            "cmnd": "CMND"
        }
        
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=120)
        
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        # ! GẮN SỰ KIỆN CHỌN
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # ! CÁC NÚT CHỨC NĂNG
        frame_btn = tk.Frame(self.tab)
        frame_btn.pack(pady=5)
        
        buttons = [
            ("Thêm", self.add_customer, "#4CAF50"),
            ("Sửa", self.edit_customer, "#2196F3"),
            ("Lưu", self.save_customer, "#FF9800"),
            ("Xóa", self.delete_customer, "#f44336"),
            ("Làm mới", self.refresh_data, "#607D8B")
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            tk.Button(frame_btn, text=text, width=8, bg=color, fg="white",
                     command=command).grid(row=0, column=i, padx=5)

    def load_data(self):
        # ! TẢI DỮ LIỆU KHÁCH HÀNG TỪ DATABASE
        for i in self.tree.get_children():
            self.tree.delete(i)
        cur = self.db.get_cursor()
        cur.execute("SELECT * FROM khachhang")
        for row in cur.fetchall():
            self.tree.insert("", tk.END, values=row)

    def add_customer(self):
        # ! THÊM KHÁCH HÀNG MỚI
        try:
            if not all([self.entry_makh.get(), self.entry_hoten.get()]):
                messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin")
                return
            
            cur = self.db.get_cursor()
            cur.execute("INSERT INTO khachhang VALUES (%s, %s, %s, %s)",
                       (self.entry_makh.get(), self.entry_hoten.get(), 
                        self.entry_sdt.get(), self.entry_cmnd.get()))
            self.db.commit()
            self.load_data()
            self.clear_form()
            messagebox.showinfo("Thành công", "Thêm khách hàng thành công")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm khách hàng: {str(e)}")

    def edit_customer(self):
        # ! CHỈNH SỬA KHÁCH HÀNG ĐÃ CHỌN
        sel = self.tree.selection()
        if not sel: 
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng cần sửa")
            return
        v = self.tree.item(sel)["values"]
        self.entry_makh.delete(0, tk.END)
        self.entry_makh.insert(0, v[0])
        self.entry_makh.config(state="disabled")
        self.entry_hoten.delete(0, tk.END)
        self.entry_hoten.insert(0, v[1])
        self.entry_sdt.delete(0, tk.END)
        self.entry_sdt.insert(0, v[2])
        self.entry_cmnd.delete(0, tk.END)
        self.entry_cmnd.insert(0, v[3])

    def save_customer(self):
        # ! LƯU THAY ĐỔI KHÁCH HÀNG
        try:
            cur = self.db.get_cursor()
            cur.execute("UPDATE khachhang SET hoten=%s, sdt=%s, cmnd=%s WHERE makh=%s",
                       (self.entry_hoten.get(), self.entry_sdt.get(), 
                        self.entry_cmnd.get(), self.entry_makh.get()))
            self.db.commit()
            self.load_data()
            self.clear_form()
            messagebox.showinfo("Thành công", "Cập nhật khách hàng thành công")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật khách hàng: {str(e)}")

    def delete_customer(self):
        # ! XÓA KHÁCH HÀNG
        sel = self.tree.selection()
        if not sel: 
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng cần xóa")
            return
        
        makh = self.tree.item(sel)["values"][0]
        
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa khách hàng {makh}?"):
            try:
                cur = self.db.get_cursor()
                cur.execute("DELETE FROM khachhang WHERE makh=%s", (makh,))
                self.db.commit()
                self.load_data()
                self.clear_form()
                messagebox.showinfo("Thành công", "Xóa khách hàng thành công")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa khách hàng: {str(e)}")

    def clear_form(self):
        # ! XÓA FORM NHẬP LIỆU
        self.entry_makh.delete(0, tk.END)
        self.entry_makh.config(state="normal")
        self.entry_hoten.delete(0, tk.END)
        self.entry_sdt.delete(0, tk.END)
        self.entry_cmnd.delete(0, tk.END)

    def refresh_data(self):
        # ! LÀM MỚI DỮ LIỆU
        self.load_data()
        self.clear_form()

    def on_select(self, event):
        # ! XỬ LÝ SỰ KIỆN CHỌN TRONG TREEVIEW
        self.edit_customer()