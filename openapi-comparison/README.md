# Hướng dẫn Chạy Demo: 1 Server Trung Tâm cho 4 API Specifications

## Yêu cầu chuẩn bị
- Máy tính đã cài đặt sẵn **Node.js** và **npm**.

## Bước 1: Khởi động Mock Server Trung Tâm

Sử dụng file `openapi.yaml` làm chuẩn để tạo ra Server giả lập thông qua thư viện **Prism**.

1. Mở Terminal / Command Prompt tại thư mục của dự án.
2. Di chuyển vào thư mục chứa file OpenAPI:
   ```bash
   cd OpenAPI
   ```
3. Chạy lệnh khởi tạo Mock Server:
    ```bash
    npx @stoplight/prism-cli mock openapi.yaml
    ```
5. Terminal sẽ thông báo Server đang chạy thành công tại địa chỉ: [Mock Server](http://127.0.0.1:4010).
(Lưu ý: Giữ nguyên cửa sổ Terminal này trong suốt quá trình test).
6. Thực hiện demo với mỗi Spec theo hướng dẫn cụ thể ở mỗi thư mục.