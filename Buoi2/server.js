const express = require('express');
const fs = require('fs');
const app = express();

// Cổng lắng nghe
const PORT = 1604;

// Hỗ trợ phiên dịch
app.use(express.json());

const FILE_PATH = './database.json';
// Đọc dữ liệu
const readData = () => {
    try {
        const data = fs.readFileSync(FILE_PATH, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        return []; // Nếu file chưa tồn tại, trả về mảng rỗng
    }
};

// Ghi dữ liệu
const writeData = (data) => {
    // Format file JSON thụt lề cho đẹp, dễ đọc
    fs.writeFileSync(FILE_PATH, JSON.stringify(data, null, 2));
};

// POST: thêm sách
app.post('/api/books', async (req, res) => {
    try {
        // Lấy dữ liệu từ client gửi lên
        const { title, author, published_year } = req.body;

        // Thông tin tên sách và tác giả là bắt buộc
        if (!title || !author) {
            return res.status(400).json({ message: "Vui lòng cung cấp đủ Tên sách và Tác giả!" });
        }

        let books = await readData();

        // Check trùng lặp
        const isDuplicate = books.some(b => b.title === title && b.author === author);
        
        if (isDuplicate) {
            // Lỗi 409 Conflict
            return res.status(409).json({ message: "Sách này đã tồn tại trong kho!" });
        }

        const newBook = {
            id: Date.now().toString(), // Lấy id theo thời gian thực post lên
            title: title,
            author: author,
            published_year: published_year,
            status: "Có sẵn"
        };
        
        books.push(newBook);
        writeData(books);
        
        // Trả về thành công (201 Created)
        res.status(201).json({ message: "Thêm sách thành công", data: newBook });

    } catch (error) {
        // Bắt lỗi và trả về lỗi 500 (Internal Server Error)
        console.error("Lỗi khi thêm sách:", error);
        res.status(500).json({ message: "Đã xảy ra lỗi trên Server", error: error.message });
    }
});

// GET: Lấy danh sách toàn bộ sách
app.get('/api/books', async (req, res) => {
    try {
        let books = await readData();
        res.status(200).json({
            message: "Lấy danh sách thành công",
            total: books.length,
            data: books
        });
    } catch (error) {
        console.error("Lỗi khi GET:", error);
        res.status(500).json({ message: "Đã xảy ra lỗi trên Server", error: error.message });
    }
});

// PUT: Ghi đè toàn bộ thông tin của cuốn sách
app.put('/api/books/:id', async (req, res) => {
    try {
        let books = await readData();
        const bookId = req.params.id;
        const index = books.findIndex(b => b.id === bookId);
        
        if (index === -1) {
            return res.status(404).json({ message: "Không tìm thấy sách để cập nhật" });
        }

        // Lấy dữ liệu mới từ body để đè lên
        const { title, author, published_year, status } = req.body;
        
        books[index] = {
            id: bookId, // Giữ nguyên ID gốc
            title: title,
            author: author,
            published_year: published_year,
            status: status
        };
        writeData(books);

        res.status(200).json({ message: "Cập nhật toàn bộ thông tin thành công", data: books[index] });
    } catch (error) {
        console.error("Lỗi khi PUT:", error);
        res.status(500).json({ message: "Đã xảy ra lỗi trên Server", error: error.message });
    }
});

// PATCH: Đổi trạng thái sang "Đã mượn"
app.patch('/api/books/:id', async (req, res) => {
    try {
        let books = await readData();
        const bookId = req.params.id;
        const book = books.find(b => b.id === bookId);

        if (!book) {
            return res.status(404).json({ message: "Không tìm thấy sách" });
        }

        book.status = "Đã mượn";

        writeData(books);

        res.status(200).json({ message: "Cập nhật trạng thái sách thành công", data: book });
    } catch (error) {
        console.error("Lỗi khi PATCH:", error);
        res.status(500).json({ message: "Đã xảy ra lỗi trên Server", error: error.message });
    }
});

// DELETE: Rút một cuốn sách khỏi thư viện
app.delete('/api/books/:id', async (req, res) => {
    try {
        let books = await readData();
        const bookId = req.params.id;
        const initialLength = books.length;
        
        books = books.filter(b => b.id !== bookId);

        if (books.length === initialLength) {
            return res.status(404).json({ message: "Không tìm thấy sách để xóa" });
        }
        writeData(books);

        res.status(204).send(); // Xóa thành công, không trả về dữ liệu (No Content)
    } catch (error) {
        console.error("Lỗi khi DELETE:", error);
        res.status(500).json({ message: "Đã xảy ra lỗi trên Server", error: error.message });
    }
});

// Khởi động server
app.listen(PORT, () => {
    console.log(`Server đang chạy tại http://localhost:${PORT}`);
});