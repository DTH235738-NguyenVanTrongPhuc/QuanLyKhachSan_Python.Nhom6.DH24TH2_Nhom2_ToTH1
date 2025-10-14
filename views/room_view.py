import tkinter as tk
from tkinter import ttk, messagebox

class RoomView:
    def __init__(self, parent, db):
        self.db = db
        self.tab = ttk.Frame(parent)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        frame_info = tk.LabelFrame(self.tab, text="Thông tin phòng")
        frame_info.pack(padx=10, pady=10, fill="x")

        # Form fields
        tk.Label(frame_info, text="Mã phòng").grid(row=0, column=0, padx=5, pady=5)
        self.entry_maphong = tk.Entry(frame_info, width=10)
        self.entry_maphong.grid(row=0, column=1, padx=5)

        tk.Label(frame_info, text="Loại phòng").grid(row=0, column=2, padx=5)
        self.cbb_loaiphong = ttk.Combobox(frame_info, values=["Đơn", "Đôi", "VIP"], width=10)
        self.cbb_loaiphong.grid(row=0, column=3, padx=5)

        tk.Label(frame_info, text="Trạng thái").grid(row=0, column=4, padx=5)
        self.cbb_trangthai = ttk.Combobox(frame_info, values=["Trống", "Đang thuê", "Bảo trì"], width=12)
        self.cbb_trangthai.grid(row=0, column=5, padx=5)

        tk.Label(frame_info, text="Giá").grid(row=0, column=6, padx=5, pady=5)
        self.entry_gia = tk.Entry(frame_info, width=12)
        self.entry_gia.grid(row=0, column=7, padx=5)

        # Treeview
        columns = ("maphong", "loaiphong", "trangthai", "gia")
        self.tree = ttk.Treeview(self.tab, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col.upper())
        self.tree.pack(padx=10, pady=10, fill="both")

        # Style for treeview
        style = ttk.Style()
        style.configure("Treeview", background="#f0f0f0", foreground="black", 
                       rowheight=25, fieldbackground="#f0f0f0")
        style.map("Treeview", background=[("selected", "#6fa1f2")])

        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Buttons
        frame_btn = tk.Frame(self.tab)
        frame_btn.pack(pady=5)
        
        buttons = [
            ("Thêm", self.add_room, "#4CACAF"),
            ("Sửa", self.edit_room, "#4CACAF"),
            ("Lưu", self.save_room, "#4CAFAF"),
            ("Xóa", self.delete_room, "#4CACAF")
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            tk.Button(frame_btn, text=text, width=8, bg=color, fg="white",
                     command=command).grid(row=0, column=i, padx=5)

    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        cur = self.db.get_cursor()
        cur.execute("SELECT * FROM phong")
        for row in cur.fetchall():
            self.tree.insert("", tk.END, values=row)

    def add_room(self):
        if not self.entry_maphong.get():
            messagebox.showwarning("Cảnh báo", "Mã phòng không được để trống")
            return
        try:
            cur = self.db.get_cursor()
            cur.execute("INSERT INTO phong VALUES (%s, %s, %s, %s)",
                       (self.entry_maphong.get(), self.cbb_loaiphong.get(),
                        self.cbb_trangthai.get(), self.entry_gia.get()))
            self.db.commit()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def edit_room(self):
        sel = self.tree.selection()
        if not sel: return
        v = self.tree.item(sel)["values"]
        self.entry_maphong.delete(0, tk.END)
        self.entry_maphong.insert(0, v[0])
        self.cbb_loaiphong.set(v[1])
        self.cbb_trangthai.set(v[2])
        self.entry_gia.delete(0, tk.END)
        self.entry_gia.insert(0, v[3])

    def save_room(self):
        try:
            cur = self.db.get_cursor()
            cur.execute("UPDATE phong SET loaiphong=%s, trangthai=%s, gia=%s WHERE maphong=%s",
                       (self.cbb_loaiphong.get(), self.cbb_trangthai.get(),
                        self.entry_gia.get(), self.entry_maphong.get()))
            self.db.commit()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def delete_room(self):
        sel = self.tree.selection()
        if not sel: return
        maphong = self.tree.item(sel)["values"][0]
        try:
            cur = self.db.get_cursor()
            cur.execute("DELETE FROM phong WHERE maphong=%s", (maphong,))
            self.db.commit()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def on_select(self, event):
        self.edit_room()