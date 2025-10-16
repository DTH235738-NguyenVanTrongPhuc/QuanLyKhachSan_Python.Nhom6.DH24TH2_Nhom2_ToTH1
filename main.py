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

# Setup logging với mức độ chi tiết cao
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
        logger.info("🚀 Khởi tạo ứng dụng Quản lý Khách sạn")
        try:
            logger.info("🖥️ Đang tạo cửa sổ chính...")
            self.root = tk.Tk()
            logger.info(f"✅ Đã tạo cửa sổ chính: {self.root}")
            
            self.root.title("HỆ THỐNG QUẢN LÝ KHÁCH SẠN")
            
            # Kiểm tra kích thước màn hình
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            logger.info(f"📺 Kích thước màn hình: {screen_width}x{screen_height}")
            
            center_window(self.root, APP_CONFIG['window_width'], APP_CONFIG['window_height'])
            self.root.resizable(True, True)
            
            # Initialize database
            logger.info("🔗 Đang kết nối database...")
            self.db = Database()
            if self.db.connection is None:
                logger.error("❌ Kết nối database thất bại!")
                self.root.destroy()
                return
            logger.info("✅ Kết nối database thành công")
            
            # Current user info
            self.current_user_id = None
            self.current_user_role = None
            self.current_user_name = None
            
            # Create UI with login tab first
            self.create_ui()
            
        except Exception as e:
            logger.error(f"❌ Lỗi khởi tạo ứng dụng: {str(e)}", exc_info=True)
            import traceback
            traceback.print_exc()

    def create_ui(self):
        logger.info("🎨 Đang tạo giao diện chính")
        try:
            # Clear existing widgets
            for widget in self.root.winfo_children():
                widget.destroy()

            # Create notebook for tabs
            self.notebook = ttk.Notebook(self.root)
            self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

            # Create login tab (always visible)
            self.login_tab = LoginView(self.notebook, self.db, self.on_login_success)
            self.notebook.add(self.login_tab.tab, text="Đăng nhập")

            # Create other tabs but disable them initially
            self.employee_tab = EmployeeView(self.notebook, self.db, None)
            self.customer_tab = CustomerView(self.notebook, self.db)
            self.room_tab = RoomView(self.notebook, self.db, None)
            self.booking_tab = BookingView(self.notebook, self.db, None, None)

            # Add tabs but disable them
            self.notebook.add(self.employee_tab.tab, text="Nhân viên")
            self.notebook.add(self.customer_tab.tab, text="Khách hàng")
            self.notebook.add(self.room_tab.tab, text="Quản lý phòng")
            self.notebook.add(self.booking_tab.tab, text="Đặt phòng")

            # Initially disable all tabs except login
            self.update_tab_access()

            logger.info("✅ Đã tạo giao diện chính thành công")
            
        except Exception as e:
            logger.error(f"❌ Lỗi tạo giao diện chính: {str(e)}", exc_info=True)

    def on_login_success(self, user_id, role, user_name):
        logger.info(f"✅ Đăng nhập thành công: {user_name} ({user_id}) - Vai trò: {role}")
        self.current_user_id = user_id
        self.current_user_role = role
        self.current_user_name = user_name
        
        # Update all views with current user info
        self.update_views_with_user()
        self.update_tab_access()
        
        # Show user info
        self.show_user_info()

    def update_views_with_user(self):
        """Update all views with current user information"""
        # Update employee view
        self.employee_tab.current_user_role = self.current_user_role
        self.employee_tab.create_widgets()  # Recreate widgets to update button states
        
        # Update room view
        self.room_tab.current_user_role = self.current_user_role
        self.room_tab.create_widgets()
        
        # Update booking view
        self.booking_tab.current_user_id = self.current_user_id
        self.booking_tab.current_user_role = self.current_user_role
        self.booking_tab.lbl_nhanvien.config(text=self.current_user_id)
        self.booking_tab.refresh_data()

    def update_tab_access(self):
        """Enable or disable tabs based on login status"""
        is_logged_in = self.current_user_id is not None
        
        # Get all tab names
        tab_names = ["Đăng nhập", "Nhân viên", "Khách hàng", "Quản lý phòng", "Đặt phòng"]
        
        # Enable all tabs if logged in, otherwise only enable login tab
        for i, tab_name in enumerate(tab_names):
            if is_logged_in:
                self.notebook.tab(i, state="normal")
            else:
                if tab_name == "Đăng nhập":
                    self.notebook.tab(i, state="normal")
                    self.notebook.select(i)  # Select login tab
                else:
                    self.notebook.tab(i, state="disabled")

    def show_user_info(self):
        try:
            # Check if user info frame already exists
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Frame) and hasattr(widget, '_is_user_frame'):
                    widget.destroy()

            user_frame = tk.Frame(self.root, bg="#2c3e50", height=40)
            user_frame.pack(fill="x", padx=10, pady=5)
            user_frame.pack_propagate(False)
            user_frame._is_user_frame = True  # Mark as user frame
            
            user_info = f"Xin chào: {self.current_user_name} ({self.current_user_id}) - Vai trò: {self.current_user_role}"
            tk.Label(user_frame, text=user_info, bg="#2c3e50", fg="white",
                    font=("Arial", 10, "bold")).pack(side="left", padx=10, pady=10)
            
            # Logout button
            tk.Button(user_frame, text="Đăng xuất", bg="#e74c3c", fg="white",
                     font=("Arial", 9, "bold"), command=self.logout).pack(side="right", padx=10, pady=5)
        except Exception as e:
            logger.error(f"❌ Lỗi hiển thị thông tin user: {str(e)}")

    def logout(self):
        logger.info("🚪 Đang đăng xuất")
        
        # Reset user info
        self.current_user_id = None
        self.current_user_role = None
        self.current_user_name = None
        
        # Remove user info frame
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) and hasattr(widget, '_is_user_frame'):
                widget.destroy()
        
        # Update views and tab access
        self.update_views_with_user()
        self.update_tab_access()

    def run(self):
        logger.info("🔄 Bắt đầu vòng lặp chính")
        try:
            logger.info("🏃 Ứng dụng đang chạy...")
            self.root.mainloop()
            logger.info("👋 Ứng dụng đã đóng")
        except Exception as e:
            logger.error(f"❌ Lỗi trong vòng lặp chính: {str(e)}", exc_info=True)

if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("ỨNG DỤNG QUẢN LÝ KHÁCH SẠN BẮT ĐẦU CHẠY")
    logger.info("=" * 50)
    
    # Kiểm tra environment
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Current directory: {os.getcwd()}")
    logger.info(f"Tkinter version: {tk.TkVersion}")
    
    app = HotelManagementApp()
    app.run()