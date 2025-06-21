// 从数据库获取国家列表
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// 数据库路径
const dbPath = path.join(__dirname, '../database/rankings.db');

// 获取国家列表
function getCountries() {
    return new Promise((resolve, reject) => {
        const db = new sqlite3.Database(dbPath, (err) => {
            if (err) {
                console.error('数据库连接错误:', err);
                reject(err);
                return;
            }
        });

        try {
            const query = 'SELECT DISTINCT country FROM universities ORDER BY country';
            
            db.all(query, [], (err, rows) => {
                if (err) {
                    console.error('获取国家列表错误:', err);
                    reject(err);
                    return;
                }

                const countries = rows.map(row => row.country);
                console.log('获取到', countries.length, '个国家');
                
                resolve(countries);
                db.close();
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
    console.log('Countries API called:', req.method, req.url);
    
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
        console.log('Returning countries:', countries);
        res.status(200).json(countries);
    } catch (error) {
        console.error('Countries API Error:', error);
        res.status(500).json({ error: 'Internal Server Error', details: error.message });
    }
} 