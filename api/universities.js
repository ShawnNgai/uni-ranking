// 使用SQLite数据库获取完整大学数据
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// 数据库路径
const dbPath = path.join(__dirname, '../database/rankings.db');

// 获取大学数据
function getUniversities(query) {
    return new Promise((resolve, reject) => {
        const db = new sqlite3.Database(dbPath, (err) => {
            if (err) {
                console.error('数据库连接错误:', err);
                reject(err);
                return;
            }
        });

        try {
            // 构建查询条件
            let whereConditions = [];
            let params = [];

            if (query.country) {
                whereConditions.push('country LIKE ?');
                params.push(`%${query.country}%`);
            }

            if (query.year) {
                whereConditions.push('year = ?');
                params.push(query.year);
            }

            if (query.search) {
                whereConditions.push('(university LIKE ? OR country LIKE ?)');
                params.push(`%${query.search}%`, `%${query.search}%`);
            }

            const whereClause = whereConditions.length > 0 ? 'WHERE ' + whereConditions.join(' AND ') : '';

            // 排序
            const sortBy = query.sortBy || 'rank';
            const sortOrder = query.sortOrder || 'ASC';
            const orderClause = `ORDER BY ${sortBy} ${sortOrder}`;

            // 分页
            const limit = parseInt(query.limit) || 20;
            const page = parseInt(query.page) || 1;
            const offset = (page - 1) * limit;

            // 获取总数
            const countQuery = `SELECT COUNT(*) as total FROM universities ${whereClause}`;
            
            db.get(countQuery, params, (err, countResult) => {
                if (err) {
                    console.error('获取总数错误:', err);
                    reject(err);
                    return;
                }

                const total = countResult.total;

                // 获取分页数据
                const dataQuery = `
                    SELECT * FROM universities 
                    ${whereClause} 
                    ${orderClause} 
                    LIMIT ? OFFSET ?
                `;

                const queryParams = [...params, limit, offset];

                db.all(dataQuery, queryParams, (err, rows) => {
                    if (err) {
                        console.error('获取数据错误:', err);
                        reject(err);
                        return;
                    }

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

                    db.close();
                });
            });

        } catch (error) {
            console.error('查询执行错误:', error);
            reject(error);
            db.close();
        }
    });
}

// Vercel API处理函数
export default async function handler(req, res) {
    console.log('Universities API called:', req.method, req.url);
    
    // 设置CORS头
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    
    // 处理OPTIONS请求
    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }
    
    // 只允许GET请求
    if (req.method !== 'GET') {
        res.status(405).json({ error: 'Method not allowed' });
        return;
    }
    
    try {
        console.log('Processing request with query:', req.query);
        
        // 获取查询参数
        const query = req.query;
        
        // 获取数据
        const result = await getUniversities(query);
        
        console.log('Returning result with', result.universities.length, 'universities');
        
        res.status(200).json(result);
        
    } catch (error) {
        console.error('API Error:', error);
        res.status(500).json({ 
            error: 'Internal Server Error', 
            details: error.message,
            stack: process.env.NODE_ENV === 'development' ? error.stack : undefined
        });
    }
} 