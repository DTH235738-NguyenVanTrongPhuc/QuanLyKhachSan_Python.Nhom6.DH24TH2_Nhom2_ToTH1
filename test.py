import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3

# ====== Hàm canh giữa cửa sổ ======
def center_window(win, w=950, h=650):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")

# ====== Kết nối và tạo CSDL ======
def connect_db():
    conn = sqlite3.connect("khachsan.db")
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS nhanvien (
                    maso TEXT PRIMARY KEY,
                    holot TEXT,
                    ten TEXT,
                    phai TEXT,
                    ngaysinh TEXT,
                    chucvu TEXT
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS khachhang (
                    makh TEXT PRIMARY KEY,
                    hoten TEXT,
                    sdt TEXT,
                    cmnd TEXT
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS phong (
                    maphong TEXT PRIMARY KEY,
                    loaiphong TEXT,
                    trangthai TEXT
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS datphong (
                    madat TEXT PRIMARY KEY,
                    makh TEXT,
                    maphong TEXT,
                    ngaydat TEXT,
                    ngaytra TEXT
                )''')
    conn.commit()
    return conn

# ====== Cửa sổ chính ======
root = tk.Tk()
root.title("QUẢN LÝ KHÁCH SẠN")
center_window(root)
root.resizable(False, False)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

conn = connect_db()

# ====== HÀM DÙNG CHUNG ======
def refresh_combobox_khachhang(cbb):
    cur = conn.cursor()
    cur.execute("SELECT makh, hoten FROM khachhang")
    cbb["values"] = [f"{row[0]} - {row[1]}" for row in cur.fetchall()]

def refresh_combobox_phong(cbb):
    cur = conn.cursor()
    cur.execute("SELECT maphong FROM phong WHERE trangthai='Trống'")
    cbb["values"] = [row[0] for row in cur.fetchall()]

# -----------------------------------------------------------------
# TAB 1: NHÂN VIÊN
# -----------------------------------------------------------------
tab_nv = ttk.Frame(notebook)
notebook.add(tab_nv, text="Nhân viên")

frame_info = tk.LabelFrame(tab_nv, text="Thông tin nhân viên")
frame_info.pack(padx=10, pady=10, fill="x")

tk.Label(frame_info, text="Mã số").grid(row=0, column=0, padx=5, pady=5)
entry_maso = tk.Entry(frame_info, width=10)
entry_maso.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_info, text="Họ lót").grid(row=0, column=2, padx=5, pady=5)
entry_holot = tk.Entry(frame_info, width=20)
entry_holot.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame_info, text="Tên").grid(row=0, column=4, padx=5, pady=5)
entry_ten = tk.Entry(frame_info, width=15)
entry_ten.grid(row=0, column=5, padx=5, pady=5)

gender_var = tk.StringVar(value="Nam")  # mặc định Nam

# Nhãn
tk.Label(frame_info, text="Giới tính").grid(row=1, column=0, padx=0, pady=3, sticky="w")

# Radiobutton Nam / Nữ
tk.Radiobutton(frame_info, text="Nam", variable=gender_var, value="Nam").grid(row=1, column=1, padx=5, sticky="w")
tk.Radiobutton(frame_info, text="Nữ", variable=gender_var, value="Nữ").grid(row=1, column=2, padx=5, sticky="w")

tk.Label(frame_info, text="Ngày sinh").grid(row=1, column=3, padx=5, pady=5)
date_entry = DateEntry(frame_info, width=12, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
date_entry.grid(row=1, column=4, padx=5, pady=5)

tk.Label(frame_info, text="Chức vụ").grid(row=1, column=5, padx=5, pady=5)
cbb_chucvu = ttk.Combobox(frame_info, values=["Trưởng phòng", "Phó phòng", "Nhân viên", "Lễ tân", "Bảo vệ"], width=18)
cbb_chucvu.grid(row=1, column=6, padx=5, pady=5)

columns_nv = ("maso", "holot", "ten", "phai", "ngaysinh", "chucvu")
tree_nv = ttk.Treeview(tab_nv, columns=columns_nv, show="headings", height=10)
for col in columns_nv:
    tree_nv.heading(col, text=col.capitalize())
tree_nv.pack(padx=10, pady=10, fill="both")

def load_nv():
    for i in tree_nv.get_children():
        tree_nv.delete(i)
    cur = conn.cursor()
    cur.execute("SELECT * FROM nhanvien")
    for row in cur.fetchall():
        tree_nv.insert("", tk.END, values=row)

def them_nv():
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO nhanvien VALUES (?, ?, ?, ?, ?, ?)", (
            entry_maso.get(), entry_holot.get(), entry_ten.get(),
            gender_var.get(), date_entry.get(), cbb_chucvu.get()
        ))
        conn.commit()
        load_nv()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def xoa_nv():
    sel = tree_nv.selection()
    if not sel: return
    maso = tree_nv.item(sel)["values"][0]
    conn.execute("DELETE FROM nhanvien WHERE maso=?", (maso,))
    conn.commit()
    load_nv()

def sua_nv():
    sel = tree_nv.selection()
    if not sel: return
    v = tree_nv.item(sel)["values"]
    entry_maso.delete(0, tk.END)
    entry_maso.insert(0, v[0])
    entry_holot.delete(0, tk.END)
    entry_holot.insert(0, v[1])
    entry_ten.delete(0, tk.END)
    entry_ten.insert(0, v[2])
    gender_var.set(v[3])
    date_entry.set_date(v[4])
    cbb_chucvu.set(v[5])

def luu_nv():
    conn.execute("""UPDATE nhanvien SET holot=?, ten=?, phai=?, ngaysinh=?, chucvu=? WHERE maso=?""",
                 (entry_holot.get(), entry_ten.get(), gender_var.get(),
                  date_entry.get(), cbb_chucvu.get(), entry_maso.get()))
    conn.commit()
    load_nv()

frame_btn_nv = tk.Frame(tab_nv)
frame_btn_nv.pack(pady=5)
tk.Button(frame_btn_nv, text="Thêm", width=8,
          bg="#4CAF50", fg="white" ,command=them_nv).grid(row=0, column=0, padx=5)
tk.Button(frame_btn_nv, text="Sửa", width=8,
          bg="#4CAF50", fg="white", command=sua_nv).grid(row=0, column=1, padx=5)
tk.Button(frame_btn_nv, text="Lưu", width=8,
          bg="#4CAF50", fg="white", command=luu_nv).grid(row=0, column=2, padx=5)
tk.Button(frame_btn_nv, text="Xóa", width=8,
          bg="#4CAF50", fg="white", command=xoa_nv).grid(row=0, column=3, padx=5)

load_nv()

# -----------------------------------------------------------------
# TAB 2: KHÁCH HÀNG
# -----------------------------------------------------------------
tab_kh = ttk.Frame(notebook)
notebook.add(tab_kh, text="Khách hàng")

frame_kh = tk.LabelFrame(tab_kh, text="Thông tin khách hàng")
frame_kh.pack(padx=10, pady=10, fill="x")

entry_makh = tk.Entry(frame_kh, width=10)
entry_hoten = tk.Entry(frame_kh, width=25)
entry_sdt = tk.Entry(frame_kh, width=15)
entry_cmnd = tk.Entry(frame_kh, width=15)

tk.Label(frame_kh, text="Mã KH").grid(row=0, column=0, padx=5, pady=5)
entry_makh.grid(row=0, column=1, padx=5)
tk.Label(frame_kh, text="Họ tên").grid(row=0, column=2, padx=5)
entry_hoten.grid(row=0, column=3, padx=5)
tk.Label(frame_kh, text="SĐT").grid(row=1, column=0, padx=5)
entry_sdt.grid(row=1, column=1, padx=5)
tk.Label(frame_kh, text="CMND").grid(row=1, column=2, padx=5)
entry_cmnd.grid(row=1, column=3, padx=5)

columns_kh = ("makh", "hoten", "sdt", "cmnd")
tree_kh = ttk.Treeview(tab_kh, columns=columns_kh, show="headings", height=10)
for col in columns_kh:
    tree_kh.heading(col, text=col.upper())
tree_kh.pack(padx=10, pady=10, fill="both")

def load_kh():
    for i in tree_kh.get_children():
        tree_kh.delete(i)
    cur = conn.cursor()
    cur.execute("SELECT * FROM khachhang")
    for row in cur.fetchall():
        tree_kh.insert("", tk.END, values=row)

def them_kh():
    try:
        conn.execute("INSERT INTO khachhang VALUES (?, ?, ?, ?)",
                     (entry_makh.get(), entry_hoten.get(), entry_sdt.get(), entry_cmnd.get()))
        conn.commit()
        load_kh()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def sua_kh():
    sel = tree_kh.selection()
    if not sel: return
    v = tree_kh.item(sel)["values"]
    entry_makh.delete(0, tk.END)
    entry_makh.insert(0, v[0])
    entry_hoten.delete(0, tk.END)
    entry_hoten.insert(0, v[1])
    entry_sdt.delete(0, tk.END)
    entry_sdt.insert(0, v[2])
    entry_cmnd.delete(0, tk.END)
    entry_cmnd.insert(0, v[3])

def luu_kh():
    conn.execute("UPDATE khachhang SET hoten=?, sdt=?, cmnd=? WHERE makh=?",
                 (entry_hoten.get(), entry_sdt.get(), entry_cmnd.get(), entry_makh.get()))
    conn.commit()
    load_kh()

def xoa_kh():
    sel = tree_kh.selection()
    if not sel: return
    makh = tree_kh.item(sel)["values"][0]
    conn.execute("DELETE FROM khachhang WHERE makh=?", (makh,))
    conn.commit()
    load_kh()

frame_btn_kh = tk.Frame(tab_kh)
frame_btn_kh.pack(pady=5)
tk.Button(frame_btn_kh, text="Thêm", command=them_kh, width=8,
          bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5)
tk.Button(frame_btn_kh, text="Sửa", command=sua_kh, width=8,
          bg="#4CAF50", fg="white").grid(row=0, column=1, padx=5)
tk.Button(frame_btn_kh, text="Lưu", command=luu_kh, width=8,
          bg="#4CAF50", fg="white").grid(row=0, column=2, padx=5)
tk.Button(frame_btn_kh, text="Xóa", command=xoa_kh, width=8,
          bg="#4CAF50", fg="white").grid(row=0, column=3, padx=5)

load_kh()

# -----------------------------------------------------------------
# TAB 3: PHÒNG
# -----------------------------------------------------------------
tab_p = ttk.Frame(notebook)
notebook.add(tab_p, text="Phòng")

# Form nhập liệu
frame_p = tk.LabelFrame(tab_p, text="Thông tin phòng")
frame_p.pack(padx=10, pady=10, fill="x")

tk.Label(frame_p, text="Mã phòng").grid(row=0, column=0, padx=5, pady=5)
entry_maphong = tk.Entry(frame_p, width=10)
entry_maphong.grid(row=0, column=1, padx=5)

tk.Label(frame_p, text="Loại phòng").grid(row=0, column=2, padx=5)
cbb_loaiphong = ttk.Combobox(frame_p, values=["Đơn", "Đôi", "VIP"], width=10)
cbb_loaiphong.grid(row=0, column=3, padx=5)

tk.Label(frame_p, text="Trạng thái").grid(row=0, column=4, padx=5)
cbb_trangthai = ttk.Combobox(frame_p, values=["Trống", "Đang thuê", "Bảo trì"], width=12)
cbb_trangthai.grid(row=0, column=5, padx=5)

tk.Label(frame_p, text="Giá").grid(row=0, column=6, padx=5, pady=5)
entry_gia = tk.Entry(frame_p, width=12)
entry_gia.grid(row=0, column=7, padx=5)

# Treeview hiển thị 4 cột
columns_p = ("maphong", "loaiphong", "trangthai", "gia")
tree_p = ttk.Treeview(tab_p, columns=columns_p, show="headings", height=10)
for col in columns_p:
    tree_p.heading(col, text=col.upper())
tree_p.pack(padx=10, pady=10, fill="both")
style = ttk.Style()
style.configure("Treeview", background="#f0f0f0", foreground="black", rowheight=25, fieldbackground="#f0f0f0")
style.map("Treeview", background=[("selected", "#6fa1f2")])  # màu khi chọn

# Thêm dữ liệu với màu xen kẽ
tree_p.tag_configure('oddrow', background="#17be4a")
tree_p.tag_configure('evenrow', background="#09902F")

# ------------------ Hàm CRUD ------------------
def load_p():
    for i in tree_p.get_children():
        tree_p.delete(i)
    cur = conn.cursor()
    cur.execute("SELECT * FROM phong")
    for row in cur.fetchall():
        tree_p.insert("", tk.END, values=row)

def them_p():
    if not entry_maphong.get():
        messagebox.showwarning("Cảnh báo", "Mã phòng không được để trống")
        return
    try:
        conn.execute("INSERT INTO phong VALUES (?, ?, ?, ?)",
                     (entry_maphong.get(), cbb_loaiphong.get(),
                      cbb_trangthai.get(), entry_gia.get()))
        conn.commit()
        load_p()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
       

def sua_p():
    sel = tree_p.selection()
    if not sel: return
    v = tree_p.item(sel)["values"]
    entry_maphong.delete(0, tk.END)
    entry_maphong.insert(0, v[0])
    cbb_loaiphong.set(v[1])
    cbb_trangthai.set(v[2])
    entry_gia.delete(0, tk.END)
    entry_gia.insert(0, v[3])

def luu_p():
    try:
        conn.execute("UPDATE phong SET loaiphong=?, trangthai=?, gia=? WHERE maphong=?",
                     (cbb_loaiphong.get(), cbb_trangthai.get(),
                      entry_gia.get(), entry_maphong.get()))
        conn.commit()
        load_p()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def xoa_p():
    sel = tree_p.selection()
    if not sel: return
    maphong = tree_p.item(sel)["values"][0]
    try:
        conn.execute("DELETE FROM phong WHERE maphong=?", (maphong,))
        conn.commit()
        load_p()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

# Khi chọn Treeview tự động điền form
def on_select_p(event):
    sua_p()

tree_p.bind("<<TreeviewSelect>>", on_select_p)

# Nút thao tác
frame_btn_p = tk.Frame(tab_p)
frame_btn_p.pack(pady=5)

tk.Button(frame_btn_p, text="Thêm", command=them_p, width=8,
          bg="#4CACAF", fg="white").grid(row=0, column=0, padx=5)
tk.Button(frame_btn_p, text="Sửa", command=sua_p, width=8,
          bg="#4CACAF", fg="white").grid(row=0, column=1, padx=5)
tk.Button(frame_btn_p, text="Lưu", command=luu_p, width=8,
          bg="#4CAFAF", fg="white").grid(row=0, column=2, padx=5)
tk.Button(frame_btn_p, text="Xóa", command=xoa_p, width=8,
          bg="#4CACAF", fg="white").grid(row=0, column=3, padx=5)

# Load dữ liệu lúc đầu
load_p()
# -----------------------------------------------------------------
# TAB 4: ĐẶT PHÒNG
# -----------------------------------------------------------------
tab_dp = ttk.Frame(notebook)
notebook.add(tab_dp, text="Đặt phòng")

frame_dp = tk.LabelFrame(tab_dp, text="Thông tin đặt phòng")
frame_dp.pack(padx=10, pady=10, fill="x")

entry_madat = tk.Entry(frame_dp, width=10)
cbb_kh = ttk.Combobox(frame_dp, width=25)
cbb_phong = ttk.Combobox(frame_dp, width=15)
date_dat = DateEntry(frame_dp, width=12, date_pattern="yyyy-mm-dd")
date_tra = DateEntry(frame_dp, width=12, date_pattern="yyyy-mm-dd")

tk.Label(frame_dp, text="Mã đặt").grid(row=0, column=0, padx=5, pady=5)
entry_madat.grid(row=0, column=1, padx=5)
tk.Label(frame_dp, text="Khách hàng").grid(row=0, column=2, padx=5)
cbb_kh.grid(row=0, column=3, padx=5)
tk.Label(frame_dp, text="Phòng").grid(row=0, column=4, padx=5)
cbb_phong.grid(row=0, column=5, padx=5)
tk.Label(frame_dp, text="Ngày đặt").grid(row=1, column=0, padx=5)
date_dat.grid(row=1, column=1, padx=5)
tk.Label(frame_dp, text="Ngày trả").grid(row=1, column=2, padx=5)
date_tra.grid(row=1, column=3, padx=5)

columns_dp = ("madat", "makh", "maphong", "ngaydat", "ngaytra")
tree_dp = ttk.Treeview(tab_dp, columns=columns_dp, show="headings", height=10)
for col in columns_dp:
    tree_dp.heading(col, text=col.upper())
tree_dp.pack(padx=10, pady=10, fill="both")

def load_dp():
    for i in tree_dp.get_children():
        tree_dp.delete(i)
    cur = conn.cursor()
    cur.execute("SELECT * FROM datphong")
    for row in cur.fetchall():
        tree_dpg
    for row in cur.fetchall():
        tree_dp.insert("", tk.END, values=row)

def them_dp():
    try:
        conn.execute("INSERT INTO datphong VALUES (?, ?, ?, ?, ?)",
                     (entry_madat.get(),
                      cbb_kh.get().split(" - ")[0],   # lấy mã KH từ combobox
                      cbb_phong.get(),
                      date_dat.get(),
                      date_tra.get()))
        conn.commit()

        # Cập nhật trạng thái phòng
        conn.execute("UPDATE phong SET trangthai='Đang thuê' WHERE maphong=?", (cbb_phong.get(),))
        conn.commit()

        load_dp()
        refresh_combobox_phong(cbb_phong)
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def sua_dp():
    sel = tree_dp.selection()
    if not sel: return
    v = tree_dp.item(sel)["values"]
    entry_madat.delete(0, tk.END)
    entry_madat.insert(0, v[0])
    cbb_kh.set(v[1])
    cbb_phong.set(v[2])
    date_dat.set_date(v[3])
    date_tra.set_date(v[4])

def luu_dp():
    try:
        conn.execute("""UPDATE datphong SET makh=?, maphong=?, ngaydat=?, ngaytra=? WHERE madat=?""",
                     (cbb_kh.get().split(" - ")[0],
                      cbb_phong.get(),
                      date_dat.get(),
                      date_tra.get(),
                      entry_madat.get()))
        conn.commit()
        load_dp()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def xoa_dp():
    sel = tree_dp.selection()
    if not sel: return
    madat, maphong = tree_dp.item(sel)["values"][0], tree_dp.item(sel)["values"][2]
    try:
        conn.execute("DELETE FROM datphong WHERE madat=?", (madat,))
        conn.commit()

        # Phòng được xóa đặt thì trả về trạng thái Trống
        conn.execute("UPDATE phong SET trangthai='Trống' WHERE maphong=?", (maphong,))
        conn.commit()

        load_dp()
        refresh_combobox_phong(cbb_phong)
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

frame_btn_dp = tk.Frame(tab_dp)
frame_btn_dp.pack(pady=5)

tk.Button(frame_btn_dp, text="Thêm", width=8, bg="#4CAF50", fg="white",
          command=them_dp).grid(row=0, column=0, padx=5)
tk.Button(frame_btn_dp, text="Sửa", width=8, bg="#4CAF50", fg="white",
          command=sua_dp).grid(row=0, column=1, padx=5)
tk.Button(frame_btn_dp, text="Lưu", width=8, bg="#4CAF50", fg="white",
          command=luu_dp).grid(row=0, column=2, padx=5)
tk.Button(frame_btn_dp, text="Xóa", width=8, bg="#4CAF50", fg="white",
          command=xoa_dp).grid(row=0, column=3, padx=5)

# Khi chọn Treeview -> tự điền form
def on_select_dp(event):
    sua_dp()
tree_dp.bind("<<TreeviewSelect>>", on_select_dp)

# Tải dữ liệu combobox và bảng khi mở
refresh_combobox_khachhang(cbb_kh)
refresh_combobox_phong(cbb_phong)
load_dp()
root.mainloop()

