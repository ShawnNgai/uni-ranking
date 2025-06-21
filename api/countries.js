// 使用真实国家数据 - 从数据库导出的静态数据
import { REAL_COUNTRIES } from '../public/js/real-data.js';

// 获取国家列表
function getCountries() {
    return new Promise((resolve, reject) => {
        try {
            console.log('获取真实国家列表');
            console.log('国家数量:', REAL_COUNTRIES.length);
            
            resolve(REAL_COUNTRIES);
            
        } catch (error) {
            console.error('获取国家列表错误:', error);
            reject(error);
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