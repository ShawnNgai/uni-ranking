// 使用内存数据，避免SQLite在Vercel环境中的问题
const countries = [
    "United States",
    "United Kingdom", 
    "Switzerland",
    "Germany",
    "Canada",
    "Australia",
    "Netherlands",
    "Singapore",
    "Japan",
    "France",
    "Sweden",
    "Denmark",
    "Norway",
    "Finland",
    "Austria",
    "Belgium",
    "Italy",
    "Spain",
    "South Korea",
    "China"
];

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
        res.status(200).json(countries);
    } catch (error) {
        console.error('API Error:', error);
        res.status(500).json({ error: 'Internal Server Error', details: error.message });
    }
}; 