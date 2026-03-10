#   Smart File Organizer (Python & SQLite)
Dự án tự động phân loại và dọn dẹp thư mục, tích hợp lưu trữ vào lịch sử thay đổi vào file database để người dùng có thể theo dõi

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

---
## Tính năng
- **Tự động phân loại:** Nhận diện đuôi file (PDF, DOCX, JPG, PNG, ZIP,...) để đưa vào các thư mục tương ứng.

- **Quản lý lịch sử:** Sử dụng **SQLite** để ghi lại nhật kí di chuyển (id, tên file, đường dẫn cũ, đường dẫn mới, thời gian).

- **Thông báo lỗi:** Sử dụng `try-except` để tránh crash khi file đang bị khóa hoặc không có quyền truy cập.

- **Phù hợp đa nền tảng:** Sử dụng `os.path.join` để hoạt động ổn định trên cả Windows và Linux.

## Công nghệ sử dụng
- **Ngôn ngữ:** Python
- **Thư viện chuẩn:** `os`, `shutil`, `sqlite3`
- **Cơ sở dữ liệu:** SQLite3

## Cách sử dụng
1. Đảm bảo đã cài đặt python
2. Tải file `organier.py`
3. Chạy chương trình bằng lệnh:
    ```bash
    python organizer.py
4. Nhập path thư mục cần sắp xếp

## Cấu trúc sau sắp xếp
```
Thư mục gốc/
├── Documents/
│   ├── PDF/
│   └── Word/
├── Images/
├── Archives/
└── history.db (File dữ liệu lịch sử)