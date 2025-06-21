// Vercel Serverless Function for Universities API
export default async function handler(req, res) {
    console.log('API called:', req.method, req.url);
    
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
        
        // 示例数据
        const sampleData = [
            {
                id: 1,
                rank: 1,
                university: "Massachusetts Institute of Technology",
                country: "United States",
                research: 100,
                reputation: 99.73,
                employment: 100,
                international: 96.675,
                total_score: 99.6,
                star_rating: "★★★★★",
                year: 2025
            },
            {
                id: 2,
                rank: 2,
                university: "Harvard University",
                country: "United States",
                research: 100,
                reputation: 97.88,
                employment: 100,
                international: 99.9,
                total_score: 99.46,
                star_rating: "★★★★★",
                year: 2025
            },
            {
                id: 3,
                rank: 3,
                university: "University of Oxford",
                country: "United Kingdom",
                research: 100,
                reputation: 98.16,
                employment: 100,
                international: 97.7,
                total_score: 99.31,
                star_rating: "★★★★★",
                year: 2025
            },
            {
                id: 4,
                rank: 4,
                university: "Stanford University",
                country: "United States",
                research: 100,
                reputation: 97.5,
                employment: 100,
                international: 95.8,
                total_score: 99.2,
                star_rating: "★★★★★",
                year: 2025
            },
            {
                id: 5,
                rank: 5,
                university: "University of Cambridge",
                country: "United Kingdom",
                research: 100,
                reputation: 97.2,
                employment: 100,
                international: 96.5,
                total_score: 99.1,
                star_rating: "★★★★★",
                year: 2025
            }
        ];
        
        // 获取查询参数
        const { country, year, search, sortBy = 'rank', sortOrder = 'ASC', limit = 20, page = 1 } = req.query;
        
        console.log('Query parameters:', { country, year, search, sortBy, sortOrder, limit, page });
        
        // 筛选数据
        let filteredData = [...sampleData];
        
        if (country) {
            filteredData = filteredData.filter(uni => 
                uni.country.toLowerCase().includes(country.toLowerCase())
            );
        }
        
        if (year) {
            filteredData = filteredData.filter(uni => uni.year == year);
        }
        
        if (search) {
            const searchTerm = search.toLowerCase();
            filteredData = filteredData.filter(uni => 
                uni.university.toLowerCase().includes(searchTerm) ||
                uni.country.toLowerCase().includes(searchTerm)
            );
        }
        
        // 排序
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
        const limitNum = parseInt(limit);
        const pageNum = parseInt(page);
        const offset = (pageNum - 1) * limitNum;
        
        const total = filteredData.length;
        const totalPages = Math.ceil(total / limitNum);
        const paginatedData = filteredData.slice(offset, offset + limitNum);
        
        const result = {
            universities: paginatedData,
            pagination: {
                page: pageNum,
                limit: limitNum,
                total,
                totalPages
            }
        };
        
        console.log('Returning result:', result);
        
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