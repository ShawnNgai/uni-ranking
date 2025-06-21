// 静态数据 - 避免API调用问题
const STATIC_UNIVERSITIES_DATA = [
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
    },
    {
        id: 11,
        rank: 11,
        university: "National University of Singapore",
        country: "Singapore",
        research: 100,
        reputation: 95.3,
        employment: 100,
        international: 92.5,
        total_score: 97.9,
        star_rating: "★★★★★",
        year: 2025
    },
    {
        id: 12,
        rank: 12,
        university: "Peking University",
        country: "China",
        research: 100,
        reputation: 95.0,
        employment: 100,
        international: 92.2,
        total_score: 97.7,
        star_rating: "★★★★★",
        year: 2025
    },
    {
        id: 13,
        rank: 13,
        university: "Tsinghua University",
        country: "China",
        research: 100,
        reputation: 94.7,
        employment: 100,
        international: 91.9,
        total_score: 97.5,
        star_rating: "★★★★★",
        year: 2025
    },
    {
        id: 14,
        rank: 14,
        university: "University of Tokyo",
        country: "Japan",
        research: 100,
        reputation: 94.4,
        employment: 100,
        international: 91.6,
        total_score: 97.3,
        star_rating: "★★★★★",
        year: 2025
    },
    {
        id: 15,
        rank: 15,
        university: "University of Toronto",
        country: "Canada",
        research: 100,
        reputation: 94.1,
        employment: 100,
        international: 91.3,
        total_score: 97.1,
        star_rating: "★★★★★",
        year: 2025
    }
];

const STATIC_COUNTRIES_DATA = [
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

// 静态数据API模拟函数
function getStaticUniversities(filters) {
    let filteredData = [...STATIC_UNIVERSITIES_DATA];
    
    // 筛选条件
    if (filters.country) {
        filteredData = filteredData.filter(uni => 
            uni.country.toLowerCase().includes(filters.country.toLowerCase())
        );
    }
    
    if (filters.year) {
        filteredData = filteredData.filter(uni => uni.year == filters.year);
    }
    
    if (filters.search) {
        const searchTerm = filters.search.toLowerCase();
        filteredData = filteredData.filter(uni => 
            uni.university.toLowerCase().includes(searchTerm) ||
            uni.country.toLowerCase().includes(searchTerm)
        );
    }
    
    // 排序
    const sortBy = filters.sortBy || 'rank';
    const sortOrder = filters.sortOrder || 'ASC';
    
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
    const limit = parseInt(filters.limit) || 20;
    const page = parseInt(filters.page) || 1;
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

function getStaticCountries() {
    return STATIC_COUNTRIES_DATA;
} 