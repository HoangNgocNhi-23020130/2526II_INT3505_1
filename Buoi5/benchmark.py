import time
from server import create_app
from core.database import db
from models.books import Book

def benchmark_pagination():
    app = create_app()
    with app.app_context():
        limit = 100
        page = 9000 # Test ở trang rất sâu (bỏ qua 899,900 bản ghi)
        offset = (page - 1) * limit
        cursor_id = offset # Giả lập ID cuối cùng của trang 8999

        print(f"--- ĐANG TEST PHÂN TRANG VỚI OFFSET = {offset} ---")

        # ---------------------------------------------------------
        # Phương án 1: Offset/Limit truyền thống
        # ---------------------------------------------------------
        start = time.time()
        books_p1 = Book.query.order_by(Book.id).offset(offset).limit(limit).all()
        time_p1 = (time.time() - start) * 1000
        print(f"1. Offset/Limit truyền thống : {time_p1:.2f} ms")


        # ---------------------------------------------------------
        # Phương án 2: PAGE-BASED Pagination
        # ---------------------------------------------------------
        start = time.time()
        # Sử dụng paginate() của SQLAlchemy
        pagination = Book.query.order_by(Book.id).paginate(page=page, per_page=limit, error_out=False)
        books_p2 = pagination.items
        time_p2 = (time.time() - start) * 1000
        print(f"2. PAGE-BASED Pagination  : {time_p2:.2f} ms")


        # ---------------------------------------------------------
        # Phương án 3: Cursor-based Pagination
        # ---------------------------------------------------------
        start = time.time()
        books_p3 = Book.query.filter(Book.id > cursor_id).order_by(Book.id).limit(limit).all()
        time_p3 = (time.time() - start) * 1000
        print(f"3. Cursor-based Pagination    : {time_p3:.2f} ms")
        
if __name__ == '__main__':
    benchmark_pagination()