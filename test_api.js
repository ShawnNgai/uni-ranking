const fetch = require('node-fetch');

async function testAPI() {
    console.log('测试API连接...');
    
    try {
        // 测试获取大学数据
        const response = await fetch('http://localhost:3000/api/universities');
        const data = await response.json();
        
        console.log('API响应状态:', response.status);
        console.log('数据:', data);
        
        if (data.universities) {
            console.log(`成功获取 ${data.universities.length} 条大学数据`);
            if (data.universities.length > 0) {
                console.log('第一条数据:', data.universities[0]);
            }
        }
        
        // 测试获取国家列表
        const countriesResponse = await fetch('http://localhost:3000/api/countries');
        const countries = await countriesResponse.json();
        console.log('国家列表:', countries);
        
    } catch (error) {
        console.error('API测试失败:', error);
    }
}

testAPI(); 