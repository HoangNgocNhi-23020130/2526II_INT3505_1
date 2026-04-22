# Thông báo: Kế hoạch ngừng hỗ trợ (Deprecation) đối với Payment version 1
Kính gửi Quý Nhà phát triển,

Nhằm đáp ứng nhu cầu thanh toán quốc tế đa tiền tệ, chúng tôi xin thông báo Payment version 1 (/api/v1/payments) sẽ chính thức bước vào giai đoạn ngừng hỗ trợ (deprecated) kể từ hôm nay và sẽ ngừng hoạt động hoàn toàn (sunset) vào ngày 8 tháng 10 năm 2026.

Lộ trình chuyển đổi dành cho bạn (Migration Path): Để đảm bảo các tích hợp của bạn không bị gián đoạn, vui lòng lập kế hoạch chuyển đổi sang Version 2 (/api/v2/payments). Thay đổi duy nhất là bạn cần bổ sung trường currency (ví dụ: "VND", "USD") vào payload của phương thức POST.

Bạn có thể xem chi tiết hướng dẫn tích hợp tại: [Đường dẫn tài liệu hướng dẫn chuyển đổi].

Các thay đổi kỹ thuật có hiệu lực ngay lập tức: Để giúp bạn dễ dàng theo dõi, chúng tôi đã áp dụng các cảnh báo tự động trên hệ thống:
- Tài liệu OpenAPI: Các endpoint chuẩn bị ngừng hỗ trợ đã được đánh dấu cờ deprecated: true trên tài liệu tham khảo API
- HTTP Headers: Chúng tôi đã thêm Sunset HTTP header vào các phản hồi (response) của API cũ. Bạn có thể sử dụng header này để thiết lập cảnh báo tự động trong hệ thống của mình về thời điểm API chính thức bị vô hiệu hóa
- Helper Libraries: Nếu bạn đang sử dụng các thư viện hỗ trợ (SDK) của chúng tôi, các thông báo cảnh báo (warnings) sẽ bắt đầu xuất hiện trong tệp log hoặc bảng điều khiển (console) của ứng dụng

Nếu bạn có bất kỳ câu hỏi nào hoặc cần hỗ trợ trong quá trình chuyển đổi, xin đừng ngần ngại liên hệ trực tiếp với chúng tôi.

Trân trọng,
Đội ngũ phát triển API