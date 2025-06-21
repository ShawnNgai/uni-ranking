// 使用内存数据，避免SQLite在Vercel环境中的问题
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
    },
    {
        id: 6,
        rank: 6,
        university: "California Institute of Technology",
        country: "United States",
        research: 100,
        reputation: 96.8,
        employment: 100,
        international: 94.2,
        total_score: 98.9,
        star_rating: "★★★★★",
        year: 2025
    },
    {
        id: 7,
        rank: 7,
        university: "ETH Zurich",
        country: "Switzerland",
        research: 100,
        reputation: 96.5,
        employment: 100,
        international: 93.8,
        total_score: 98.7,
        star_rating: "★★★★★",
        year: 2025
    },
    {
        id: 8,
        rank: 8,
        university: "Imperial College London",
        country: "United Kingdom",
        research: 100,
        reputation: 96.2,
        employment: 100,
        international: 93.5,
        total_score: 98.5,
        star_rating: "★★★★★",
        year: 2025
    },
    {
        id: 9,
        rank: 9,
        university: "University of Chicago",
        country: "United States",
        research: 100,
        reputation: 95.9,
        employment: 100,
        international: 93.1,
        total_score: 98.3,
        star_rating: "★★★★★",
        year: 2025
    },
    {
        id: 10,
        rank: 10,
        university: "University College London",
        country: "United Kingdom",
        research: 100,
        reputation: 95.6,
        employment: 100,
        international: 92.8,
        total_score: 98.1,
        star_rating: "★★★★★",
        year: 2025
    }
];

// 获取大学数据
function getUniversities(query) {
    let filteredData = [...sampleData];
    
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
    
    return {
        universities: paginatedData,
        pagination: {
            page,
            limit,
            total,
            totalPages
        }
    };
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
        // 获取查询参数
        const query = req.query;
        
        // 获取数据
        const result = getUniversities(query);
        
        res.status(200).json(result);
    } catch (error) {
        console.error('API Error:', error);
        res.status(500).json({ error: 'Internal Server Error', details: error.message });
    }
}; 