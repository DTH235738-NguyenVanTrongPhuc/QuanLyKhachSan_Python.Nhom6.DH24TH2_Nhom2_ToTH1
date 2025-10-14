import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

class BookingView:
    def __init__(self, parent, db):
        self.db = db
        self.tab = ttk.Frame(parent)
        self.create_widgets()
        self.load_data()
        self.refresh_comboboxes()

    def create_widgets(self):
        frame_info = tk.LabelFrame(self.tab, text="Thông tin đặt phòng")
        frame_info.pack(padx=10, pady=10, fill="x")

        # Form fields
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

        # Treeview
        columns = ("madat", "makh", "maphong", "ngaydat", "ngaytra")
        self.tree = ttk.Treeview(self.tab, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col.upper())
        self.tree.pack(padx=10, pady=10, fill="both")

        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Buttons
        frame_btn = tk.Frame(self.tab)
        frame_btn.pack(pady=5)
        
        buttons = [
            ("Thêm", self.add_booking, "#4CAF50"),
            ("Sửa", self.edit_booking, "#4CAF50"),
            ("Lưu", self.save_booking, "#4CAF50"),
            ("Xóa", self.delete_booking, "#4CAF50")
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            tk.Button(frame_btn, text=text, width=8, bg=color, fg="white",
                     command=command).grid(row=0, column=i, padx=5)

    def refresh_comboboxes(self):
        # Refresh customer combobox
        cur = self.db.get_cursor()
        cur.execute("SELECT makh, hoten FROM khachhang")
        self.cbb_kh["values"] = [f"{row[0]} - {row[1]}" for row in cur.fetchall()]

        # Refresh room combobox
        cur.execute("SELECT maphong FROM phong WHERE trangthai='Trống'")
        self.cbb_phong["values"] = [row[0] for row in cur.fetchall()]

    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        cur = self.db.get_cursor()
        cur.execute("SELECT * FROM datphong")
        for row in cur.fetchall():
            self.tree.insert("", tk.END, values=row)

    def add_booking(self):
        try:
            cur = self.db.get_cursor()
            cur.execute("INSERT INTO datphong VALUES (%s, %s, %s, %s, %s)",
                       (self.entry_madat.get(),
                        self.cbb_kh.get().split(" - ")[0],
                        self.cbb_phong.get(),
                        self.date_dat.get(),
                        self.date_tra.get()))
            self.db.commit()

            # Update room status
            cur.execute("UPDATE phong SET trangthai='Đang thuê' WHERE maphong=%s", 
                       (self.cbb_phong.get(),))
            self.db.commit()

            self.load_data()
            self.refresh_comboboxes()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def edit_booking(self):
        sel = self.tree.selection()
        if not sel: return
        v = self.tree.item(sel)["values"]
        self.entry_madat.delete(0, tk.END)
        self.entry_madat.insert(0, v[0])
        self.cbb_kh.set(v[1])
        self.cbb_phong.set(v[2])
        self.date_dat.set_date(v[3])
        self.date_tra.set_date(v[4])

    def save_booking(self):
        try:
            cur = self.db.get_cursor()
            cur.execute("""UPDATE datphong SET makh=%s, maphong=%s, 
                          ngaydat=%s, ngaytra=%s WHERE madat=%s""",
                       (self.cbb_kh.get().split(" - ")[0],
                        self.cbb_phong.get(),
                        self.date_dat.get(),
                        self.date_tra.get(),
                        self.entry_madat.get()))
            self.db.commit()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def delete_booking(self):
        sel = self.tree.selection()
        if not sel: return
        madat, maphong = self.tree.item(sel)["values"][0], self.tree.item(sel)["values"][2]
        try:
            cur = self.db.get_cursor()
            cur.execute("DELETE FROM datphong WHERE madat=%s", (madat,))
            self.db.commit()

            # Reset room status
            cur.execute("UPDATE phong SET trangthai='Trống' WHERE maphong=%s", (maphong,))
            self.db.commit()

            self.load_data()
            self.refresh_comboboxes()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def on_select(self, event):
        self.edit_booking()