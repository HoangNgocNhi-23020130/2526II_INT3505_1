# Phân tích API Design Patterns của Stripe và GitHub

Trong quá trình xây dựng hệ thống demo, chúng ta đã áp dụng và mô phỏng các API Patterns từ các hệ thống lớn như Stripe và GitHub.

## 1. Stripe API Patterns (Áp dụng trong hệ thống demo)

Stripe là chuẩn mực của việc thiết kế Webhook bảo mật và API rành mạch:

- **Webhook Signature (Chữ ký HMAC):** Stripe sử dụng header `Stripe-Signature` chứa timestamp (`t=...`) và mã băm HMAC (`v1=...`) để xác thực tính toàn vẹn. Trong demo, chúng ta đã implement hệ thống bảo mật tương tự với header `X-Webhook-Signature`.
- **Chống Replay Attack:** Bằng cách kết hợp `timestamp` vào payload ký HMAC, bên nhận Webhook (Notification System) có thể tính toán thời gian và từ chối các request cũ (ví dụ quá 5 phút), chặn hacker lấy lại request cũ gửi liên tục. Trong code demo, Notification System có kiểm tra `int(time.time()) - int(timestamp) > 300`.
- **Phản hồi chuẩn hóa:** Sử dụng HTTP Status code rõ ràng và trả về object dạng `{"status": ..., "data": ...}`.
- **Idempotency (Tính luỹ đẳng):** (Kiến thức mở rộng) Stripe cho phép truyền `Idempotency-Key` ở Header để tránh bị charge tiền hai lần khi mạng lỗi. 

## 2. GitHub API Patterns

GitHub nổi tiếng với thiết kế RESTful chuẩn xác và HATEOAS:

- **HATEOAS và Pagination:** GitHub trả về link phân trang trực tiếp trong HTTP Header `Link` hoặc bên trong JSON Response (như `next`, `prev` links) giúp client không cần tự nối chuỗi URL. Trong code demo, danh sách `/products` trả về thuộc tính `links` chứa điều hướng `self`, `create`, `update`, v.v.
- **Event-Driven qua Webhooks:** GitHub cho phép repository đăng ký webhook với rất nhiều loại event (`push`, `pull_request`). Khi có sự kiện, nó gửi HTTP POST kèm signature `X-Hub-Signature-256`. Hệ thống đăng ký Webhook trong demo của chúng ta đang bắt chước flow này qua thuộc tính `event_types`.
- **Throttling/Rate Limiting:** GitHub trả về các header `X-RateLimit-Limit`, `X-RateLimit-Remaining` để thông báo cho người dùng biết mức độ sử dụng API.
