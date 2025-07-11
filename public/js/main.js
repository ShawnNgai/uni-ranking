// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    loadTopUniversities();
});

// 检测是否为移动设备
function isMobileDevice() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
           window.innerWidth <= 768;
}

// 加载顶部大学排名
async function loadTopUniversities() {
    try {
        const isMobile = isMobileDevice();
        const apiEndpoint = isMobile ? '/api/mobile-universities' : '/api/universities';
        
        console.log(`使用${isMobile ? '移动端' : '桌面端'}API:`, apiEndpoint);
        
        const response = await fetch(`${apiEndpoint}?limit=5&sortBy=rank&sortOrder=ASC&year=2025`);
        const data = await response.json();
        
        if (response.ok) {
            displayTopUniversities(data.universities);
        } else {
            throw new Error(data.error || '加载数据失败');
        }
    } catch (error) {
        console.error('加载顶部大学排名失败:', error);
        // 显示默认数据
        displayDefaultTopUniversities();
    }
}

// 显示顶部大学排名
function displayTopUniversities(universities) {
    const tbody = document.getElementById('top-universities');
    tbody.innerHTML = '';
    
    universities.forEach(uni => {
        const row = document.createElement('tr');
        row.className = 'fade-in';
        
        const rankClass = uni.rank <= 3 ? `rank-${uni.rank}` : 'rank-other';
        
        row.innerHTML = `
            <td>
                <span class="rank-badge ${rankClass}">${uni.rank}</span>
            </td>
            <td><strong>${uni.university}</strong></td>
            <td>${uni.country}</td>
            <td><strong>${uni.total_score.toFixed(1)}</strong></td>
        `;
        
        tbody.appendChild(row);
    });
}

// 显示默认的顶部大学排名（当API不可用时）
function displayDefaultTopUniversities() {
    const tbody = document.getElementById('top-universities');
    tbody.innerHTML = `
        <tr class="fade-in">
            <td><span class="rank-badge rank-1">1</span></td>
            <td><strong>Massachusetts Institute of Technology</strong></td>
            <td>United States</td>
            <td><strong>99.6</strong></td>
        </tr>
        <tr class="fade-in">
            <td><span class="rank-badge rank-2">2</span></td>
            <td><strong>Harvard University</strong></td>
            <td>United States</td>
            <td><strong>99.46</strong></td>
        </tr>
        <tr class="fade-in">
            <td><span class="rank-badge rank-3">3</span></td>
            <td><strong>University of Oxford</strong></td>
            <td>United Kingdom</td>
            <td><strong>99.31</strong></td>
        </tr>
        <tr class="fade-in">
            <td><span class="rank-badge rank-other">4</span></td>
            <td><strong>Stanford University</strong></td>
            <td>United States</td>
            <td><strong>99.17</strong></td>
        </tr>
        <tr class="fade-in">
            <td><span class="rank-badge rank-other">5</span></td>
            <td><strong>University of Cambridge</strong></td>
            <td>United Kingdom</td>
            <td><strong>99.03</strong></td>
        </tr>
    `;
} 