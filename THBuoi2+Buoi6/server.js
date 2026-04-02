require('dotenv').config();
const express = require('express');
const jwt = require('jsonwebtoken');
const { v4: uuidv4 } = require('uuid');

const app = express();
app.use(express.json());

// Database
const usersDb = {
    "Nguyen Van A": { password: "123", role: "Admin" },
    "Tran Thi B": { password: "hihi", role: "Reader" },
    "Hoang Ngoc Nhi": { password: "0810", role: "Admin" }
};

const booksDb = [
    { id: 1, title: "De Men Phieu Luu Ky", author: "To Hoai" },
    { id: 2, title: "Luoc Su Thoi Gian", author: "Stephen Hawking" },
    { id: 3, title: "Khong Gia Dinh", author: "Hector Malot" },
    { id: 4, title: "Dat Rung Phuong Nam", author: "To Hoai" }
];

// Chuẩn hóa response
const libRes = (res, status, data = null, message = null, code = 200) => {
    return res.status(code).json({ status, data, message });
};

// Xác Thực & Phân Quyền
const requireJwt = (requiredRole = null) => {
    return (req, res, next) => {
        const authHeader = req.headers['authorization'];
        // Lấy token từ chuỗi "Bearer <token>"
        const token = authHeader && authHeader.split(' ')[1];
        if (!token) {
            return libRes(res, 'error', null, 'Missing Access Token!', 401);
        }

        jwt.verify(token, process.env.ACCESS_TOKEN_SECRET, (err, decoded) => {
            if (err) {
                const message = err.name === 'TokenExpiredError' 
                    ? 'Access Token expired!' 
                    : 'Invalid Token!';
                return libRes(res, 'error', null, message, 401);
            }

            // Kiểm tra phân quyền (Role)
            if (requiredRole && decoded.role !== requiredRole) {
                return libRes(res, 'error', null, 'Permission denied: Admin required!', 403);
            }

            // Gắn thông tin user vào request
            req.user = decoded;
            next(); // Cho phép đi tiếp vào route controller
        });
    };
};

// 1. Login (Cấp phát Access & Refresh Token)
app.post('/api/auth/login', (req, res) => {
    const { username, password } = req.body;

    if (!username || !password) {
        return libRes(res, 'error', null, 'Username and password are required', 400);
    }

    const user = usersDb[username];
    if (!user || user.password !== password) {
        return libRes(res, 'error', null, 'Invalid credentials', 401);
    }

    // Payload cho Access Token (Sống 15 phút)
    const accessPayload = {
        jti: uuidv4(),
        sub: username,
        role: user.role
    };
    const accessToken = jwt.sign(accessPayload, process.env.ACCESS_TOKEN_SECRET, { expiresIn: '15m' });

    // Payload cho Refresh Token (Sống 7 ngày, không chứa role)
    const refreshPayload = {
        jti: uuidv4(),
        sub: username
    };
    const refreshToken = jwt.sign(refreshPayload, process.env.REFRESH_TOKEN_SECRET, { expiresIn: '7d' });

    return libRes(res, 'success', {
        access_token: accessToken,
        refresh_token: refreshToken,
        user: { username, role: user.role }
    }, 'Login successful', 200);
});

// 2. Refresh Token (Lấy Access Token mới)
app.post('/api/auth/refresh', (req, res) => {
    const { refresh_token } = req.body;

    if (!refresh_token) {
        return libRes(res, 'error', null, 'Refresh token is required', 400);
    }

    jwt.verify(refresh_token, process.env.REFRESH_TOKEN_SECRET, (err, decoded) => {
        if (err) {
            const message = err.name === 'TokenExpiredError' 
                ? 'Refresh token expired. Please login again.' 
                : 'Invalid refresh token.';
            return libRes(res, 'error', null, message, 401);
        }

        const username = decoded.sub;
        const user = usersDb[username];
        
        if (!user) {
            return libRes(res, 'error', null, 'User no longer exists.', 401);
        }

        // Cấp lại Access Token mới
        const newAccessPayload = {
            jti: uuidv4(),
            sub: username,
            role: user.role
        };
        const newAccessToken = jwt.sign(newAccessPayload, process.env.ACCESS_TOKEN_SECRET, { expiresIn: '15m' });

        return libRes(res, 'success', { access_token: newAccessToken }, 'Token refreshed', 200);
    });
});

// 3. Lấy danh sách sách (Public)
app.get('/api/books', (req, res) => {
    return libRes(res, 'success', booksDb);
});

// 4. Thêm sách mới (Chỉ Admin)
app.post('/api/books', requireJwt('Admin'), (req, res) => {
    // req.user chứa thông tin người đang thao tác
    const { title, author } = req.body;

    if (!title || !author) {
        return libRes(res, 'error', null, 'Need title and author!', 400);
    }

    const newBook = {
        id: booksDb.length + 1,
        title,
        author
    };
    booksDb.push(newBook);

    return libRes(res, 'success', newBook, 'Book added successfully!', 201);
});

// Start Server
const PORT = process.env.PORT || 1604;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});