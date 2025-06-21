const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// 创建数据库连接
function getDatabase() {
    const dbPath = path.join(process.cwd(), 'database', 'rankings.db');
    return new sqlite3.Database(dbPath);
}

// 获取国家列表
function getCountries() {
    return new Promise((resolve, reject) => {
        const db = getDatabase();
        
        db.all("SELECT DISTINCT country FROM universities WHERE country IS NOT NULL AND country != '' ORDER BY country", (err, rows) => {
            if (err) {
                reject(err);
            } else {
                const countries = rows.map(row => row.country);
                resolve(countries);
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
        const countries = await getCountries();
        res.status(200).json(countries);
    } catch (error) {
        console.error('API Error:', error);
        res.status(500).json({ error: 'Internal Server Error', details: error.message });
    }
}; 