const express = require('express');
const app = express();

// Cổng lắng nghe
const PORT = 1604;

// Hỗ trợ phiên dịch
app.use(express.json());

// Database
let books = [];

// Khởi động server
app.listen(PORT, () => {
    console.log(`Server đang chạy tại http://localhost:${PORT}`);
});