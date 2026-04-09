import time
from faker import Faker
from server import create_app
from core.database import db
from models.books import Book

fake = Faker()

def seed_million_books():
    # 1. Khởi tạo app để lấy context kết nối database
    app = create_app()
    with app.app_context():
        # Xóa sạch dữ liệu cũ trong bảng books để tạo mới
        print("Đang dọn dẹp dữ liệu cũ...")
        db.session.query(Book).delete()
        db.session.commit()

        print("Bắt đầu tạo 1.000.000 bản ghi sách...")
        start_time = time.time()

        # 2. Thiết lập thông số chia lô (Batch processing)
        chunk_size = 10000  # Mỗi lần lưu 10 ngàn dòng
        total_records = 1000000

        # 3. Chạy vòng lặp tạo dữ liệu
        for i in range(0, total_records, chunk_size):
            books_data = []
            for j in range(chunk_size):
                # Tính toán số thứ tự tuyệt đối của bản ghi
                current_index = i + j + 1
                
                books_data.append({
                    # Nối chuỗi "978-" với số thứ tự được thêm số 0 ở đầu cho đủ độ dài
                    "isbn": f"978-{str(current_index).zfill(10)}", 
                    "title": fake.catch_phrase(),
                    "author": fake.name(),
                    "total_copies": fake.random_int(min=10, max=50),
                    "available_copies": fake.random_int(min=0, max=10)
                })
            
            # Sử dụng bulk_insert_mappings (Chèn hàng loạt siêu tốc của SQLAlchemy)
            db.session.bulk_insert_mappings(Book, books_data)
            db.session.commit()
            
            print(f"Đã chèn {i + chunk_size:,} / {total_records:,} bản ghi...")

        end_time = time.time()
        print(f"\nHoàn thành! Tổng thời gian: {round(end_time - start_time, 2)} giây.")

if __name__ == '__main__':
    seed_million_books()