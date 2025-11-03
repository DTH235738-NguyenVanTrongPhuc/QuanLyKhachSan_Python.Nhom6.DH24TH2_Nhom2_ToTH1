# 🏨 HỆ THỐNG QUẢN LÝ KHÁCH SẠN

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> **Dự án Quản Lý Khách Sạn** - Ứng dụng desktop quản lý khách sạn toàn diện được xây dựng bằng Python Tkinter và SQLite

---

## 📋 Mục Lục

- [Giới Thiệu](#-giới-thiệu)
- [Tính Năng](#-tính-năng)
- [Công Nghệ Sử Dụng](#-công-nghệ-sử-dụng)
- [Cài Đặt](#-cài-đặt)
- [Hướng Dẫn Sử Dụng](#-hướng-dẫn-sử-dụng)
- [Cấu Trúc Dự Án](#-cấu-trúc-dự-án)
- [Cơ Sở Dữ Liệu](#-cơ-sở-dữ-liệu)
- [Screenshots](#-screenshots)
- [Đóng Góp](#-đóng-góp)
- [Thông Tin Nhóm](#-thông-tin-nhóm)
- [Giấy Phép](#-giấy-phép)

---

## 🎯 Giới Thiệu

**Hệ Thống Quản Lý Khách Sạn** là một ứng dụng desktop được phát triển nhằm giúp các khách sạn vừa và nhỏ quản lý hoạt động kinh doanh một cách hiệu quả và chuyên nghiệp. Ứng dụng cung cấp giao diện thân thiện, dễ sử dụng với đầy đủ các tính năng cần thiết cho việc vận hành một khách sạn.

### 🌟 Điểm Nổi Bật

- ✅ Giao diện trực quan, dễ sử dụng
- ✅ Quản lý đầy đủ thông tin phòng, khách hàng và đặt phòng
- ✅ Báo cáo thống kê chi tiết theo thời gian thực
- ✅ Tìm kiếm và lọc thông tin nhanh chóng
- ✅ Không cần kết nối internet, hoạt động offline
- ✅ Dữ liệu được lưu trữ an toàn với SQLite

---

## 🚀 Tính Năng

### 1. 🔐 Quản Lý Người Dùng
- Đăng nhập/Đăng xuất hệ thống
- Phân quyền người dùng (Admin, Lễ tân, Quản lý)
- Quản lý thông tin tài khoản

### 2. 🏠 Quản Lý Phòng
- Thêm, sửa, xóa thông tin phòng
- Phân loại phòng (Standard, Deluxe, Suite, VIP)
- Theo dõi trạng thái phòng (Trống, Đã đặt, Đang sử dụng, Bảo trì)
- Cập nhật giá phòng theo từng loại
- Xem lịch sử sử dụng phòng

### 3. 👥 Quản Lý Khách Hàng
- Lưu trữ thông tin khách hàng chi tiết
- Tìm kiếm khách hàng nhanh chóng
- Lịch sử đặt phòng của khách hàng
- Quản lý khách hàng thân thiết

### 4. 📅 Quản Lý Đặt Phòng
- Đặt phòng mới
- Check-in/Check-out
- Gia hạn thời gian lưu trú
- Hủy đặt phòng
- Xem lịch đặt phòng theo ngày/tuần/tháng
- Tính toán tự động chi phí lưu trú

### 5. 💰 Quản Lý Thanh Toán
- Tạo hóa đơn tự động
- Quản lý các hình thức thanh toán
- Theo dõi công nợ
- In hóa đơn

### 6. 🍽️ Quản Lý Dịch Vụ
- Quản lý dịch vụ ăn uống
- Dịch vụ giặt ủi
- Dịch vụ spa và massage
- Các dịch vụ bổ sung khác

### 7. 📊 Báo Cáo & Thống Kê
- Thống kê doanh thu theo ngày/tháng/năm
- Báo cáo tỷ lệ lấp đầy phòng
- Thống kê khách hàng
- Phân tích xu hướng đặt phòng
- Xuất báo cáo ra file Excel/PDF

### 8. 🔍 Tìm Kiếm & Lọc
- Tìm kiếm nhanh theo nhiều tiêu chí
- Lọc dữ liệu theo điều kiện
- Sắp xếp thông tin linh hoạt

---

## 💻 Công Nghệ Sử Dụng

| Công Nghệ | Phiên Bản | Mục Đích |
|-----------|-----------|----------|
| **Python** | 3.8+ | Ngôn ngữ lập trình chính |
| **Tkinter** | Built-in | Xây dựng giao diện người dùng |
| **SQLite3** | Built-in | Cơ sở dữ liệu lưu trữ |
| **datetime** | Built-in | Xử lý ngày tháng |
| **re** | Built-in | Xử lý biểu thức chính quy |
| **hashlib** | Built-in | Mã hóa mật khẩu |

---

## 📦 Cài Đặt

### Yêu Cầu Hệ Thống

- **Hệ điều hành**: Windows 10/11, macOS 10.14+, hoặc Linux
- **Python**: Phiên bản 3.8 trở lên
- **RAM**: Tối thiểu 2GB
- **Ổ cứng**: 100MB dung lượng trống

### Các Bước Cài Đặt

#### 1. Clone Repository

```bash
git clone https://github.com/your-username/QuanLyKhachSan_Python.Nhom6.DH24TH2_Nhom2_ToTH1.git
cd QuanLyKhachSan_Python.Nhom6.DH24TH2_Nhom2_ToTH1
```

#### 2. Tạo Môi Trường Ảo (Khuyến nghị)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Cài Đặt Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Chạy Ứng Dụng

```bash
python main.py
```

---

## 📖 Hướng Dẫn Sử Dụng

### Đăng Nhập Lần Đầu

**Tài khoản mặc định:**
- **Username**: `admin`
- **Password**: `admin123`

⚠️ **Lưu ý**: Nên đổi mật khẩu ngay sau lần đăng nhập đầu tiên để bảo mật!

### Quy Trình Đặt Phòng

1. **Bước 1**: Chọn menu "Đặt Phòng" → "Đặt Phòng Mới"
2. **Bước 2**: Nhập thông tin khách hàng (hoặc tìm khách hàng có sẵn)
3. **Bước 3**: Chọn loại phòng và phòng cụ thể
4. **Bước 4**: Chọn ngày check-in và check-out
5. **Bước 5**: Xác nhận thông tin và hoàn tất đặt phòng

### Quy Trình Check-in

1. Tìm kiếm đặt phòng theo mã đặt phòng hoặc tên khách
2. Xác nhận thông tin khách hàng
3. Thu tiền đặt cọc (nếu chưa thanh toán)
4. Cập nhật trạng thái phòng thành "Đang sử dụng"

### Quy Trình Check-out

1. Tìm phòng đang sử dụng
2. Kiểm tra và tính toán chi phí lưu trú + dịch vụ
3. Tạo hóa đơn và thu tiền
4. Cập nhật trạng thái phòng thành "Trống"
5. In hóa đơn cho khách

---

## 📁 Cấu Trúc Dự Án

```
QuanLyKhachSan_Python.Nhom6.DH24TH2_Nhom2_ToTH1/
│
├── main.py                      # File chính để chạy ứng dụng
├── requirements.txt             # Danh sách thư viện cần thiết
├── README.md                    # File tài liệu này
│
├── database/                    # Thư mục cơ sở dữ liệu
│   ├── hotel.db                 # File database SQLite
│   ├── db_manager.py            # Quản lý kết nối database
│   └── init_db.py               # Khởi tạo database và dữ liệu mẫu
│
├── models/                      # Thư mục chứa các model
│   ├── user.py                  # Model người dùng
│   ├── room.py                  # Model phòng
│   ├── customer.py              # Model khách hàng
│   ├── booking.py               # Model đặt phòng
│   ├── payment.py               # Model thanh toán
│   └── service.py               # Model dịch vụ
│
├── views/                       # Thư mục giao diện
│   ├── login_view.py            # Màn hình đăng nhập
│   ├── main_view.py             # Màn hình chính
│   ├── room_view.py             # Quản lý phòng
│   ├── customer_view.py         # Quản lý khách hàng
│   ├── booking_view.py          # Quản lý đặt phòng
│   ├── payment_view.py          # Quản lý thanh toán
│   ├── service_view.py          # Quản lý dịch vụ
│   └── report_view.py           # Báo cáo thống kê
│
├── controllers/                 # Thư mục controllers
│   ├── user_controller.py       # Xử lý logic người dùng
│   ├── room_controller.py       # Xử lý logic phòng
│   ├── customer_controller.py   # Xử lý logic khách hàng
│   ├── booking_controller.py    # Xử lý logic đặt phòng
│   ├── payment_controller.py    # Xử lý logic thanh toán
│   └── service_controller.py    # Xử lý logic dịch vụ
│
├── utils/                       # Thư mục tiện ích
│   ├── validator.py             # Validation dữ liệu
│   ├── formatter.py             # Format dữ liệu hiển thị
│   ├── constants.py             # Các hằng số
│   └── helpers.py               # Các hàm hỗ trợ
│
├── assets/                      # Thư mục tài nguyên
│   ├── images/                  # Hình ảnh
│   ├── icons/                   # Icons
│   └── fonts/                   # Fonts chữ
│
├── reports/                     # Thư mục lưu báo cáo
│   ├── exports/                 # File báo cáo xuất ra
│   └── templates/               # Mẫu báo cáo
│
└── docs/                        # Tài liệu
    ├── user_manual.pdf          # Hướng dẫn sử dụng
    ├── technical_doc.pdf        # Tài liệu kỹ thuật
    └── database_schema.png      # Sơ đồ cơ sở dữ liệu
```

---

## 🗄️ Cơ Sở Dữ Liệu

### Sơ Đồ ERD

```
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│   USERS     │       │   BOOKINGS   │       │    ROOMS    │
├─────────────┤       ├──────────────┤       ├─────────────┤
│ user_id (PK)│       │ booking_id   │       │ room_id (PK)│
│ username    │       │ customer_id  │───────│ room_number │
│ password    │       │ room_id (FK) │       │ room_type   │
│ full_name   │       │ check_in     │       │ price       │
│ role        │       │ check_out    │       │ status      │
│ email       │       │ total_price  │       │ floor       │
│ phone       │       │ status       │       │ description │
└─────────────┘       └──────────────┘       └─────────────┘
                            │
                            │
                      ┌──────────────┐
                      │  CUSTOMERS   │
                      ├──────────────┤
                      │customer_id   │
                      │ full_name    │
                      │ id_card      │
                      │ phone        │
                      │ email        │
                      │ address      │
                      └──────────────┘
                            │
                            │
                      ┌──────────────┐       ┌─────────────┐
                      │  PAYMENTS    │       │  SERVICES   │
                      ├──────────────┤       ├─────────────┤
                      │ payment_id   │       │ service_id  │
                      │ booking_id   │       │ booking_id  │
                      │ amount       │       │ service_name│
                      │ payment_date │       │ price       │
                      │ method       │       │ quantity    │
                      └──────────────┘       └─────────────┘
```

### Bảng Chính

#### 1. USERS (Người Dùng)
Lưu trữ thông tin người dùng hệ thống với các quyền khác nhau.

#### 2. ROOMS (Phòng)
Quản lý thông tin tất cả các phòng trong khách sạn.

#### 3. CUSTOMERS (Khách Hàng)
Lưu trữ thông tin chi tiết của khách hàng.

#### 4. BOOKINGS (Đặt Phòng)
Quản lý tất cả các đặt phòng và lịch trình.

#### 5. PAYMENTS (Thanh Toán)
Theo dõi các giao dịch thanh toán.

#### 6. SERVICES (Dịch Vụ)
Quản lý các dịch vụ bổ sung cho khách hàng.

---

## 📸 Screenshots

### Màn Hình Đăng Nhập
```
┌─────────────────────────────────────┐
│     🏨 QUẢN LÝ KHÁCH SẠN          │
│                                     │
│   Username: [___________________]   │
│   Password: [___________________]   │
│                                     │
│         [ Đăng Nhập ]              │
│                                     │
└─────────────────────────────────────┘
```

### Dashboard Chính
```
╔═══════════════════════════════════════════╗
║  🏠 Trang Chủ  │  🛏️ Phòng  │  👤 Khách   ║
║  📅 Đặt Phòng  │  💰 Thanh Toán  │  📊 BC  ║
╠═══════════════════════════════════════════╣
║  📊 Thống Kê Nhanh                       ║
║  ┌──────────┬──────────┬──────────┐     ║
║  │ 45 Phòng │ 32 Đã Đặt│ 71% LĐF │     ║
║  └──────────┴──────────┴──────────┘     ║
║                                           ║
║  📈 Biểu Đồ Doanh Thu Tháng              ║
║  [████████████████████░░░░░░]            ║
╚═══════════════════════════════════════════╝
```

---

## 🤝 Đóng Góp

Chúng tôi luôn hoan nghênh mọi đóng góp để cải thiện dự án! 

### Cách Đóng Góp

1. **Fork** repository này
2. Tạo **branch** mới (`git checkout -b feature/TinhNangMoi`)
3. **Commit** thay đổi (`git commit -m 'Thêm tính năng mới'`)
4. **Push** lên branch (`git push origin feature/TinhNangMoi`)
5. Tạo **Pull Request**

### Quy Tắc Đóng Góp

- Viết code rõ ràng, dễ hiểu
- Thêm comment cho các phần phức tạp
- Tuân thủ PEP 8 style guide
- Test kỹ trước khi tạo pull request
- Cập nhật tài liệu nếu cần thiết

---

## 👥 Thông Tin Nhóm

### Nhóm 6 - DH24TH2 | Nhóm 2 - ToTH1

| Thành Viên | Vai Trò | Email | GitHub |
|------------|---------|-------|--------|
| **Nguyễn Văn A** | Nhóm trưởng - Backend Developer | nguyenvana@email.com | [@nguyenvana](#) |
| **Trần Thị B** | Frontend Developer | tranthib@email.com | [@tranthib](#) |
| **Lê Văn C** | Database Designer | levanc@email.com | [@levanc](#) |
| **Phạm Thị D** | UI/UX Designer | phamthid@email.com | [@phamthid](#) |
| **Hoàng Văn E** | Tester & Documentation | hoangvane@email.com | [@hoangvane](#) |

### Giảng Viên Hướng Dẫn
**TS. Nguyễn Văn X**  
Khoa Công Nghệ Thông Tin  
Email: nguyenvanx@university.edu.vn

---

## 📞 Liên Hệ & Hỗ Trợ

- **Email nhóm**: nhom6.dh24th2@email.com
- **Hotline**: 0123-456-789
- **Issues**: [GitHub Issues](https://github.com/your-username/QuanLyKhachSan_Python/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/QuanLyKhachSan_Python/discussions)

---

## 📝 Changelog

### Version 1.0.0 (2025-01-15)
- ✨ Ra mắt phiên bản đầu tiên
- ✅ Hoàn thiện các tính năng cơ bản
- 🎨 Thiết kế giao diện hoàn chỉnh
- 📚 Hoàn thiện tài liệu hướng dẫn

### Version 0.9.0 (2024-12-20)
- 🚀 Beta testing
- 🐛 Sửa các lỗi phát hiện
- 📊 Thêm chức năng báo cáo

### Version 0.5.0 (2024-11-15)
- 🎯 Hoàn thành prototype
- 💾 Thiết kế database
- 🔧 Xây dựng các module cơ bản

---

## 🎓 Học Hỏi Thêm

### Tài Nguyên Học Tập

- 📖 [Python Documentation](https://docs.python.org/3/)
- 📖 [Tkinter Tutorial](https://docs.python.org/3/library/tkinter.html)
- 📖 [SQLite Documentation](https://www.sqlite.org/docs.html)
- 🎥 [Video Tutorial Python GUI](https://www.youtube.com)
- 📚 [Clean Code in Python](https://realpython.com)

---

## ⚖️ Giấy Phép

Dự án này được phân phối dưới giấy phép **MIT License**.

```
MIT License

Copyright (c) 2025 Nhóm 6 - DH24TH2

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🌟 Lời Cảm Ơn

Chúng em xin chân thành cảm ơn:

- **Thầy/Cô giảng viên** đã tận tình hướng dẫn
- **Gia đình và bạn bè** đã động viên, ủng hộ
- **Cộng đồng Python Việt Nam** đã chia sẻ kiến thức
- **Tất cả những người** đã đóng góp ý kiến cho dự án

---

<div align="center">

### 💖 Làm với tình yêu bởi Nhóm 6 💖

**⭐ Nếu bạn thấy dự án hữu ích, hãy cho chúng tôi một ngôi sao! ⭐**

[⬆ Về đầu trang](#-hệ-thống-quản-lý-khách-sạn)

</div>

---

**📅 Cập nhật lần cuối: 08/10/2025**  
**📍 Phiên bản: 1.0.0**  
**🏫 Trường:]Đại Học An Giang**