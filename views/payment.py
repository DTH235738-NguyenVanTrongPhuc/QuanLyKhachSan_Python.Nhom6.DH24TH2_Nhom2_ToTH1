import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ThanhToanView:
    def __init__(self, parent, db):
        self.db = db
        self.tab = ttk.Frame(parent)
        self.tab.pack(fill="both", expand=True)

        self.create_widgets()
        self.refresh_comboboxes()
        self.load_data()

    # =====================================================
    # GIAO DIỆN
    # =====================================================
    def create_widgets(self):
        frame_info = tk.LabelFrame(self.tab, text="Thông tin thanh toán")
        frame_info.pack(padx=10, pady=10, fill="x")

        # --- Mã thanh toán ---
        tk.Label(frame_info, text="Mã TT").grid(row=0, column=0, padx=5, pady=5)
        self.entry_matt = tk.Entry(frame_info, width=15)
        self.entry_matt.grid(row=0, column=1, padx=5, pady=5)

        # --- Mã đặt phòng ---
        tk.Label(frame_info, text="Mã đặt phòng").grid(row=0, column=2, padx=5, pady=5)
        self.cbb_madat = ttk.Combobox(frame_info, width=25, state="readonly")
        self.cbb_madat.grid(row=0, column=3, padx=5, pady=5)
        self.cbb_madat.bind("<<ComboboxSelected>>", self.on_booking_select)

        # --- Khách hàng ---
        tk.Label(frame_info, text="Khách hàng").grid(row=1, column=0, padx=5, pady=5)
        self.entry_kh = tk.Entry(frame_info, width=25, state="readonly")
        self.entry_kh.grid(row=1, column=1, padx=5, pady=5)

        # --- Loại phòng ---
        tk.Label(frame_info, text="Loại phòng").grid(row=1, column=2, padx=5, pady=5)
        self.entry_loaiphong = tk.Entry(frame_info, width=20, state="readonly")
        self.entry_loaiphong.grid(row=1, column=3, padx=5, pady=5)

        # --- Ngày đặt / Ngày trả ---
        tk.Label(frame_info, text="Ngày đặt").grid(row=2, column=0, padx=5, pady=5)
        self.entry_ngaydat = tk.Entry(frame_info, width=20, state="readonly")
        self.entry_ngaydat.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_info, text="Ngày trả").grid(row=2, column=2, padx=5, pady=5)
        self.entry_ngaytra = tk.Entry(frame_info, width=20, state="readonly")
        self.entry_ngaytra.grid(row=2, column=3, padx=5, pady=5)

        # --- Tổng tiền ---
        tk.Label(frame_info, text="Tổng tiền (VND)").grid(row=3, column=0, padx=5, pady=5)
        self.entry_tongtien = tk.Entry(frame_info, width=20, state="readonly")
        self.entry_tongtien.grid(row=3, column=1, padx=5, pady=5)

        # --- Ngày thanh toán ---
        tk.Label(frame_info, text="Ngày thanh toán").grid(row=3, column=2, padx=5, pady=5)
        self.entry_ngaytt = tk.Entry(frame_info, width=20, state="readonly")
        self.entry_ngaytt.grid(row=3, column=3, padx=5, pady=5)
        self.entry_ngaytt.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # --- Ghi chú ---
        tk.Label(frame_info, text="Ghi chú").grid(row=4, column=0, padx=5, pady=5)
        self.entry_ghichu = tk.Entry(frame_info, width=60)
        self.entry_ghichu.grid(row=4, column=1, columnspan=3, padx=5, pady=5, sticky="we")

        # =====================================================
        # TREEVIEW
        # =====================================================
        columns = ("mathanhtoan", "madat", "hoten", "loaiphong", "ngaydat", "ngaytra", "tongtien", "ngaythanhtoan", "ghichu")
        self.tree = ttk.Treeview(self.tab, columns=columns, show="headings", height=12)

        headings = {
            "mathanhtoan": "MÃ TT",
            "madat": "MÃ ĐẶT",
            "hoten": "KHÁCH HÀNG",
            "loaiphong": "LOẠI PHÒNG",
            "ngaydat": "NGÀY ĐẶT",
            "ngaytra": "NGÀY TRẢ",
            "tongtien": "TỔNG TIỀN",
            "ngaythanhtoan": "NGÀY TT",
            "ghichu": "GHI CHÚ"
        }

        for col, text in headings.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=110)

        self.tree.pack(padx=10, pady=10, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # =====================================================
        # BUTTONS
        # =====================================================
        frame_btn = tk.Frame(self.tab)
        frame_btn.pack(pady=5)
        buttons = [
            ("Thêm", self.add_payment, "#4CAF50"),
            ("Xóa", self.delete_payment, "#f44336"),
            ("Làm mới", self.refresh_data, "#607D8B")
        ]
        for i, (text, cmd, color) in enumerate(buttons):
            btn = tk.Button(frame_btn, text=text, bg=color, fg="white", width=10, command=cmd)
            btn.grid(row=0, column=i, padx=6)

    # =====================================================
    # LOAD COMBOBOXES
    # =====================================================
    def refresh_comboboxes(self):
        cur = self.db.get_cursor()
        cur.execute("""
            SELECT d.madat, k.hoten, l.tenloai
            FROM datphong d
            JOIN khachhang k ON d.makh = k.makh
            JOIN phong p ON d.maphong = p.maphong
            JOIN loaiphong l ON p.maloai = l.maloai
            WHERE d.trangthai = N'Active'
        """)
        self.bookings = {row[0]: {"hoten": row[1], "loaiphong": row[2]} for row in cur.fetchall()}
        self.cbb_madat["values"] = [f"{madat}" for madat in self.bookings]

    # =====================================================
    # LOAD DỮ LIỆU THANH TOÁN
    # =====================================================
    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        cur = self.db.get_cursor()
        cur.execute("""
            SELECT 
                t.mathanhtoan, 
                t.madat, 
                k.hoten, 
                l.tenloai, 
                d.ngaydat, 
                d.ngaytra, 
                t.tongtien, 
                t.ngaythanhtoan, 
                ISNULL(t.ghichu, N'') AS ghichu
            FROM thanhtoan t
            JOIN datphong d ON t.madat = d.madat
            JOIN khachhang k ON d.makh = k.makh
            JOIN phong p ON d.maphong = p.maphong
            JOIN loaiphong l ON p.maloai = l.maloai
            ORDER BY t.ngaythanhtoan DESC
        """)

        rows = cur.fetchall()
        for row in rows:
            # Làm sạch ký tự lạ hoặc dấu nháy đơn
            cleaned = tuple(str(v).strip("'") if isinstance(v, str) else v for v in row)
            self.tree.insert("", tk.END, values=cleaned)


    # =====================================================
    # CHỌN MÃ ĐẶT → TỰ ĐỔ DỮ LIỆU
    # =====================================================
    def on_booking_select(self, event):
        madat = self.cbb_madat.get()
        if not madat:
            return
        cur = self.db.get_cursor()
        cur.execute("""
            SELECT k.hoten, l.tenloai, d.ngaydat, d.ngaytra, l.gia
            FROM datphong d
            JOIN khachhang k ON d.makh = k.makh
            JOIN phong p ON d.maphong = p.maphong
            JOIN loaiphong l ON p.maloai = l.maloai
            WHERE d.madat = ?
        """, (madat,))
        row = cur.fetchone()
        if row:
            hoten, tenloai, ngaydat, ngaytra, gia = row
            self.entry_kh.config(state="normal")
            self.entry_loaiphong.config(state="normal")
            self.entry_ngaydat.config(state="normal")
            self.entry_ngaytra.config(state="normal")
            self.entry_tongtien.config(state="normal")

            self.entry_kh.delete(0, tk.END)
            self.entry_kh.insert(0, hoten)
            self.entry_loaiphong.delete(0, tk.END)
            self.entry_loaiphong.insert(0, tenloai)
            self.entry_ngaydat.delete(0, tk.END)
            self.entry_ngaydat.insert(0, ngaydat)
            self.entry_ngaytra.delete(0, tk.END)
            self.entry_ngaytra.insert(0, ngaytra)

            # Tính tổng tiền
            days = (ngaytra - ngaydat).days or 1
            tongtien = days * float(gia)
            self.entry_tongtien.delete(0, tk.END)
            self.entry_tongtien.insert(0, f"{tongtien:,.0f}")

            # Khóa lại
            self.entry_kh.config(state="readonly")
            self.entry_loaiphong.config(state="readonly")
            self.entry_ngaydat.config(state="readonly")
            self.entry_ngaytra.config(state="readonly")
            self.entry_tongtien.config(state="readonly")

    # =====================================================
    # THÊM THANH TOÁN
    # =====================================================
    def add_payment(self):
        if not self.entry_matt.get() or not self.cbb_madat.get():
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã TT và chọn mã đặt phòng.")
            return
        try:
            cur = self.db.get_cursor()
            cur.execute("""
                INSERT INTO thanhtoan (mathanhtoan, madat, tongtien, ngaythanhtoan, ghichu)
                VALUES (?, ?, ?, ?, ?)
            """, (
                self.entry_matt.get(),
                self.cbb_madat.get(),
                float(self.entry_tongtien.get().replace(",", "")),
                self.entry_ngaytt.get(),
                self.entry_ghichu.get()
            ))
            self.db.commit()
            self.load_data()
            self.clear_form()
            messagebox.showinfo("Thành công", "Thêm thanh toán thành công")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm: {e}")

    # =====================================================
    # XÓA THANH TOÁN
    # =====================================================
    def delete_payment(self):
        sel = self.tree.selection()
        if not sel:
            return
        matt = self.tree.item(sel)["values"][0]
        if messagebox.askyesno("Xác nhận", f"Xóa thanh toán {matt}?"):
            try:
                cur = self.db.get_cursor()
                cur.execute("DELETE FROM thanhtoan WHERE mathanhtoan=?", (matt,))
                self.db.commit()
                self.load_data()
                self.clear_form()
                messagebox.showinfo("Thành công", "Đã xóa")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    # =====================================================
    # CLEAR + REFRESH
    # =====================================================
    def clear_form(self):
        for e in [self.entry_matt, self.entry_kh, self.entry_loaiphong,
                  self.entry_ngaydat, self.entry_ngaytra,
                  self.entry_tongtien, self.entry_ghichu]:
            e.config(state="normal")
            e.delete(0, tk.END)
            if e in [self.entry_kh, self.entry_loaiphong,
                     self.entry_ngaydat, self.entry_ngaytra, self.entry_tongtien]:
                e.config(state="readonly")
        self.entry_ngaytt.config(state="normal")
        self.entry_ngaytt.delete(0, tk.END)
        self.entry_ngaytt.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_ngaytt.config(state="readonly")
        self.cbb_madat.set("")

    def refresh_data(self):
        self.load_data()
        self.refresh_comboboxes()
        self.clear_form()

    def on_select(self, event):
        pass
