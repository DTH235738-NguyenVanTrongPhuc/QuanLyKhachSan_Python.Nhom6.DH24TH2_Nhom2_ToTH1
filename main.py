# main.py - Enhanced version with login tab
import tkinter as tk
from tkinter import ttk
import logging
import sys
import os
from database import Database
from utils import center_window
from views.employee_view import EmployeeView
from views.customer_view import CustomerView
from views.room_view import RoomView
from views.booking_view import BookingView
from views.login_view import LoginView
from config import APP_CONFIG

# ! THIẾT LẬP LOGGING VỚI MỨC ĐỘ CHI TIẾT CAO
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app_debug.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class HotelManagementApp:
    def __init__(self):
        # ! KHỞI TẠO ỨNG DỤNG QUẢN LÝ KHÁCH SẠN
        logger.info(" Khởi tạo ứng dụng Quản lý Khách sạn")
        try:
            logger.info("Đang tạo cửa sổ chính...")
            self.root = tk.Tk()
            logger.info(f"Đã tạo cửa sổ chính: {self.root}")
            
            self.root.title("HỆ THỐNG QUẢN LÝ KHÁCH SẠN")
            
            # ! KIỂM TRA KÍCH THƯỚC MÀN HÌNH
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            logger.info(f"Kích thước màn hình: {screen_width}x{screen_height}")
            
            center_window(self.root, APP_CONFIG['window_width'], APP_CONFIG['window_height'])
            self.root.resizable(True, True)
            
            # ! KHỞI TẠO KẾT NỐI DATABASE
            logger.info("Đang kết nối database...")
            self.db = Database()
            if self.db.connection is None:
                logger.error("Kết nối database thất bại!")
                self.root.destroy()
                return
            logger.info(" Kết nối database thành công")
            
            # ! THÔNG TIN USER HIỆN TẠI
            self.current_user_id = None
            self.current_user_role = None
            self.current_user_name = None
            
            # ! KHỞI TẠO BIẾN TAB VỚI GIÁ TRỊ NONE
            self.employee_tab = None
            self.customer_tab = None
            self.room_tab = None
            self.booking_tab = None
            
            # ! TẠO UI VỚI TAB ĐĂNG NHẬP ĐẦU TIÊN
            self.create_ui()
            
        except Exception as e:
            logger.error(f" Lỗi khởi tạo ứng dụng: {str(e)}", exc_info=True)
            import traceback
            traceback.print_exc()

    def create_ui(self):
        # ! TẠO GIAO DIỆN NGƯỜI DÙNG CHÍNH
        logger.info(" Đang tạo giao diện chính")
        try:
            # ! XÓA CÁC WIDGET HIỆN CÓ
            for widget in self.root.winfo_children():
                widget.destroy()

            # ! TẠO NOTEBOOK CHO CÁC TAB
            self.notebook = ttk.Notebook(self.root)
            self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

            # ! TẠO TAB ĐĂNG NHẬP (LUÔN HIỂN THỊ)
            self.login_tab = LoginView(self.notebook, self.db, self.on_login_success)
            self.notebook.add(self.login_tab.tab, text="Đăng nhập")

            # ! TẠO CÁC TAB KHÁC NHƯNG VÔ HIỆU HÓA BAN ĐẦU
            self.employee_tab = EmployeeView(self.notebook, self.db, None)
            self.customer_tab = CustomerView(self.notebook, self.db)
            self.room_tab = RoomView(self.notebook, self.db, None)
            self.booking_tab = BookingView(self.notebook, self.db, None, None)

            # ! THÊM CÁC TAB NHƯNG VÔ HIỆU HÓA CHÚNG
            self.notebook.add(self.employee_tab.tab, text="Nhân viên")
            self.notebook.add(self.customer_tab.tab, text="Khách hàng")
            self.notebook.add(self.room_tab.tab, text="Quản lý phòng")
            self.notebook.add(self.booking_tab.tab, text="Đặt phòng")

            # ! BAN ĐẦU VÔ HIỆU HÓA TẤT CẢ TAB TRỪ ĐĂNG NHẬP
            self.update_tab_access()

            logger.info("Đã tạo giao diện chính thành công")
            
        except Exception as e:
            logger.error(f" Lỗi tạo giao diện chính: {str(e)}", exc_info=True)

    def on_login_success(self, user_id, role, user_name):
        # ! CALLBACK KHI ĐĂNG NHẬP THÀNH CÔNG
        logger.info(f"Đăng nhập thành công: {user_name} ({user_id}) - Vai trò: {role}")
        self.current_user_id = user_id
        self.current_user_role = role
        self.current_user_name = user_name
        
        # ! CẬP NHẬT TẤT CẢ VIEWS VỚI THÔNG TIN USER
        self.update_views_with_user()
        self.update_tab_access()
        
        # ! HIỂN THỊ THÔNG TIN USER
        self.show_user_info()

    def update_views_with_user(self):
        # ! CẬP NHẬT TẤT CẢ VIEWS VỚI THÔNG TIN USER HIỆN TẠI
        try:
            # ! CẬP NHẬT EMPLOYEE VIEW - CHỈ CẬP NHẬT ROLE, KHÔNG TẠO LẠI WIDGETS
            if self.employee_tab:
                self.employee_tab.current_user_role = self.current_user_role
                # ! CẬP NHẬT TRẠNG THÁI NÚT DỰA TRÊN ROLE
                self.update_employee_buttons()
            
            # ! CẬP NHẬT ROOM VIEW
            if self.room_tab:
                self.room_tab.current_user_role = self.current_user_role
                self.update_room_buttons()
            
            # ! CẬP NHẬT BOOKING VIEW
            if self.booking_tab:
                self.booking_tab.current_user_id = self.current_user_id
                self.booking_tab.current_user_role = self.current_user_role
                # ! CẬP NHẬT LABEL NHÂN VIÊN
                self.booking_tab.lbl_nhanvien.config(text=self.current_user_id)
                self.booking_tab.refresh_data()
                
        except Exception as e:
            logger.error(f"Lỗi cập nhật views: {str(e)}")

    def update_employee_buttons(self):
        # ! CẬP NHẬT TRẠNG THÁI NÚT TRONG EMPLOYEE VIEW
        if not self.employee_tab:
            return
            
        # ! TÌM TẤT CẢ CÁC NÚT TRONG FRAME_BTN
        for widget in self.employee_tab.tab.winfo_children():
            if isinstance(widget, tk.Frame):
                for btn in widget.winfo_children():
                    if isinstance(btn, tk.Button):
                        btn_text = btn.cget('text')
                        if btn_text in ["Thêm", "Sửa", "Xóa"]:
                            if self.current_user_role != "Trưởng phòng":
                                btn.config(state="disabled")
                            else:
                                btn.config(state="normal")

    def update_room_buttons(self):
        # ! CẬP NHẬT TRẠNG THÁI NÚT TRONG ROOM VIEW
        if not self.room_tab:
            return
            
        # ! TÌM TẤT CẢ CÁC NÚT TRONG FRAME_BTN
        for widget in self.room_tab.tab.winfo_children():
            if isinstance(widget, tk.Frame):
                for btn in widget.winfo_children():
                    if isinstance(btn, tk.Button):
                        btn_text = btn.cget('text')
                        if btn_text in ["Thêm", "Sửa", "Xóa"]:
                            if self.current_user_role != "Trưởng phòng":
                                btn.config(state="disabled")
                            else:
                                btn.config(state="normal")

    def update_tab_access(self):
        # ! BẬT HOẶC TẮT TRUY CẬP TAB DỰA TRÊN TRẠNG THÁI ĐĂNG NHẬP
        is_logged_in = self.current_user_id is not None
        
        # ! LẤY TẤT CẢ TÊN TAB
        tab_names = ["Đăng nhập", "Nhân viên", "Khách hàng", "Quản lý phòng", "Đặt phòng"]
        
        # ! BẬT TẤT CẢ TAB NẾU ĐÃ ĐĂNG NHẬP, NGƯỢC LẠI CHỈ BẬT TAB ĐĂNG NHẬP
        for i, tab_name in enumerate(tab_names):
            if is_logged_in:
                self.notebook.tab(i, state="normal")
                if tab_name == "Đăng nhập":
                    self.notebook.tab(i, state="normal")
                else:
                    self.notebook.tab(i, state="normal")
            else:
                if tab_name == "Đăng nhập":
                    self.notebook.tab(i, state="normal")
                    self.notebook.select(i)  # ! CHỌN TAB ĐĂNG NHẬP
                else:
                    self.notebook.tab(i, state="disabled")

    def show_user_info(self):
        # ! HIỂN THỊ THÔNG TIN USER TRÊN GIAO DIỆN
        try:
            # ! KIỂM TRA XEM USER INFO FRAME ĐÃ TỒN TẠI CHƯA
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Frame) and hasattr(widget, '_is_user_frame'):
                    widget.destroy()

            user_frame = tk.Frame(self.root, bg="#2c3e50", height=40)
            user_frame.pack(fill="x", padx=10, pady=5)
            user_frame.pack_propagate(False)
            user_frame._is_user_frame = True  # ! ĐÁNH DẤU LÀ USER FRAME
            
            user_info = f"Xin chào: {self.current_user_name} ({self.current_user_id}) - Vai trò: {self.current_user_role}"
            tk.Label(user_frame, text=user_info, bg="#2c3e50", fg="white",
                    font=("Arial", 10, "bold")).pack(side="left", padx=10, pady=10)
            
            # ! NÚT ĐĂNG XUẤT
            tk.Button(user_frame, text="Đăng xuất", bg="#e74c3c", fg="white",
                     font=("Arial", 9, "bold"), command=self.logout).pack(side="right", padx=10, pady=5)
        except Exception as e:
            logger.error(f" Lỗi hiển thị thông tin user: {str(e)}")

    def logout(self):
        # ! XỬ LÝ ĐĂNG XUẤT
        logger.info(" Đang đăng xuất")
        
        # ! RESET THÔNG TIN USER
        self.current_user_id = None
        self.current_user_role = None
        self.current_user_name = None
        
        # ! XÓA USER INFO FRAME
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) and hasattr(widget, '_is_user_frame'):
                widget.destroy()
        
        # ! CẬP NHẬT VIEWS VÀ TRUY CẬP TAB
        self.update_views_with_user()
        self.update_tab_access()

    def run(self):
        # ! CHẠY ỨNG DỤNG
        logger.info(" Bắt đầu vòng lặp chính")
        try:
            logger.info(" Ứng dụng đang chạy...")
            self.root.mainloop()
            logger.info(" Ứng dụng đã đóng")
        except Exception as e:
            logger.error(f" Lỗi trong vòng lặp chính: {str(e)}", exc_info=True)

if __name__ == "__main__":
    # ! KHỞI CHẠY ỨNG DỤNG
    logger.info("=" * 50)
    logger.info("ỨNG DỤNG QUẢN LÝ KHÁCH SẠN BẮT ĐẦU CHẠY")
    logger.info("=" * 50)
    
    # ! KIỂM TRA MÔI TRƯỜNG
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Current directory: {os.getcwd()}")
    logger.info(f"Tkinter version: {tk.TkVersion}")
    
    app = HotelManagementApp()
    app.run()