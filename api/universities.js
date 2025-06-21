const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// 创建数据库连接
function getDatabase() {
    const dbPath = path.join(process.cwd(), 'database', 'rankings.db');
    return new sqlite3.Database(dbPath);
}

// 初始化数据库
function initDatabase() {
    return new Promise((resolve, reject) => {
        const db = getDatabase();
        
        db.run(`CREATE TABLE IF NOT EXISTS universities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rank INTEGER,
            university TEXT NOT NULL,
            country TEXT,
            research REAL DEFAULT 0,
            reputation REAL DEFAULT 0,
            employment REAL DEFAULT 0,
            international REAL DEFAULT 0,
            total_score REAL DEFAULT 0,
            star_rating TEXT,
            year INTEGER DEFAULT 2024
        )`, (err) => {
            if (err) {
                reject(err);
            } else {
                // 检查是否有数据，如果没有则插入示例数据
                db.get("SELECT COUNT(*) as count FROM universities", (err, row) => {
                    if (err) {
                        reject(err);
                    } else if (row.count === 0) {
                        // 插入示例数据
                        const sampleData = [
                            [1, 'Massachusetts Institute of Technology', 'United States', 100, 99.73, 100, 96.675, 99.6, '★★★★★', 2025],
                            [2, 'Harvard University', 'United States', 100, 97.88, 100, 99.9, 99.46, '★★★★★', 2025],
                            [3, 'University of Oxford', 'United Kingdom', 100, 98.16, 100, 97.7, 99.31, '★★★★★', 2025],
                            [4, 'Stanford University', 'United States', 100, 97.5, 100, 95.8, 99.2, '★★★★★', 2025],
                            [5, 'University of Cambridge', 'United Kingdom', 100, 97.2, 100, 96.5, 99.1, '★★★★★', 2025]
                        ];
                        
                        const stmt = db.prepare("INSERT INTO universities (rank, university, country, research, reputation, employment, international, total_score, star_rating, year) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");
                        
                        sampleData.forEach(row => {
                            stmt.run(row);
                        });
                        
                        stmt.finalize(() => {
                            resolve();
                        });
                    } else {
                        resolve();
                    }
                });
            }
        });
    });
}

// 获取大学数据
function getUniversities(query) {
    return new Promise((resolve, reject) => {
        const db = getDatabase();
        
        let sql = "SELECT * FROM universities WHERE 1=1";
        const params = [];
        
        // 添加筛选条件
        if (query.country) {
            sql += " AND country = ?";
            params.push(query.country);
        }
        
        if (query.year) {
            sql += " AND year = ?";
            params.push(query.year);
        }
        
        if (query.search) {
            sql += " AND (university LIKE ? OR country LIKE ?)";
            const searchTerm = `%${query.search}%`;
            params.push(searchTerm, searchTerm);
        }
        
        // 排序
        const sortBy = query.sortBy || 'rank';
        const sortOrder = query.sortOrder || 'ASC';
        sql += ` ORDER BY ${sortBy} ${sortOrder}`;
        
        // 分页
        const limit = parseInt(query.limit) || 20;
        const page = parseInt(query.page) || 1;
        const offset = (page - 1) * limit;
        sql += ` LIMIT ? OFFSET ?`;
        params.push(limit, offset);
        
        db.all(sql, params, (err, rows) => {
            if (err) {
                reject(err);
            } else {
                // 获取总数
                let countSql = "SELECT COUNT(*) as total FROM universities WHERE 1=1";
                const countParams = [];
                
                if (query.country) {
                    countSql += " AND country = ?";
                    countParams.push(query.country);
                }
                
                if (query.year) {
                    countSql += " AND year = ?";
                    countParams.push(query.year);
                }
                
                if (query.search) {
                    countSql += " AND (university LIKE ? OR country LIKE ?)";
                    const searchTerm = `%${query.search}%`;
                    countParams.push(searchTerm, searchTerm);
                }
                
                db.get(countSql, countParams, (err, countRow) => {
                    if (err) {
                        reject(err);
                    } else {
                        const total = countRow.total;
                        const totalPages = Math.ceil(total / limit);
                        
                        resolve({
                            universities: rows,
                            pagination: {
                                page,
                                limit,
                                total,
                                totalPages
                            }
                        });
                    }
                });
            }
        });
    });
}

// Vercel API处理函数
module.exports = async (req, res) => {
    // 设置CORS头
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    
    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }
    
    try {
        // 初始化数据库
        await initDatabase();
        
        // 获取查询参数
        const query = req.query;
        
        // 获取数据
        const result = await getUniversities(query);
        
        res.status(200).json(result);
    } catch (error) {
        console.error('API Error:', error);
        res.status(500).json({ error: 'Internal Server Error', details: error.message });
    }
}; 