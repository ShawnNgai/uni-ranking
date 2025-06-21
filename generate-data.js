// 生成完整的大学数据脚本
const fs = require('fs');

// 大学名称模板
const universityTemplates = [
    "University of {city}",
    "{city} University", 
    "{city} Institute of Technology",
    "{city} State University",
    "{city} Polytechnic University",
    "{city} Technical University",
    "{city} Medical University",
    "{city} Business School",
    "{city} College",
    "{city} Academy"
];

// 城市名称
const cities = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
    "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte", "San Francisco", "Indianapolis", "Seattle", "Denver", "Washington",
    "Boston", "El Paso", "Nashville", "Detroit", "Oklahoma City", "Portland", "Las Vegas", "Memphis", "Louisville", "Baltimore",
    "Milwaukee", "Albuquerque", "Tucson", "Fresno", "Sacramento", "Atlanta", "Kansas City", "Long Beach", "Colorado Springs", "Miami",
    "Raleigh", "Omaha", "Minneapolis", "Cleveland", "Tulsa", "Arlington", "New Orleans", "Wichita", "Cleveland", "Tampa",
    "London", "Manchester", "Birmingham", "Leeds", "Liverpool", "Sheffield", "Edinburgh", "Glasgow", "Bristol", "Cardiff",
    "Belfast", "Newcastle", "Nottingham", "Southampton", "Oxford", "Cambridge", "York", "Bath", "Exeter", "Durham",
    "St Andrews", "Warwick", "Loughborough", "Reading", "Surrey", "Sussex", "Kent", "Essex", "Leicester", "Lancaster",
    "Toronto", "Montreal", "Vancouver", "Calgary", "Edmonton", "Ottawa", "Winnipeg", "Quebec City", "Hamilton", "Kitchener",
    "Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Gold Coast", "Newcastle", "Canberra", "Sunshine Coast", "Wollongong",
    "Tokyo", "Osaka", "Nagoya", "Sapporo", "Fukuoka", "Kobe", "Kyoto", "Kawasaki", "Yokohama", "Saitama",
    "Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Chengdu", "Tianjin", "Chongqing", "Nanjing", "Wuhan", "Xi'an",
    "Singapore", "Hong Kong", "Seoul", "Bangkok", "Kuala Lumpur", "Jakarta", "Manila", "Ho Chi Minh City", "Hanoi", "Phnom Penh"
];

// 国家列表
const countries = [
    "United States", "United Kingdom", "Canada", "Australia", "Japan", "China", "Singapore", "South Korea", "Germany", "France",
    "Netherlands", "Switzerland", "Sweden", "Denmark", "Norway", "Finland", "Austria", "Belgium", "Italy", "Spain",
    "Portugal", "Greece", "Poland", "Czech Republic", "Hungary", "Slovakia", "Slovenia", "Croatia", "Serbia", "Bulgaria",
    "Romania", "Ukraine", "Russia", "Belarus", "Lithuania", "Latvia", "Estonia", "Iceland", "Ireland", "New Zealand",
    "Brazil", "Argentina", "Chile", "Mexico", "Colombia", "Peru", "Venezuela", "Ecuador", "Uruguay", "Paraguay",
    "India", "Pakistan", "Bangladesh", "Sri Lanka", "Nepal", "Bhutan", "Maldives", "Afghanistan", "Iran", "Iraq",
    "Saudi Arabia", "United Arab Emirates", "Qatar", "Kuwait", "Bahrain", "Oman", "Yemen", "Jordan", "Lebanon", "Syria",
    "Egypt", "Morocco", "Algeria", "Tunisia", "Libya", "Sudan", "South Sudan", "Ethiopia", "Kenya", "Uganda",
    "Tanzania", "Rwanda", "Burundi", "Democratic Republic of the Congo", "Republic of the Congo", "Gabon", "Cameroon", "Nigeria", "Ghana", "Ivory Coast"
];

// 生成随机分数
function generateRandomScore(min, max) {
    return Math.round((Math.random() * (max - min) + min) * 100) / 100;
}

// 生成星级评分
function generateStarRating(score) {
    if (score >= 95) return "★★★★★";
    if (score >= 85) return "★★★★☆";
    if (score >= 75) return "★★★☆☆";
    if (score >= 65) return "★★☆☆☆";
    return "★☆☆☆☆";
}

// 生成大学数据
function generateUniversityData(year, startId, count) {
    const universities = [];
    
    for (let i = 0; i < count; i++) {
        const rank = i + 1;
        const country = countries[Math.floor(Math.random() * countries.length)];
        const city = cities[Math.floor(Math.random() * cities.length)];
        const template = universityTemplates[Math.floor(Math.random() * universityTemplates.length)];
        const universityName = template.replace('{city}', city);
        
        const research = generateRandomScore(60, 100);
        const reputation = generateRandomScore(50, 100);
        const employment = generateRandomScore(70, 100);
        const international = generateRandomScore(40, 100);
        const totalScore = Math.round((research * 0.3 + reputation * 0.3 + employment * 0.2 + international * 0.2) * 100) / 100;
        
        universities.push({
            id: startId + i,
            rank: rank,
            university: universityName,
            country: country,
            research: research,
            reputation: reputation,
            employment: employment,
            international: international,
            total_score: totalScore,
            star_rating: generateStarRating(totalScore),
            year: year
        });
    }
    
    return universities;
}

// 生成完整数据
function generateCompleteData() {
    console.log('开始生成大学数据...');
    
    // 生成2025年数据 (3000所大学)
    const universities2025 = generateUniversityData(2025, 1, 3000);
    console.log(`生成了 ${universities2025.length} 所2025年大学数据`);
    
    // 生成2024年数据 (2000所大学)
    const universities2024 = generateUniversityData(2024, 3001, 2000);
    console.log(`生成了 ${universities2024.length} 所2024年大学数据`);
    
    // 合并数据
    const allUniversities = [...universities2025, ...universities2024];
    
    // 获取所有国家
    const allCountries = [...new Set(allUniversities.map(uni => uni.country))].sort();
    
    // 生成JavaScript代码
    const jsCode = `// 完整的大学排名数据 - 静态数据
// 2025年数据 (${universities2025.length}所大学)
const UNIVERSITIES_2025 = ${JSON.stringify(universities2025, null, 2)};

// 2024年数据 (${universities2024.length}所大学)  
const UNIVERSITIES_2024 = ${JSON.stringify(universities2024, null, 2)};

// 合并所有数据
const ALL_UNIVERSITIES_DATA = [...UNIVERSITIES_2025, ...UNIVERSITIES_2024];

// 获取所有国家列表
const ALL_COUNTRIES = ${JSON.stringify(allCountries, null, 2)};

// 数据查询函数
function getUniversitiesData(filters) {
    let filteredData = [...ALL_UNIVERSITIES_DATA];
    
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

function getCountriesData() {
    return ALL_COUNTRIES;
}

// 导出函数供其他文件使用
window.getUniversitiesData = getUniversitiesData;
window.getCountriesData = getCountriesData;`;

    // 写入文件
    fs.writeFileSync('public/js/complete-data.js', jsCode);
    console.log('数据已写入 public/js/complete-data.js');
    console.log(`总共生成了 ${allUniversities.length} 所大学数据`);
    console.log(`涵盖 ${allCountries.length} 个国家`);
}

// 运行生成器
generateCompleteData(); 