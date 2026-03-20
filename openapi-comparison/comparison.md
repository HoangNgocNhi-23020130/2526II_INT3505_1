# I. Tổng quan về từng chuẩn API

## 1. OpenAPI (Trước đây là Swagger)
* Ban đầu là Swagger Specification, sau này thuộc quyền Linux Foundation và đổi tên thành OenAPI Initiative (OAI).
* **Định dạng:** YAML hoặc JSON.
* **Đặc điểm nổi bật:** Rất chi tiết, chặt chẽ và mô tả được mọi khía cạnh của API (từ tham số, đường dẫn, đến cấu trúc bảo mật). Đây là chuẩn công nghiệp được sử dụng rộng rãi nhất.
* **Hệ sinh thái (Tooling)**: Vô cùng khổng lồ, có thể dễ dàng tìm thấy các công cụ tự động sinh giao diện tài liệu (Swagger UI, Redoc), sinh code Frontend/Backend (OpenAPI Generator), hoặc tạo Mock Server (Prism).
* **Nhược điểm:** Cú pháp khá dài dòng (verbose). Khi dự án mở rộng ra hàng trăm endpoint, file cấu hình YAML có thể lên tới hàng ngàn dòng và rất khó để tái sử dụng code linh hoạt.

## 2. RAML (RESTful API Modeling Language)
* Phổ biến trong hệ sinh thái cửa MuleSoft (nay thuộc Salesforce).
* **Định dạng:** YAML.
* **Đặc điểm nổi bật:** Thiết kế theo hướng phân cấp (Top-down) trực quan. Điểm nổi bật nằm ở khả năng **tái sử dụng (Reusability)** thông qua các tính năng như `traits`, `resourceTypes`, giúp giảm thiểu việc lặp lại code.
* **Nhược điểm:** Hệ sinh thái bị bó hẹp khá nhiều vào các sản phẩm thương mại của MuleSoft (như Anypoint Platform). Ít công cụ mã nguồn mở (open-source) hỗ trợ hơn so với OpenAPI.

## 3. API Blueprint
* Được phát triển bởi Apiary (hiện thuộc Oracle).
* **Định dạng:** Markdown.
* **Đặc điểm nổi bật:** Thân thiện nhất với con người do viết bằng Markdown, giống như soạn một file tài liệu hướng dẫn thông thường. Những người không chuyên về code (như Product Manager, QA) vẫn có thể đọc hiểu và chỉnh sửa dễ dàng.
* **Nhược điểm:** Định dạng Markdown tuy dễ đọc nhưng lại khó để máy tính phân tích (parse) tự động hóa. Hiện tại, cộng đồng và các công cụ hỗ trợ cho API Blueprint đang có dấu hiệu đi xuống và ít được cập nhật.

## 4. TypeSpec
* Được phát triển bởi Microsoft, giải quyết bài toán thiết kế API ở quy mô siêu lớn.
* **Định dạng:** Cú pháp riêng giống TypeScript và C#.
* **Đặc điểm nổi bật:** Tiếp cận API như một **ngôn ngữ lập trình**, hỗ trợ các tính năng của Lập trình hướng đối tượng (OOP) như extends, namespaces, và module hóa. Đặc biệt là trình biên dịch của TypeSpec có thể tự động "dịch" mã .tsp sang OpenAPI 3.0, JSON Schema hoặc gRPC.
* **Nhược điểm:** Cần có tư duy lập trình viên (đặc biệt là quen thuộc với TypeScript) mới có thể viết tốt. Vì còn khá mới, hệ sinh thái vẫn đang trong giai đoạn phát triển, nên chưa thuận tiện.

# II. Bảng So Sánh Trực Quan

| Tiêu chí | OpenAPI 3.x | RAML 1.0 | API Blueprint | TypeSpec |
| :--- | :--- | :--- | :--- | :--- |
| **Cú pháp (Format)** | YAML / JSON | YAML | Markdown | Giống TypeScript |
| **Độ phổ biến (Thị phần)** | Rất cao (Tiêu chuẩn nghành) | Trung bình (chủ yếu trong hệ sinh thái của MuleSoft / Salesforce.) | Thấp (Đang giảm dần) | Mới nổi |
| **Khả năng tái sử dụng code**| Trung bình | Rất tốt (`traits`) | Kém | Xuất sắc (OOP, Modules) |
| **Hệ sinh thái Tooling** | Khổng lồ (Swagger, Redoc...) | Phụ thuộc MuleSoft | Phụ thuộc Apiary | Đang phát triển (Microsoft) |
| **Phù hợp nhất** | Mọi dự án từ nhỏ đến lớn. Cần sinh code tự động. | Các hệ thống Enterprise lớn, dùng MuleSoft. | Ưu tiên tài liệu dễ đọc cho cả người không biết code. | Dự án siêu lớn. |

## III. Tổng Kết
1. **OpenAPI** vẫn là sự lựa chọn số hàng đầu cho hầu hết các dự án hiện nay nhờ cộng đồng quá lớn mạnh.
2. Nếu dự án đòi hỏi thiết kế hàng nghìn API phức tạp, **TypeSpec** là một giải pháp thay thế hoàn hảo để quản lý source code API gọn gàng hơn, sau đó compile ngược lại ra OpenAPI để tận dụng hệ sinh thái Tooling.