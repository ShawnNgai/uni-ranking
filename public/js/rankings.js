// 全局变量
let currentPage = 1;
let currentFilters = {
    page: 1,
    limit: 20,
    country: '',
    year: '2025',
    search: '',
    sortBy: 'rank',
    sortOrder: 'ASC'
};

// 配置API基础URL
const API_BASE_URL = ''; // 使用相对路径，自动适配部署域名

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializePage();
    loadFilterOptions();
    loadUniversities();
    
    // 绑定事件监听器
    document.getElementById('filterForm').addEventListener('submit', handleFilterSubmit);
    document.getElementById('resetFilters').addEventListener('click', resetFilters);
});

// 初始化页面
function initializePage() {
    // 从URL参数中恢复筛选条件
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('page')) currentFilters.page = parseInt(urlParams.get('page'));
    if (urlParams.has('limit')) currentFilters.limit = parseInt(urlParams.get('limit'));
    if (urlParams.has('country')) currentFilters.country = urlParams.get('country');
    if (urlParams.has('year')) currentFilters.year = urlParams.get('year');
    if (urlParams.has('search')) currentFilters.search = urlParams.get('search');
    if (urlParams.has('sortBy')) currentFilters.sortBy = urlParams.get('sortBy');
    if (urlParams.has('sortOrder')) currentFilters.sortOrder = urlParams.get('sortOrder');
    
    // 如果没有指定年份，默认使用2025
    if (!currentFilters.year) {
        currentFilters.year = '2025';
    }
    
    // 更新表单值
    updateFormValues();
}

// 更新表单值
function updateFormValues() {
    document.getElementById('search').value = currentFilters.search;
    document.getElementById('country').value = currentFilters.country;
    document.getElementById('year').value = currentFilters.year;
    document.getElementById('sortBy').value = currentFilters.sortBy;
    document.getElementById('sortOrder').value = currentFilters.sortOrder;
    document.getElementById('limit').value = currentFilters.limit;
}

// 加载筛选选项 - 使用真实数据
function loadFilterOptions() {
    try {
        // 使用真实国家列表
        const countries = getRealCountriesData();
        const countrySelect = document.getElementById('country');
        countries.forEach(country => {
            const option = document.createElement('option');
            option.value = country;
            option.textContent = country;
            countrySelect.appendChild(option);
        });
        
        // 加载年份列表 - 只显示2025和2024年
        const yearSelect = document.getElementById('year');
        yearSelect.innerHTML = ''; // 清空现有选项
        
        // 添加2025年选项（默认选中）
        const option2025 = document.createElement('option');
        option2025.value = '2025';
        option2025.textContent = '2025';
        option2025.selected = true;
        yearSelect.appendChild(option2025);
        
        // 添加2024年选项
        const option2024 = document.createElement('option');
        option2024.value = '2024';
        option2024.textContent = '2024';
        yearSelect.appendChild(option2024);
        
        // 加载完选项后，重新应用URL参数
        updateFormValues();
        
    } catch (error) {
        console.error('Failed to load filter options:', error);
    }
}

// 处理筛选表单提交
function handleFilterSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    currentFilters = {
        page: 1,
        limit: parseInt(formData.get('limit')) || 20,
        country: formData.get('country') || '',
        year: formData.get('year') || '',
        search: formData.get('search') || '',
        sortBy: formData.get('sortBy') || 'rank',
        sortOrder: formData.get('sortOrder') || 'ASC'
    };
    
    // 更新URL
    updateURL();
    
    // 重新加载数据
    loadUniversities();
}

// 重置筛选条件
function resetFilters() {
    currentFilters = {
        page: 1,
        limit: 20,
        country: '',
        year: '2025', // 重置时默认选择2025年
        search: '',
        sortBy: 'rank',
        sortOrder: 'ASC'
    };
    
    // 重置表单
    document.getElementById('filterForm').reset();
    
    // 手动设置年份为2025
    document.getElementById('year').value = '2025';
    
    // 更新URL
    updateURL();
    
    // 重新加载数据
    loadUniversities();
}

// 更新URL参数
function updateURL() {
    const url = new URL(window.location);
    Object.keys(currentFilters).forEach(key => {
        if (currentFilters[key]) {
            url.searchParams.set(key, currentFilters[key]);
        } else {
            url.searchParams.delete(key);
        }
    });
    window.history.pushState({}, '', url);
}

