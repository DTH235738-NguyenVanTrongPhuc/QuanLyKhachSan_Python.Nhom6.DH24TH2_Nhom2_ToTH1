# booking_view.py - Fixed version for SQL Server (pyodbc)
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

class BookingView:
    def __init__(self, parent, db, current_user_id=None, current_user_role=None):
        self.db = db
        self.current_user_id = current_user_id
        self.current_user_role = current_user_role
        self.tab = ttk.Frame(parent)
        self.create_widgets()
        self.load_data()
        self.refresh_comboboxes()
    # -------- Create Widgets ---------
    def create_widgets(self):
        frame_info = tk.LabelFrame(self.tab, text="Thông tin đặt phòng")
        frame_info.pack(padx=10, pady=10, fill="x")

        tk.Label(frame_info, text="Mã đặt").grid(row=0, column=0, padx=5, pady=5)
        self.entry_madat = tk.Entry(frame_info, width=10)
        self.entry_madat.grid(row=0, column=1, padx=5)

        tk.Label(frame_info, text="Khách hàng").grid(row=0, column=2, padx=5)
        self.cbb_kh = ttk.Combobox(frame_info, width=25)
        self.cbb_kh.grid(row=0, column=3, padx=5)

        tk.Label(frame_info, text="Phòng").grid(row=0, column=4, padx=5)
        self.cbb_phong = ttk.Combobox(frame_info, width=15)
        self.cbb_phong.grid(row=0, column=5, padx=5)

        tk.Label(frame_info, text="Ngày đặt").grid(row=1, column=0, padx=5)
        self.date_dat = DateEntry(frame_info, width=12, date_pattern="yyyy-mm-dd")
        self.date_dat.grid(row=1, column=1, padx=5)

        tk.Label(frame_info, text="Ngày trả").grid(row=1, column=2, padx=5)
        self.date_tra = DateEntry(frame_info, width=12, date_pattern="yyyy-mm-dd")
        self.date_tra.grid(row=1, column=3, padx=5)

        tk.Label(frame_info, text="Nhân viên tạo").grid(row=1, column=4, padx=5)
        self.lbl_nhanvien = tk.Label(frame_info, text=self.current_user_id,
                                     bg="#f0f0f0", relief="sunken", width=15)
        self.lbl_nhanvien.grid(row=1, column=5, padx=5)

        columns = ("madat", "makh", "hoten", "maphong", "manv", "ngaydat", "ngaytra")
        self.tree = ttk.Treeview(self.tab, columns=columns, show="headings", height=10)

        headings = {
            "madat": "MÃ ĐẶT",
            "makh": "MÃ KH",
            "hoten": "TÊN KH",
            "maphong": "PHÒNG",
            "manv": "NV TẠO",
            "ngaydat": "NGÀY ĐẶT",
            "ngaytra": "NGÀY TRẢ"
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
# ! Frame chứa các nút chức năng
        frame_btn = tk.Frame(self.tab)
        frame_btn.pack(pady=5)
        buttons = [
            ("Thêm", self.add_booking, "#4CAF50"),
            ("Sửa", self.edit_booking, "#2196F3"),
            ("Lưu", self.save_booking, "#FF9800"),
            ("Xóa", self.delete_booking, "#f44336"),
            ("Làm mới", self.refresh_data, "#607D8B")
        ]
        for i, (text, command, color) in enumerate(buttons):
            tk.Button(frame_btn, text=text, width=8, bg=color, fg="white",
                      command=command).grid(row=0, column=i, padx=5)

    def refresh_comboboxes(self):
          # ! Load dữ liệu cho combobox khách hàng và phòng trống
        cur = self.db.get_cursor()
        cur.execute("SELECT makh, hoten FROM khachhang ORDER BY hoten")
        self.cbb_kh["values"] = [f"{row[0]} - {row[1]}" for row in cur.fetchall()]

        cur.execute("""
            SELECT p.maphong, l.tenloai, l.gia
            FROM phong p
            JOIN loaiphong l ON p.maloai = l.maloai
            WHERE p.trangthai = N'Trống'
            ORDER BY p.maphong
        """)
        rooms = cur.fetchall()
        self.cbb_phong["values"] = [f"{row[0]} - {row[1]} ({row[2]:,} VND)" for row in rooms]

    def load_data(self):
         # ! Load danh sách đặt phòng vào Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)
        cur = self.db.get_cursor()
        cur.execute("""
            SELECT d.madat, d.makh, k.hoten, d.maphong, d.manv, d.ngaydat, d.ngaytra
            FROM datphong d
            JOIN khachhang k ON d.makh = k.makh
            WHERE d.trangthai = N'Active'
            ORDER BY d.ngaydat DESC
        """)

        for row in cur.fetchall():
            # Làm sạch chuỗi chứa nháy
            cleaned = []
            for item in row:
                if isinstance(item, str):
                    cleaned.append(item.strip("'").strip('"').strip())
                else:
                    cleaned.append(item)
            self.tree.insert("", tk.END, values=cleaned)


    def add_booking(self):
        try:
                # ! Kiểm tra dữ liệu đầu vào 
            if not all([self.entry_madat.get(), self.cbb_kh.get(), self.cbb_phong.get()]):
                messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin")
                return

            cur = self.db.get_cursor()
            cur.execute("SELECT COUNT(*) FROM datphong WHERE madat = ?", (self.entry_madat.get(),))
            if cur.fetchone()[0] > 0:
                messagebox.showerror("Lỗi", "Mã đặt phòng đã tồn tại")
                return

            madat = self.entry_madat.get()
            makh = self.cbb_kh.get().split(" - ")[0]
            maphong = self.cbb_phong.get().split(" - ")[0]
            ngaydat = self.date_dat.get()
            ngaytra = self.date_tra.get()

            cur.execute("""
                INSERT INTO datphong (madat, makh, maphong, manv, ngaydat, ngaytra, trangthai)
                VALUES (?, ?, ?, ?, ?, ?, N'Active')
            """, (madat, makh, maphong, self.current_user_id, ngaydat, ngaytra))

            cur.execute("UPDATE phong SET trangthai = N'Đang thuê' WHERE maphong = ?", (maphong,))
            self.db.commit()
            self.load_data()
            self.refresh_comboboxes()
            self.clear_form()
            messagebox.showinfo("Thành công", "Đặt phòng thành công")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đặt phòng: {str(e)}")

    def edit_booking(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn đặt phòng cần sửa")
            return
        v = self.tree.item(sel)["values"]
        self.entry_madat.delete(0, tk.END)
        self.entry_madat.insert(0, v[0])
        self.entry_madat.config(state="disabled")
        self.cbb_kh.set(f"{v[1]} - {v[2]}")
        self.cbb_phong.set(v[3])
        self.date_dat.set_date(v[5])
        self.date_tra.set_date(v[6])

    def save_booking(self):
        try:
            cur = self.db.get_cursor()
            cur.execute("SELECT maphong FROM datphong WHERE madat = ?", (self.entry_madat.get(),))
            old_room = cur.fetchone()[0]

            makh = self.cbb_kh.get().split(" - ")[0]
            new_room = self.cbb_phong.get().split(" - ")[0]
            ngaydat = self.date_dat.get()
            ngaytra = self.date_tra.get()

            cur.execute("""
                UPDATE datphong SET makh=?, maphong=?, ngaydat=?, ngaytra=?
                WHERE madat=?
            """, (makh, new_room, ngaydat, ngaytra, self.entry_madat.get()))

            if old_room != new_room:
                cur.execute("UPDATE phong SET trangthai = N'Trống' WHERE maphong = ?", (old_room,))
                cur.execute("UPDATE phong SET trangthai = N'Đang thuê' WHERE maphong = ?", (new_room,))

            self.db.commit()
            self.load_data()
            self.refresh_comboboxes()
            self.clear_form()
            messagebox.showinfo("Thành công", "Cập nhật đặt phòng thành công")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật đặt phòng: {str(e)}")

    def delete_booking(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn đặt phòng cần xóa")
            return

        v = self.tree.item(sel)["values"]
        madat = str(v[0]).strip()
        maphong = str(v[3]).strip()

        if not madat:
            messagebox.showerror("Lỗi", "Mã đặt phòng bị rỗng! Không thể xóa.")
            return

        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa đặt phòng {madat}?"):
            try:
                cur = self.db.get_cursor()

                # 1. Cập nhật trạng thái phòng về Trống
                cur.execute("UPDATE phong SET trangthai = N'Trống' WHERE maphong = ?", (maphong,))

                # 2. XÓA DỮ LIỆU ĐẶT PHÒNG THẬT SỰ TRONG SQL
                cur.execute("DELETE FROM datphong WHERE madat = ?", (madat,))

                # 3. Lưu thay đổi
                self.db.commit()

                messagebox.showinfo("Thành công", "Xóa đặt phòng thành công")

                # Refresh giao diện
                self.load_data()
                self.refresh_comboboxes()
                self.clear_form()

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa đặt phòng: {str(e)}")




    def clear_form(self):
        self.entry_madat.delete(0, tk.END)
        self.entry_madat.config(state="normal")
        self.cbb_kh.set("")
        self.cbb_phong.set("")
        self.date_dat.set_date(datetime.now())
        self.date_tra.set_date(datetime.now())
 # ! Làm mới dữ liệu Treeview và combobox
    def refresh_data(self):
        self.load_data()
        self.refresh_comboboxes()
        self.clear_form()

    def on_select(self, event):
        # ! Khi chọn hàng trong Treeview, hiển thị lên form để sửa
        self.edit_booking()
