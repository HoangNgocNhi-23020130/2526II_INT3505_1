# Kết quả Kiểm thử API (Newman Report)

## 1. Chi tiết các Endpoint
Test API

→ Get Books
  GET http://127.0.0.1:1604/api/books [200 OK, 685B, 40ms]
  √  Status code là 200
  √  Cấu trúc phản hồi đúng chuẩn success

→ Get a book
  GET http://127.0.0.1:1604/api/books/1 [200 OK, 317B, 9ms]
  √  Lấy đúng sách đã tạo

→ Post new book
  POST http://127.0.0.1:1604/api/books [201 CREATED, 307B, 11ms]
  √  Tạo thành công - Status 201
  √  Thông điệp trả về đúng

→ Put book
  PUT http://127.0.0.1:1604/api/books/3 [200 OK, 313B, 14ms]
  √  Cập nhật thành công

→ Delete Book
  DELETE http://127.0.0.1:1604/api/books/1 [200 OK, 232B, 10ms]
  √  Xóa thành công

## 2. Bảng thống kê tổng quát
| | executed | failed |
| :--- | :---: | :---: |
| **iterations** | 1 | 0 |
| **requests** | 5 | 0 |
| **test-scripts** | 5 | 0 |
| **prerequest-scripts** | 0 | 0 |
| **assertions** | 7 | 0 |

- **total run duration:** 550ms
- **total data received:** 1.02kB (approx)
- **average response time:** 16ms [min: 9ms, max: 40ms, s.d.: 11ms]