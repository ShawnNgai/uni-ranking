// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    loadDataStats();
    loadDataPreview();
    
    // 绑定事件监听器
    document.getElementById('downloadTemplate').addEventListener('click', downloadTemplate);
    document.getElementById('uploadForm').addEventListener('submit', handleFileUpload);
    document.getElementById('clearData').addEventListener('click', clearAllData);
    document.getElementById('exportAllData').addEventListener('click', exportAllData);
    document.getElementById('import2024Btn').addEventListener('click', import2024Data);
    document.getElementById('import2025Btn').addEventListener('click', import2025Data);
});

// 下载模板
async function downloadTemplate() {
    try {
        const response = await fetch('/api/template');
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'university_template.xlsx';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } else {
            throw new Error('下载模板失败');
        }
    } catch (error) {
        console.error('下载模板失败:', error);
        alert('下载模板失败，请稍后重试');
    }
}

// 处理文件上传
async function handleFileUpload(event) {
    event.preventDefault();
    
    const fileInput = document.getElementById('file');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('请选择文件');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    const resultDiv = document.getElementById('uploadResult');
    resultDiv.innerHTML = '<div class="loading"><div class="spinner"></div><span style="margin-left: 1rem;">正在上传...</span></div>';
    
    try {
        const response = await fetch('/api/import', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            resultDiv.innerHTML = `
                <div style="background: #d4edda; color: #155724; padding: 1rem; border-radius: 5px; border: 1px solid #c3e6cb;">
                    <h4><i class="fas fa-check-circle"></i> 上传成功</h4>
                    <p>成功导入: ${result.successCount} 条记录</p>
                    <p>失败: ${result.errorCount} 条记录</p>
                    <p>总计: ${result.totalCount} 条记录</p>
                </div>
            `;
            
            // 刷新数据统计和预览
            loadDataStats();
            loadDataPreview();
        } else {
            resultDiv.innerHTML = `
                <div style="background: #f8d7da; color: #721c24; padding: 1rem; border-radius: 5px; border: 1px solid #f5c6cb;">
                    <h4><i class="fas fa-exclamation-triangle"></i> 上传失败</h4>
                    <p>${result.error}</p>
                    ${result.requiredFields ? `<p>必需字段: ${result.requiredFields.join(', ')}</p>` : ''}
                    ${result.sampleData ? `<p>示例数据: ${JSON.stringify(result.sampleData)}</p>` : ''}
                </div>
            `;
        }
    } catch (error) {
        console.error('上传失败:', error);
        resultDiv.innerHTML = `
            <div style="background: #f8d7da; color: #721c24; padding: 1rem; border-radius: 5px; border: 1px solid #f5c6cb;">
                <h4><i class="fas fa-exclamation-triangle"></i> 上传失败</h4>
                <p>网络错误，请稍后重试</p>
            </div>
        `;
    }
}

