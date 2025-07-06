// 移动端优化的大学API
import { MOBILE_UNIVERSITIES_DATA } from '../public/js/mobile-data.js';

// 内存缓存
let cache = new Map();
const CACHE_DURATION = 10 * 60 * 1000; // 10分钟缓存

// 获取移动端大学数据
function getMobileUniversities(query) {
    return new Promise((resolve, reject) => {
        try {
            console.log('移动端API查询:', query);
            
            // 检查缓存
            const cacheKey = JSON.stringify(query);
            const cached = cache.get(cacheKey);
            if (cached && (Date.now() - cached.timestamp) < CACHE_DURATION) {
                console.log('返回移动端缓存数据');
                resolve(cached.data);
                return;
            }
            
            let filteredData = [...MOBILE_UNIVERSITIES_DATA];
            
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
            
            // 分页 - 移动端优化
            const limit = parseInt(query.limit) || 10; // 移动端默认10条
            const page = parseInt(query.page) || 1;
            const offset = (page - 1) * limit;
            
            const total = filteredData.length;
            const totalPages = Math.ceil(total / limit);
            const paginatedData = filteredData.slice(offset, offset + limit);
            
            const result = {
                universities: paginatedData,
                pagination: {
                    page,
                    limit,
                    total,
                    totalPages
                },
                mobile_optimized: true
            };
            
            // 缓存结果
            cache.set(cacheKey, {
                data: result,
                timestamp: Date.now()
            });
            
            console.log(`移动端API返回 ${paginatedData.length} 条数据，总计 ${total} 条`);
            
            resolve(result);
            
        } catch (error) {
            console.error('移动端API查询执行错误:', error);
            reject(error);
        }
    });
}

// Vercel API处理函数
export default async function handler(req, res) {
    console.log('Mobile Universities API called:', req.method, req.url);
    
    // 设置CORS头
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    
    // 添加缓存控制头 - 移动端更长的缓存时间
    res.setHeader('Cache-Control', 'public, max-age=600'); // 10分钟缓存
    res.setHeader('ETag', `"mobile-${Date.now()}"`);
    
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
        console.log('Processing mobile request with query:', req.query);
        
        // 获取查询参数
        const query = req.query;
        
        // 获取数据
        const result = await getMobileUniversities(query);
        
        console.log('Mobile API returning result with', result.universities.length, 'universities');
        
        res.status(200).json(result);
        
    } catch (error) {
        console.error('Mobile API Error:', error);
        res.status(500).json({ 
            error: 'Internal Server Error', 
            details: error.message,
            stack: process.env.NODE_ENV === 'development' ? error.stack : undefined
        });
    }
} 