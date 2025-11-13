import tkinter as tk
from tkinter import ttk, messagebox

class LoaiPhongView:
    def __init__(self, parent, db):
        self.db = db
        self.tab = ttk.Frame(parent)
        self.create_widgets()
        self.load_data()

    # ------------------------------------------------------------
    def create_widgets(self):
        # Form thông tin loại phòng
        frame_info = tk.LabelFrame(self.tab, text="Thông tin loại phòng")
        frame_info.pack(padx=10, pady=10, fill="x")

        tk.Label(frame_info, text="Mã loại").grid(row=0, column=0, padx=5, pady=5)
        self.entry_maloai = tk.Entry(frame_info, width=15)
        self.entry_maloai.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_info, text="Tên loại").grid(row=0, column=2, padx=5, pady=5)
        self.entry_tenloai = tk.Entry(frame_info, width=20)
        self.entry_tenloai.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_info, text="Giá (VNĐ)").grid(row=0, column=4, padx=5, pady=5)
        self.entry_gia = tk.Entry(frame_info, width=15)
        self.entry_gia.grid(row=0, column=5, padx=5, pady=5)

        # Treeview hiển thị danh sách loại phòng
        columns = ("maloai", "tenloai", "gia")
        self.tree = ttk.Treeview(self.tab, columns=columns, show="headings", height=15)
        headings = {"maloai": "MÃ LOẠI", "tenloai": "TÊN LOẠI", "gia": "GIÁ (VNĐ)"}
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Nút chức năng
        frame_btn = tk.Frame(self.tab)
        frame_btn.pack(pady=5)

        buttons = [
            ("Thêm", self.add_loai, "#4CAF50"),
            ("Sửa", self.edit_loai, "#2196F3"),
            ("Lưu", self.save_loai, "#FF9800"),
            ("Xóa", self.delete_loai, "#f44336"),
            ("Làm mới", self.refresh_data, "#607D8B")
        ]
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(frame_btn, text=text, width=8, bg=color, fg="white",
                            command=lambda c=command: c())
            btn.grid(row=0, column=i, padx=5)

    # ------------------------------------------------------------
    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            cur = self.db.get_cursor()
            cur.execute("SELECT maloai, tenloai, gia FROM loaiphong")
            for row in cur.fetchall():
                # ✨ Chuyển dữ liệu về dạng hiển thị sạch
                maloai = str(row[0]).strip().replace("'", "")
                tenloai = str(row[1]).strip().replace("'", "")
                # Nếu là Decimal hoặc dạng 'Decimal("...")' → lấy phần số
                gia = row[2]
                try:
                    gia = float(gia)
                except:
                    gia = float(str(gia).replace("Decimal(", "").replace("'", "").replace(")", ""))
                self.tree.insert("", tk.END, values=(maloai, tenloai, f"{gia:,.0f}"))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể load dữ liệu: {str(e)}")


    # ------------------------------------------------------------
    def add_loai(self):
        maloai = self.entry_maloai.get().strip()
        tenloai = self.entry_tenloai.get().strip()
        gia = self.entry_gia.get().strip()
        if not (maloai and tenloai and gia):
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin")
            return
        try:
            gia = float(gia)
            cur = self.db.get_cursor()
            cur.execute("INSERT INTO loaiphong (maloai, tenloai, gia) VALUES (?, ?, ?)", (maloai, tenloai, gia))
            self.db.commit()
            self.load_data()
            self.clear_form()
            messagebox.showinfo("Thành công", "Thêm loại phòng thành công")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm loại phòng: {str(e)}")

    # ------------------------------------------------------------
    def delete_loai(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn loại phòng cần xóa")
            return
        maloai = self.tree.item(sel)["values"][0]
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa loại phòng {maloai}?"):
            try:
                cur = self.db.get_cursor()
                cur.execute("DELETE FROM loaiphong WHERE maloai = ?", (maloai,))
                self.db.commit()
                self.load_data()
                self.clear_form()
                messagebox.showinfo("Thành công", "Xóa loại phòng thành công")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa loại phòng: {str(e)}")

    # ------------------------------------------------------------
    def edit_loai(self):
        sel = self.tree.selection()
        if not sel:
            return
        v = self.tree.item(sel)["values"]
        self.entry_maloai.delete(0, tk.END)
        self.entry_maloai.insert(0, v[0])
        self.entry_maloai.config(state="disabled")
        self.entry_tenloai.delete(0, tk.END)
        self.entry_tenloai.insert(0, v[1])
        self.entry_gia.delete(0, tk.END)
        self.entry_gia.insert(0, v[2])

    # ------------------------------------------------------------
    def save_loai(self):
        try:
            tenloai = self.entry_tenloai.get().strip()
            gia = float(self.entry_gia.get().strip())
            maloai = self.entry_maloai.get().strip()
            cur = self.db.get_cursor()
            cur.execute("UPDATE loaiphong SET tenloai=?, gia=? WHERE maloai=?", (tenloai, gia, maloai))
            self.db.commit()
            self.load_data()
            self.clear_form()
            messagebox.showinfo("Thành công", "Cập nhật loại phòng thành công")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật: {str(e)}")

    # ------------------------------------------------------------
    def clear_form(self):
        self.entry_maloai.config(state="normal")
        self.entry_maloai.delete(0, tk.END)
        self.entry_tenloai.delete(0, tk.END)
        self.entry_gia.delete(0, tk.END)

    # ------------------------------------------------------------
    def refresh_data(self):
        self.load_data()
        self.clear_form()

    # ------------------------------------------------------------
    def on_select(self, event):
        self.edit_loai()
