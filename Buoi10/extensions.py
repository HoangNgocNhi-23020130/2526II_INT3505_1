from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from prometheus_flask_exporter import PrometheusMetrics

# Khởi tạo Limiter
# get_remote_address: Lấy IP của người dùng để làm mốc đếm request
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"], # Giới hạn mặc định cho mọi endpoint
    storage_uri="memory://" # Lưu trữ tạm trên RAM (production thực tế hay dùng redis://)
)

# Khởi tạo Prometheus
metrics = PrometheusMetrics.for_app_factory(path=None)