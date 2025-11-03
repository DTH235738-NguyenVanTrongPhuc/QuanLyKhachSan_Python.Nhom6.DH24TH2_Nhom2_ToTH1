# room_view.py - Fixed for SQL Server (pyodbc)
import tkinter as tk
from tkinter import ttk, messagebox

class RoomView:
    def __init__(self, parent, db, current_user_role=None):
        self.db = db
        self.current_user_role = current_user_role
        self.tab = ttk.Frame(parent)
        self.create_widgets()
        self.load_room_types()
        self.load_data()

    def create_widgets(self):
        frame_info = tk.LabelFrame(self.tab, text="Thông tin phòng")
        frame_info.pack(padx=10, pady=10, fill="x")

        # --- Form fields ---
        tk.Label(frame_info, text="Mã phòng").grid(row=0, column=0, padx=5, pady=5)
        self.entry_maphong = tk.Entry(frame_info, width=10)
        self.entry_maphong.grid(row=0, column=1, padx=5)

        tk.Label(frame_info, text="Loại phòng").grid(row=0, column=2, padx=5)
        self.cbb_loaiphong = ttk.Combobox(frame_info, width=15)
        self.cbb_loaiphong.grid(row=0, column=3, padx=5)

        tk.Label(frame_info, text="Trạng thái").grid(row=0, column=4, padx=5)
        self.cbb_trangthai = ttk.Combobox(
            frame_info,
            values=["Trống", "Đang thuê", "Bảo trì", "Đang dọn dẹp"],
            width=12
        )
        self.cbb_trangthai.grid(row=0, column=5, padx=5)

        tk.Label(frame_info, text="Ghi chú").grid(row=1, column=0, padx=5, pady=5)
        self.entry_ghichu = tk.Entry(frame_info, width=50)
        self.entry_ghichu.grid(row=1, column=1, columnspan=5, padx=5, sticky="we")

        # --- Treeview ---
        columns = ("maphong", "tenloai", "gia", "trangthai", "ghichu")
        self.tree = ttk.Treeview(self.tab, columns=columns, show="headings", height=10)

        headings = {
            "maphong": "MÃ PHÒNG",
            "tenloai": "LOẠI PHÒNG",
            "gia": "GIÁ",
            "trangthai": "TRẠNG THÁI",
            "ghichu": "GHI CHÚ"
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=120 if col != "gia" else 100)

        self.tree.pack(padx=10, pady=10, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # --- Buttons ---
        frame_btn = tk.Frame(self.tab)
        frame_btn.pack(pady=5)
        buttons = [
            ("Thêm", self.add_room, "#4CAF50"),
            ("Sửa", self.edit_room, "#2196F3"),
            ("Lưu", self.save_room, "#FF9800"),
            ("Xóa", self.delete_room, "#f44336")
        ]
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(frame_btn, text=text, width=8, bg=color, fg="white", command=command)
            btn.grid(row=0, column=i, padx=5)
            # Nếu không phải trưởng phòng → khóa thêm/sửa/xóa
            if self.current_user_role != "Trưởng phòng" and text in ["Thêm", "Sửa", "Xóa"]:
                btn.config(state="disabled")

    # --- Load dữ liệu loại phòng ---
    def load_room_types(self):
        cur = self.db.get_cursor()
        cur.execute("SELECT maloai, tenloai FROM loaiphong")
        room_types = cur.fetchall()
        self.cbb_loaiphong["values"] = [f"{row[0]} - {row[1]}" for row in room_types]

    # --- Load dữ liệu phòng ---
    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        cur = self.db.get_cursor()
        cur.execute("""
            SELECT p.maphong, l.tenloai, l.gia, p.trangthai, p.ghichu
            FROM phong p
            JOIN loaiphong l ON p.maloai = l.maloai
            ORDER BY p.maphong
        """)
        for row in cur.fetchall():
            formatted_row = list(row)
            formatted_row[2] = f"{row[2]:,} VND" if row[2] else "0 VND"
            self.tree.insert("", tk.END, values=formatted_row)

    # --- Thêm phòng ---
    def add_room(self):
        if not self.entry_maphong.get():
            messagebox.showwarning("Cảnh báo", "Mã phòng không được để trống")
            return
        if not self.cbb_loaiphong.get():
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn loại phòng")
            return
        try:
            cur = self.db.get_cursor()
            maloai = self.cbb_loaiphong.get().split(" - ")[0]
            cur.execute("""
                INSERT INTO phong (maphong, maloai, trangthai, ghichu)
                VALUES (?, ?, ?, ?)
            """, (
                self.entry_maphong.get(),
                maloai,
                self.cbb_trangthai.get() or "Trống",
                self.entry_ghichu.get()
            ))
            self.db.commit()
            self.load_data()
            self.clear_form()
            messagebox.showinfo("Thành công", "Thêm phòng thành công")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm phòng: {str(e)}")

    # --- Sửa phòng ---
    def edit_room(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phòng cần sửa")
            return
        v = self.tree.item(sel)["values"]
        self.entry_maphong.delete(0, tk.END)
        self.entry_maphong.insert(0, v[0])
        self.entry_maphong.config(state="disabled")
        self.cbb_loaiphong.set(v[1])
        self.cbb_trangthai.set(v[3])
        self.entry_ghichu.delete(0, tk.END)
        self.entry_ghichu.insert(0, v[4] if len(v) > 4 else "")

    # --- Lưu phòng ---
    def save_room(self):
        try:
            cur = self.db.get_cursor()
            maloai = self.cbb_loaiphong.get().split(" - ")[0]
            cur.execute("""
                UPDATE phong
                SET maloai=?, trangthai=?, ghichu=?
                WHERE maphong=?
            """, (
                maloai,
                self.cbb_trangthai.get(),
                self.entry_ghichu.get(),
                self.entry_maphong.get()
            ))
            self.db.commit()
            self.load_data()
            self.clear_form()
            messagebox.showinfo("Thành công", "Cập nhật phòng thành công")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật phòng: {str(e)}")

    # --- Xóa phòng ---
    def delete_room(self):
        sel = self.tree.selection()
        if not sel:
            return
        maphong = self.tree.item(sel)["values"][0]

        cur = self.db.get_cursor()
        cur.execute("SELECT COUNT(*) FROM datphong WHERE maphong=? AND trangthai=N'Active'", (maphong,))
        if cur.fetchone()[0] > 0:
            messagebox.showerror("Lỗi", "Không thể xóa phòng đang được đặt")
            return

        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa phòng {maphong}?"):
            try:
                cur.execute("DELETE FROM phong WHERE maphong=?", (maphong,))
                self.db.commit()
                self.load_data()
                self.clear_form()
                messagebox.showinfo("Thành công", "Xóa phòng thành công")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa phòng: {str(e)}")

    # --- Dọn form ---
    def clear_form(self):
        self.entry_maphong.delete(0, tk.END)
        self.entry_maphong.config(state="normal")
        self.cbb_loaiphong.set("")
        self.cbb_trangthai.set("Trống")
        self.entry_ghichu.delete(0, tk.END)

    # --- Khi chọn dòng ---
    def on_select(self, event):
        self.edit_room()