// 清空所有数据
async function clearAllData() {
    if (!confirm('确定要清空所有数据吗？此操作不可恢复！')) {
        return;
    }
    
    try {
        const response = await fetch('/api/universities', {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (response.ok) {
            alert('数据已清空');
            loadDataStats();
            loadDataPreview();
        } else {
            alert('清空数据失败: ' + result.error);
        }
    } catch (error) {
        console.error('清空数据失败:', error);
        alert('清空数据失败，请稍后重试');
    }
}

// 导出所有数据
async function exportAllData() {
    try {
        const response = await fetch('/api/universities?limit=10000');
        const data = await response.json();
        
        if (response.ok) {
            const csvContent = createCSV(data.universities);
            downloadCSV(csvContent, 'university_rankings_all.csv');
        } else {
            throw new Error(data.error || '导出数据失败');
        }
    } catch (error) {
        console.error('导出数据失败:', error);
        alert('导出数据失败，请稍后重试');
    }
}

// 创建CSV内容
function createCSV(universities) {
    const headers = [
        'Rank', 'University', 'Country', 'Research', 'Reputation', 'Employment', 
        'International', 'Total_Score', 'Star_Rating', 'year'
    ];
    
    const rows = universities.map(uni => [
        uni.rank,
        uni.university,
        uni.country,
        uni.research,
        uni.reputation,
        uni.employment,
        uni.international,
        uni.total_score,
        uni.star_rating,
        uni.year
    ]);
    
    return [headers, ...rows]
        .map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(','))
        .join('\n');
}

// 下载CSV文件
function downloadCSV(csvContent, filename) {
    const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// 加载数据统计
async function loadDataStats() {
    try {
        const response = await fetch('/api/universities?limit=1');
        const data = await response.json();
        
        if (response.ok) {
            const statsDiv = document.getElementById('dataStats');
            statsDiv.innerHTML = `
                <strong>总记录数:</strong> ${data.pagination.total}<br>
                <strong>年份范围:</strong> ${Math.min(...data.universities.map(u => u.year))} - ${Math.max(...data.universities.map(u => u.year))}
            `;
        }
    } catch (error) {
        console.error('加载数据统计失败:', error);
        document.getElementById('dataStats').innerHTML = '加载失败';
    }
}

// 加载数据预览
async function loadDataPreview() {
    try {
        const response = await fetch('/api/universities?limit=10');
        const data = await response.json();
        
        const previewDiv = document.getElementById('dataPreview');
        
        if (response.ok && data.universities.length > 0) {
            previewDiv.innerHTML = `
                <table class="table">
                    <thead>
                        <tr>
                            <th>排名</th>
                            <th>大学</th>
                            <th>国家</th>
                            <th>总分</th>
                            <th>星级</th>
                            <th>年份</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.universities.map(uni => `
                            <tr>
                                <td><span class="rank-badge ${uni.rank <= 3 ? `rank-${uni.rank}` : 'rank-other'}">${uni.rank}</span></td>
                                <td><strong>${uni.university}</strong></td>
                                <td>${uni.country}</td>
                                <td><strong>${uni.total_score.toFixed(1)}</strong></td>
                                <td>${uni.star_rating}</td>
                                <td>${uni.year}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
                <p style="text-align: center; margin-top: 1rem; color: #666;">
                    显示前10条记录，共 ${data.pagination.total} 条记录
                </p>
            `;
        } else {
            previewDiv.innerHTML = '<p style="text-align: center; padding: 2rem;">No data available in the database. Please import a file.</p>';
        }
    } catch (error) {
        console.error('加载数据预览失败:', error);
        document.getElementById('dataPreview').innerHTML = `
            <div style="text-align: center; padding: 2rem; color: #dc3545;">
                <i class="fas fa-exclamation-triangle" style="font-size: 3rem; margin-bottom: 1rem;"></i>
                <p>加载数据失败</p>
            </div>
        `;
    }
}

// 显示导入状态
function showStatus(message, type = 'info') {
    const statusDiv = document.getElementById('importStatus');
    statusDiv.textContent = message;
    statusDiv.className = `import-status ${type}`;
    
    setTimeout(() => {
        statusDiv.textContent = '';
        statusDiv.className = 'import-status';
    }, 5000);
}

// 导入2024年数据
async function import2024Data() {
    if (!confirm('确定要导入2024年数据吗？这将覆盖现有的2024年数据。')) {
        return;
    }
    
    const statusDiv = document.getElementById('sheetImportStatus');
    statusDiv.innerHTML = '<div class="loading"><div class="spinner"></div><span style="margin-left: 1rem;">正在导入2024年数据...</span></div>';
    
    try {
        const response = await fetch('/api/import-2024', {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (response.ok) {
            statusDiv.innerHTML = `
                <div style="background: #d4edda; color: #155724; padding: 1rem; border-radius: 5px; border: 1px solid #c3e6cb;">
                    <h4><i class="fas fa-check-circle"></i> 2024年数据导入成功</h4>
                    <p>${result.message}</p>
                    <p>导入记录数: ${result.count}</p>
                </div>
            `;
            
            // 刷新数据统计和预览
            loadDataStats();
            loadDataPreview();
        } else {
            statusDiv.innerHTML = `
                <div style="background: #f8d7da; color: #721c24; padding: 1rem; border-radius: 5px; border: 1px solid #f5c6cb;">
                    <h4><i class="fas fa-exclamation-triangle"></i> 2024年数据导入失败</h4>
                    <p>${result.error}</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('导入2024年数据失败:', error);
        statusDiv.innerHTML = `
            <div style="background: #f8d7da; color: #721c24; padding: 1rem; border-radius: 5px; border: 1px solid #f5c6cb;">
                <h4><i class="fas fa-exclamation-triangle"></i> 2024年数据导入失败</h4>
                <p>网络错误，请稍后重试</p>
            </div>
        `;
    }
}

// 导入2025年数据
async function import2025Data() {
    if (!confirm('确定要导入2025年数据吗？这将覆盖现有的2025年数据。')) {
        return;
    }
    
    const statusDiv = document.getElementById('sheetImportStatus');
    statusDiv.innerHTML = '<div class="loading"><div class="spinner"></div><span style="margin-left: 1rem;">正在导入2025年数据...</span></div>';
    
    try {
        const response = await fetch('/api/import', {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (response.ok) {
            statusDiv.innerHTML = `
                <div style="background: #d4edda; color: #155724; padding: 1rem; border-radius: 5px; border: 1px solid #c3e6cb;">
                    <h4><i class="fas fa-check-circle"></i> 2025年数据导入成功</h4>
                    <p>成功导入: ${result.successCount} 条记录</p>
                    <p>失败: ${result.errorCount} 条记录</p>
                    <p>总计: ${result.totalCount} 条记录</p>
                </div>
            `;
            
            // 刷新数据统计和预览
            loadDataStats();
            loadDataPreview();
        } else {
            statusDiv.innerHTML = `
                <div style="background: #f8d7da; color: #721c24; padding: 1rem; border-radius: 5px; border: 1px solid #f5c6cb;">
                    <h4><i class="fas fa-exclamation-triangle"></i> 2025年数据导入失败</h4>
                    <p>${result.error}</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('导入2025年数据失败:', error);
        statusDiv.innerHTML = `
            <div style="background: #f8d7da; color: #721c24; padding: 1rem; border-radius: 5px; border: 1px solid #f5c6cb;">
                <h4><i class="fas fa-exclamation-triangle"></i> 2025年数据导入失败</h4>
                <p>网络错误，请稍后重试</p>
            </div>
        `;
    }
}

// 初始加载
loadDataPreview(); 