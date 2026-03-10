import os
import shutil  # Thư viện di chuyển file
import sqlite3 # Thư viện làm việc với Cơ sở dữ liệu
from datetime import datetime

# 1. BẢN ĐỒ PHÂN LOẠI FILE
EXTENSION_MAP = {
    '.pdf': 'Documents/PDF',
    '.docx': 'Documents/Word',
    '.jpg': 'Images',
    '.png': 'Images',
    '.zip': 'Archives',
    '.rar': 'Archives',
    '.mp4': 'Videos',
    '.mp3': 'Music',
    '.exe': 'Applications',
    '.sql': 'Documents/SQL',
    '.html': 'Documents/HTML',
}

# 2. KHỞI TẠO CƠ SỞ DỮ LIỆU
def prepare_db():
    connect_sql = sqlite3.connect('history.db') #Kết nối với file database (nếu chưa có sẽ tự tạo)
    cursor = connect_sql.cursor()   #Tạo ra con trỏ để thực thi các câu lệnh SQL
    # Tạo bảng history nếu chưa tồn tại
    cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        filename TEXT,
                        original_path TEXT,
                        new_path TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')
    connect_sql.commit() # Lưu thay đổi cấu trúc bảng
    connect_sql.close()

# 3. HÀM GHI LOG VÀO DATABASE
def log_movement(filename, original_path, new_path):
    try:
        connect_sql = sqlite3.connect('history.db')
        cursor = connect_sql.cursor()
        cursor.execute('''INSERT INTO history (filename, original_path, new_path) 
                          VALUES (?, ?, ?)''', (filename, original_path, new_path))
        connect_sql.commit()
        connect_sql.close()
    except Exception as e:
        print(f"Lỗi ghi log vào Database: {e}")

# 4. HÀM XỬ LÝ DỌN DẸP THƯ MỤC
def organize_folder(path):
    # Kiểm tra đường dẫn có tồn tại không
    if not os.path.exists(path):
        print(f"Đường dẫn {path} không tồn tại.")
        return

    print(f"--- Bắt đầu dọn dẹp thư mục: {path} ---")

    for filename in os.listdir(path):
        original_path = os.path.join(path, filename)

        # Chỉ xử lý nếu là FILE (bỏ qua các thư mục con đã dọn dẹp trước đó)
        if os.path.isfile(original_path):
            name, ext = os.path.splitext(filename)
            ext = ext.lower() 

            # Kiểm tra xem đuôi file có trong danh sách phân loại không
            if ext in EXTENSION_MAP:
                # Xây dựng đường dẫn thư mục đích và đường dẫn file mới
                destination_folder = os.path.join(path, EXTENSION_MAP[ext])
                new_path = os.path.join(destination_folder, filename)

                # Tạo thư mục đích nếu chưa có
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)
                    print(f"Đã tạo thư mục: {destination_folder}")

                try:
                    # Di chuyển file
                    shutil.move(original_path, new_path)
                    print(f"Thành công: {filename} -> {EXTENSION_MAP[ext]}")
                    
                    # Ghi lại lịch sử vào CSDL
                    log_movement(filename, original_path, new_path)
                except PermissionError:
                    print(f"Lỗi: File {filename} đang được sử dụng bởi chương trình khác.")
                except Exception as e:
                    print(f"Lỗi khi di chuyển {filename}: {e}")
            else:
                # Nếu không có quy tắc phân loại cho đuôi file này
                print(f"Bỏ qua: {filename} (Không có quy tắc cho đuôi {ext})")
        else:
            print(f"Bỏ qua: {filename} (Không phải là file)")

# 5. HÀM HIỂN THỊ LỊCH SỬ TỪ DATABASE
def show_history():
    print("\n--- LỊCH SỬ DI CHUYỂN FILE (TRONG DATABASE) ---")
    try:
        connect_sql = sqlite3.connect('history.db')
        cursor = connect_sql.cursor()
        cursor.execute('''SELECT id, filename, original_path, new_path, timestamp FROM history ORDER BY id DESC''')
        records = cursor.fetchall()
        
        if not records:
            print("Chưa có lịch sử nào được lưu.")
        else:
            for record in records:
                print(f"ID: {record[0]} | File: {record[1]} | Từ: {row_path_shorten(record[2])} | Đến: {row_path_shorten(record[3])} | Lúc: {record[4]}")
        
        connect_sql.close()
    except Exception as e:
        print(f"Lỗi truy vấn Database: {e}")

def row_path_shorten(path):
    # Hàm phụ để thu gọn đường dẫn khi in ra cho đẹp
    return "..." + path[-50:] if len(path) > 50 else path

# --- CHƯƠNG TRÌNH CHÍNH ---
if __name__ == "__main__":
    prepare_db()
    target_path = input("Nhập đường dẫn thư mục bạn muốn dọn dẹp (VD: C:\\Users\\HOA08\\Downloads): ")
    organize_folder(target_path)
    show_history()