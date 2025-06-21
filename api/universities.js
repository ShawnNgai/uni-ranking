// 使用真实大学数据 - 从数据库导出的静态数据
import { REAL_UNIVERSITIES_DATA } from '../public/js/real-data.js';

// 获取大学数据
function getUniversities(query) {
    return new Promise((resolve, reject) => {
        try {
            console.log('使用真实数据查询:', query);
            
            let filteredData = [...REAL_UNIVERSITIES_DATA];
            
            // 筛选条件
            if (query.country) {
                filteredData = filteredData.filter(uni => 
                    uni.country.toLowerCase().includes(query.country.toLowerCase())
                );
            }
            
            if (query.year) {
                filteredData = filteredData.filter(uni => uni.year == query.year);
            }
            
            if (query.search) {
                const searchTerm = query.search.toLowerCase();
                filteredData = filteredData.filter(uni => 
                    uni.university.toLowerCase().includes(searchTerm) ||
                    uni.country.toLowerCase().includes(searchTerm)
                );
            }
            
            // 排序
            const sortBy = query.sortBy || 'rank';
            const sortOrder = query.sortOrder || 'ASC';
            
            filteredData.sort((a, b) => {
                let aVal = a[sortBy];
                let bVal = b[sortBy];
                
                if (typeof aVal === 'string') {
                    aVal = aVal.toLowerCase();
                    bVal = bVal.toLowerCase();
                }
                
                if (sortOrder === 'ASC') {
                    return aVal > bVal ? 1 : -1;
                } else {
                    return aVal < bVal ? 1 : -1;
                }
            });
            
            // 分页
            const limit = parseInt(query.limit) || 20;
            const page = parseInt(query.page) || 1;
            const offset = (page - 1) * limit;
            
            const total = filteredData.length;
            const totalPages = Math.ceil(total / limit);
            const paginatedData = filteredData.slice(offset, offset + limit);
            
            console.log(`返回 ${paginatedData.length} 条数据，总计 ${total} 条`);
            
            resolve({
                universities: paginatedData,
                pagination: {
                    page,
                    limit,
                    total,
                    totalPages
                }
            });
            
        } catch (error) {
            console.error('查询执行错误:', error);
            reject(error);
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