// 加载大学数据 - 使用真实数据
function loadUniversities() {
    showLoading(true);
    
    try {
        // 使用真实数据函数
        const data = getRealUniversitiesData(currentFilters);
        
            displayUniversities(data.universities);
            displayPagination(data.pagination);
            updateResultCount(data.pagination);
        
    } catch (error) {
        console.error('加载大学数据失败:', error);
        showError('加载数据失败，请稍后重试');
    } finally {
        showLoading(false);
    }
}

// 显示大学数据
function displayUniversities(universities) {
    const tbody = document.getElementById('universitiesTable');
    tbody.innerHTML = '';
    
    if (universities.length === 0) {
        tbody.innerHTML = '<tr><td colspan="10" style="text-align: center; padding: 2rem;">No matching universities found</td></tr>';
        return;
    }
    
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
            <td>${uni.research.toFixed(1)}</td>
            <td>${uni.reputation.toFixed(1)}</td>
            <td>${uni.employment.toFixed(1)}</td>
            <td>${uni.international.toFixed(1)}</td>
            <td><strong>${uni.total_score.toFixed(1)}</strong></td>
            <td>${uni.star_rating}</td>
            <td>${uni.year}</td>
        `;
        
        tbody.appendChild(row);
    });
}

// 显示分页
function displayPagination(pagination) {
    const paginationContainer = document.getElementById('pagination');
    
    if (pagination.totalPages <= 1) {
        paginationContainer.style.display = 'none';
        return;
    }
    
    paginationContainer.style.display = 'flex';
    paginationContainer.innerHTML = '';
    
    const { page, totalPages } = pagination;
    
    // 上一页按钮
    const prevBtn = document.createElement('button');
    prevBtn.textContent = 'Previous';
    prevBtn.disabled = page <= 1;
    prevBtn.addEventListener('click', () => changePage(page - 1));
    paginationContainer.appendChild(prevBtn);
    
    // 页码按钮
    const startPage = Math.max(1, page - 2);
    const endPage = Math.min(totalPages, page + 2);
    
    for (let i = startPage; i <= endPage; i++) {
        const pageBtn = document.createElement('button');
        pageBtn.textContent = i;
        pageBtn.className = i === page ? 'active' : '';
        pageBtn.addEventListener('click', () => changePage(i));
        paginationContainer.appendChild(pageBtn);
    }
    
    // 下一页按钮
    const nextBtn = document.createElement('button');
    nextBtn.textContent = 'Next';
    nextBtn.disabled = page >= totalPages;
    nextBtn.addEventListener('click', () => changePage(page + 1));
    paginationContainer.appendChild(nextBtn);
}

// 切换页面
function changePage(newPage) {
    currentFilters.page = newPage;
    updateURL();
    loadUniversities();
}

// 更新结果计数
function updateResultCount(pagination) {
    const resultCount = document.getElementById('resultCount');
    if (resultCount) {
        resultCount.textContent = `Showing ${(pagination.page - 1) * pagination.limit + 1} - ${Math.min(pagination.page * pagination.limit, pagination.total)} of ${pagination.total} results`;
    }
}

// 显示加载状态
function showLoading(show) {
    const loadingElement = document.getElementById('loading');
    const tableContent = document.getElementById('tableContent');
    
    if (show) {
        loadingElement.style.display = 'flex';
        tableContent.style.display = 'none';
    } else {
        loadingElement.style.display = 'none';
        tableContent.style.display = 'block';
    }
}

// 显示错误信息
function showError(message) {
    const tbody = document.getElementById('universitiesTable');
    tbody.innerHTML = `<tr><td colspan="10" style="text-align: center; padding: 2rem; color: #dc3545;">${message}</td></tr>`;
    
    const tableContent = document.getElementById('tableContent');
    tableContent.style.display = 'block';
}

// 更新分页信息
function updatePaginationInfo(page, totalPages, totalResults) {
    const paginationInfo = document.getElementById('pagination-info');
    if (paginationInfo) {
        paginationInfo.textContent = `Page ${page} of ${totalPages} (${totalResults} results)`;
    }
} 