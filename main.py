import tkinter as tk
from tkinter import ttk
from database import Database
from utils import center_window
from views.employee_view import EmployeeView
from views.customer_view import CustomerView
from views.room_view import RoomView
from views.booking_view import BookingView
from config import APP_CONFIG

class HotelManagementApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("QUẢN LÝ KHÁCH SẠN")
        center_window(self.root, APP_CONFIG['window_width'], APP_CONFIG['window_height'])
        self.root.resizable(False, False)
        
        # Initialize database
        self.db = Database()
        if self.db.connection is None:
            self.root.destroy()
            return
            
        self.create_ui()
        
    def create_ui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Create tabs
        self.employee_tab = EmployeeView(self.notebook, self.db)
        self.customer_tab = CustomerView(self.notebook, self.db)
        self.room_tab = RoomView(self.notebook, self.db)
        self.booking_tab = BookingView(self.notebook, self.db)

        # Add tabs to notebook
        self.notebook.add(self.employee_tab.tab, text="Nhân viên")
        self.notebook.add(self.customer_tab.tab, text="Khách hàng")
        self.notebook.add(self.room_tab.tab, text="Phòng")
        self.notebook.add(self.booking_tab.tab, text="Đặt phòng")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = HotelManagementApp()
    app.run()