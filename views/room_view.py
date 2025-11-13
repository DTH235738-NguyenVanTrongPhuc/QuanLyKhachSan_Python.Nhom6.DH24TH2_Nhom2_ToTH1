import tkinter as tk
from tkinter import ttk, messagebox

class RoomView:
    def __init__(self, parent, db, current_user_role=None):
        self.db = db
        self.current_user_role = current_user_role
        self.tab = ttk.Frame(parent)
        self.tab.pack(fill="both", expand=True)

        self.room_type_data = {}  # {maloai: (tenloai, gia)}

        self.create_widgets()
        self.load_room_types()
        self.load_data()

    # =======================================================
    # TẠO GIAO DIỆN
    # =======================================================
    def create_widgets(self):
        frame_info = tk.LabelFrame(self.tab, text="Thông tin phòng")
        frame_info.pack(padx=10, pady=10, fill="x")

        # --- Mã phòng ---
        tk.Label(frame_info, text="Mã phòng").grid(row=0, column=0, padx=5, pady=5)
        self.entry_maphong = tk.Entry(frame_info, width=10)
        self.entry_maphong.grid(row=0, column=1, padx=5)

        # --- Loại phòng ---
        tk.Label(frame_info, text="Loại phòng").grid(row=0, column=2, padx=5)
        self.cbb_loaiphong = ttk.Combobox(frame_info, width=20, state="readonly")
        self.cbb_loaiphong.grid(row=0, column=3, padx=5)
        self.cbb_loaiphong.bind("<<ComboboxSelected>>", self.on_loai_change)

        # --- Giá phòng ---
        tk.Label(frame_info, text="Giá phòng").grid(row=0, column=4, padx=5)
        self.entry_gia = tk.Entry(frame_info, width=15, state="readonly")
        self.entry_gia.grid(row=0, column=5, padx=5)

        # --- Trạng thái ---
        tk.Label(frame_info, text="Trạng thái").grid(row=1, column=0, padx=5, pady=5)
        self.cbb_trangthai = ttk.Combobox(
            frame_info,
            values=["Trống", "Đang thuê", "Bảo trì", "Đang dọn dẹp"],
            width=15
        )
        self.cbb_trangthai.grid(row=1, column=1, padx=5)
        self.cbb_trangthai.set("Trống")

        # --- Ghi chú ---
        tk.Label(frame_info, text="Ghi chú").grid(row=1, column=2, padx=5)
        self.entry_ghichu = tk.Entry(frame_info, width=40)
        self.entry_ghichu.grid(row=1, column=3, columnspan=3, padx=5, sticky="we")

        # --- Treeview ---
        columns = ("maphong", "maloai", "tenloai", "gia", "trangthai", "ghichu")
        self.tree = ttk.Treeview(self.tab, columns=columns, show="headings", height=12)

        self.tree.heading("maphong", text="MÃ PHÒNG")
        self.tree.heading("maloai", text="MÃ LOẠI")
        self.tree.heading("tenloai", text="LOẠI PHÒNG")
        self.tree.heading("gia", text="GIÁ")
        self.tree.heading("trangthai", text="TRẠNG THÁI")
        self.tree.heading("ghichu", text="GHI CHÚ")

        self.tree.column("maphong", width=120)
        self.tree.column("maloai", width=0, stretch=False)  # ẨN MÃ LOẠI
        self.tree.column("tenloai", width=180)
        self.tree.column("gia", width=120)
        self.tree.column("trangthai", width=120)
        self.tree.column("ghichu", width=200)

        self.tree.pack(padx=10, pady=10, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # --- Buttons ---
        frame_btn = tk.Frame(self.tab)
        frame_btn.pack(pady=5)
        buttons = [
            ("Thêm", self.add_room, "#4CAF50"),
            ("Sửa", self.edit_room, "#2196F3"),
            ("Lưu", self.save_room, "#FF9800"),
            ("Xóa", self.delete_room, "#f44336"),
            ("Làm mới", self.refresh_data, "#607D8B")
            
        ]
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(frame_btn, text=text, width=8, bg=color, fg="white", command=command)
            btn.grid(row=0, column=i, padx=6)
            if self.current_user_role != "Trưởng phòng" and text in ["Thêm", "Sửa", "Xóa"]:
                btn.config(state="disabled")

    # =======================================================
    # LOAD LOẠI PHÒNG + GIÁ
    # =======================================================
    def refresh_comboboxes(self):
        
        self.room_type_data.clear()
        cur = self.db.get_cursor()
        cur.execute("""
            SELECT maloai, tenloai, gia
            FROM loaiphong
            ORDER BY tenloai
        """)
        rows = cur.fetchall()
        display_values = []
        for maloai, tenloai, gia in rows:
            self.room_type_data[maloai] = (tenloai, gia)
            display_values.append(f"{maloai} - {tenloai}")
        self.cbb_loaiphong["values"] = display_values

    def load_room_types(self):
        cur = self.db.get_cursor()
        cur.execute("SELECT maloai, tenloai, gia FROM loaiphong ORDER BY maloai")
        rows = cur.fetchall()
        list_display = []
        for maloai, tenloai, gia in rows:
            self.room_type_data[maloai] = (tenloai, gia)
            list_display.append(f"{maloai} - {tenloai}")
        self.cbb_loaiphong["values"] = list_display

    # =======================================================
    # LOAD PHÒNG
    # =======================================================
    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        cur = self.db.get_cursor()
        cur.execute("""
            SELECT p.maphong, p.maloai, l.tenloai, l.gia, p.trangthai, p.ghichu
            FROM phong p
            JOIN loaiphong l ON p.maloai = l.maloai
            ORDER BY p.maphong
        """)
        for row in cur.fetchall():
            maphong, maloai, tenloai, gia, trangthai, ghichu = row
            gia_text = f"{gia:,.0f} VND"
            self.tree.insert("", tk.END, values=(maphong, maloai, tenloai, gia_text, trangthai, ghichu))

    # =======================================================
    # THÊM PHÒNG
    # =======================================================
    def add_room(self):
        if not self.entry_maphong.get() or not self.cbb_loaiphong.get():
            messagebox.showwarning("Cảnh báo", "Điền đầy đủ thông tin")
            return
        maloai = self.cbb_loaiphong.get().split(" - ")[0]
        try:
            cur = self.db.get_cursor()
            cur.execute("""
                INSERT INTO phong (maphong, maloai, trangthai, ghichu)
                VALUES (?, ?, ?, ?)
            """, (self.entry_maphong.get(), maloai, self.cbb_trangthai.get(), self.entry_ghichu.get()))
            self.db.commit()
            self.load_data()
            self.refresh_comboboxes()
            self.clear_form()
            messagebox.showinfo("Thành công", "Thêm phòng thành công")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # =======================================================
    # SỬA PHÒNG → ĐỔ DỮ LIỆU LÊN FORM
    # =======================================================
    def edit_room(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phòng cần sửa")
            return
        v = self.tree.item(sel)["values"]
        maphong, maloai, tenloai, gia, trangthai, ghichu = v
        self.entry_maphong.config(state="normal")
        self.entry_maphong.delete(0, tk.END)
        self.entry_maphong.insert(0, maphong)
        self.entry_maphong.config(state="disabled")
        self.cbb_loaiphong.set(f"{maloai} - {tenloai}")
        self.entry_gia.config(state="normal")
        self.entry_gia.delete(0, tk.END)
        self.entry_gia.insert(0, gia)
        self.entry_gia.config(state="readonly")
        self.cbb_trangthai.set(trangthai)
        self.entry_ghichu.delete(0, tk.END)
        self.entry_ghichu.insert(0, ghichu)

    # =======================================================
    # LƯU PHÒNG (UPDATE)
    # =======================================================
    def save_room(self):
        maloai = self.cbb_loaiphong.get().split(" - ")[0]
        try:
            cur = self.db.get_cursor()
            cur.execute("""
                UPDATE phong
                SET maloai=?, trangthai=?, ghichu=?
                WHERE maphong=?
            """, (maloai, self.cbb_trangthai.get(), self.entry_ghichu.get(), self.entry_maphong.get()))
            self.db.commit()
            self.load_data()
            self.refresh_comboboxes()
            self.clear_form()
            messagebox.showinfo("Thành công", "Cập nhật phòng thành công")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # =======================================================
    # XÓA PHÒNG
    # =======================================================
    def delete_room(self):
        sel = self.tree.selection()
        if not sel:
            return
        maphong = self.tree.item(sel)["values"][0]
        cur = self.db.get_cursor()
        cur.execute("SELECT COUNT(*) FROM datphong WHERE maphong=? AND trangthai IN (N'Active', N'Đang thuê')", (maphong,))
        if cur.fetchone()[0] > 0:
            messagebox.showerror("Lỗi", "Không thể xóa phòng đang được đặt hoặc thuê")
            return
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa phòng {maphong}?"):
            try:
                cur.execute("DELETE FROM phong WHERE maphong=?", (maphong,))
                self.db.commit()
                self.load_data()
                self.clear_form()
                messagebox.showinfo("Thành công", "Xóa phòng thành công")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    # =======================================================
    # CLEAR FORM
    # =======================================================
    def clear_form(self):
        self.entry_maphong.config(state="normal")
        self.entry_maphong.delete(0, tk.END)
        self.cbb_loaiphong.set("")
        self.entry_gia.config(state="normal")
        self.entry_gia.delete(0, tk.END)
        self.entry_gia.config(state="readonly")
        self.cbb_trangthai.set("Trống")
        self.entry_ghichu.delete(0, tk.END)


   

    # =======================================================
    # THAY ĐỔI LOẠI → TỰ ĐỘNG CẬP NHẬT GIÁ
    # =======================================================
    def on_loai_change(self, event):
        try:
            maloai = self.cbb_loaiphong.get().split(" - ")[0]
            tenloai, gia = self.room_type_data.get(maloai, ("", 0))
            self.entry_gia.config(state="normal")
            self.entry_gia.delete(0, tk.END)
            self.entry_gia.insert(0, f"{gia:,.0f} VND")
            self.entry_gia.config(state="readonly")
        except:
            self.entry_gia.config(state="normal")
            self.entry_gia.delete(0, tk.END)
            self.entry_gia.config(state="readonly")

    # =======================================================
    # CHỌN DÒNG TRONG TREEVIEW
    # =======================================================
    def refresh_data(self):
        self.load_data()
        self.refresh_comboboxes()
        self.clear_form()
    def on_select(self, event):
        self.edit_room()
