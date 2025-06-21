// 静态大学排名数据 - 可以直接在Wix中使用
const UNIVERSITY_DATA = {
    "2025": [
        {
            "rank": 1,
            "university": "Massachusetts Institute of Technology (MIT)",
            "country": "United States",
            "research": 95.2,
            "reputation": 98.5,
            "employment": 96.8,
            "international": 92.1,
            "total_score": 95.7,
            "star_rating": 5,
            "year": "2025"
        },
        {
            "rank": 2,
            "university": "Stanford University",
            "country": "United States",
            "research": 94.8,
            "reputation": 97.2,
            "employment": 95.9,
            "international": 90.5,
            "total_score": 94.6,
            "star_rating": 5,
            "year": "2025"
        },
        {
            "rank": 3,
            "university": "Harvard University",
            "country": "United States",
            "research": 93.5,
            "reputation": 99.1,
            "employment": 97.2,
            "international": 88.9,
            "total_score": 94.2,
            "star_rating": 5,
            "year": "2025"
        },
        {
            "rank": 4,
            "university": "University of Oxford",
            "country": "United Kingdom",
            "research": 92.8,
            "reputation": 96.7,
            "employment": 94.1,
            "international": 91.3,
            "total_score": 93.7,
            "star_rating": 5,
            "year": "2025"
        },
        {
            "rank": 5,
            "university": "University of Cambridge",
            "country": "United Kingdom",
            "research": 92.1,
            "reputation": 95.8,
            "employment": 93.5,
            "international": 90.2,
            "total_score": 92.9,
            "star_rating": 5,
            "year": "2025"
        },
        {
            "rank": 6,
            "university": "California Institute of Technology (Caltech)",
            "country": "United States",
            "research": 94.2,
            "reputation": 93.4,
            "employment": 92.8,
            "international": 87.6,
            "total_score": 92.0,
            "star_rating": 5,
            "year": "2025"
        },
        {
            "rank": 7,
            "university": "ETH Zurich",
            "country": "Switzerland",
            "research": 91.5,
            "reputation": 92.1,
            "employment": 91.7,
            "international": 94.8,
            "total_score": 92.5,
            "star_rating": 5,
            "year": "2025"
        },
        {
            "rank": 8,
            "university": "University of California, Berkeley",
            "country": "United States",
            "research": 91.8,
            "reputation": 93.7,
            "employment": 90.9,
            "international": 89.3,
            "total_score": 91.4,
            "star_rating": 5,
            "year": "2025"
        },
        {
            "rank": 9,
            "university": "Imperial College London",
            "country": "United Kingdom",
            "research": 90.9,
            "reputation": 91.8,
            "employment": 92.1,
            "international": 93.2,
            "total_score": 92.0,
            "star_rating": 5,
            "year": "2025"
        },
        {
            "rank": 10,
            "university": "University of Chicago",
            "country": "United States",
            "research": 89.7,
            "reputation": 94.2,
            "employment": 91.5,
            "international": 86.4,
            "total_score": 90.5,
            "star_rating": 5,
            "year": "2025"
        }
    ],
    "2024": [
        {
            "rank": 1,
            "university": "Massachusetts Institute of Technology (MIT)",
            "country": "United States",
            "research": 94.8,
            "reputation": 98.2,
            "employment": 96.5,
            "international": 91.8,
            "total_score": 95.3,
            "star_rating": 5,
            "year": "2024"
        },
        {
            "rank": 2,
            "university": "Stanford University",
            "country": "United States",
            "research": 94.2,
            "reputation": 96.9,
            "employment": 95.6,
            "international": 90.1,
            "total_score": 94.2,
            "star_rating": 5,
            "year": "2024"
        },
        {
            "rank": 3,
            "university": "Harvard University",
            "country": "United States",
            "research": 93.1,
            "reputation": 98.8,
            "employment": 96.9,
            "international": 88.5,
            "total_score": 94.3,
            "star_rating": 5,
            "year": "2024"
        },
        {
            "rank": 4,
            "university": "University of Oxford",
            "country": "United Kingdom",
            "research": 92.3,
            "reputation": 96.4,
            "employment": 93.8,
            "international": 91.0,
            "total_score": 93.4,
            "star_rating": 5,
            "year": "2024"
        },
        {
            "rank": 5,
            "university": "University of Cambridge",
            "country": "United Kingdom",
            "research": 91.7,
            "reputation": 95.5,
            "employment": 93.2,
            "international": 89.9,
            "total_score": 92.6,
            "star_rating": 5,
            "year": "2024"
        }
    ]
};

// 获取所有国家列表
function getAllCountries() {
    const countries = new Set();
    Object.values(UNIVERSITY_DATA).forEach(yearData => {
        yearData.forEach(uni => {
            countries.add(uni.country);
        });
    });
    return Array.from(countries).sort();
}

// 筛选大学数据
function filterUniversities(filters) {
    let data = UNIVERSITY_DATA[filters.year] || UNIVERSITY_DATA["2025"];
    
    // 按国家筛选
    if (filters.country) {
        data = data.filter(uni => uni.country === filters.country);
    }
    
    // 按搜索词筛选
    if (filters.search) {
        const searchTerm = filters.search.toLowerCase();
        data = data.filter(uni => 
            uni.university.toLowerCase().includes(searchTerm) ||
            uni.country.toLowerCase().includes(searchTerm)
        );
    }
    
    // 排序
    data.sort((a, b) => {
        let aValue, bValue;
        
        switch (filters.sortBy) {
            case 'university':
                aValue = a.university;
                bValue = b.university;
                break;
            case 'country':
                aValue = a.country;
                bValue = b.country;
                break;
            case 'research':
                aValue = a.research;
                bValue = b.research;
                break;
            case 'reputation':
                aValue = a.reputation;
                bValue = b.reputation;
                break;
            case 'employment':
                aValue = a.employment;
                bValue = b.employment;
                break;
            case 'total_score':
                aValue = a.total_score;
                bValue = b.total_score;
                break;
            default:
                aValue = a.rank;
                bValue = b.rank;
        }
        
        if (filters.sortOrder === 'DESC') {
            return bValue > aValue ? 1 : -1;
        } else {
            return aValue > bValue ? 1 : -1;
        }
    });
    
    // 分页
    const startIndex = (filters.page - 1) * filters.limit;
    const endIndex = startIndex + filters.limit;
    const paginatedData = data.slice(startIndex, endIndex);
    
    return {
        universities: paginatedData,
        pagination: {
            currentPage: filters.page,
            totalPages: Math.ceil(data.length / filters.limit),
            totalResults: data.length,
            startIndex: startIndex,
            endIndex: Math.min(endIndex, data.length),
            limit: filters.limit
        }
    };
} 