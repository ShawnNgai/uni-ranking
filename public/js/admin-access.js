// 隐藏的Admin访问脚本
// 使用方法：在浏览器控制台中输入 adminAccess() 即可访问admin页面

let accessAttempts = 0;
const maxAttempts = 3;

function adminAccess() {
    accessAttempts++;
    
    if (accessAttempts > maxAttempts) {
        console.log('Access denied. Too many attempts.');
        return;
    }
    
    // 检查是否在正确的域名下
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        // 本地开发环境，直接访问
        window.location.href = '/admin?key=barentsz2024';
    } else {
        // 生产环境，需要额外的验证
        const password = prompt('Enter admin password:');
        if (password === 'barentsz2024') {
            window.location.href = '/admin?key=barentsz2024';
        } else {
            console.log('Access denied.');
        }
    }
}

// 添加键盘快捷键（Ctrl+Shift+A）
document.addEventListener('keydown', function(event) {
    if (event.ctrlKey && event.shiftKey && event.key === 'A') {
        event.preventDefault();
        adminAccess();
    }
});

// 在控制台中显示提示
console.log('Admin access available. Type adminAccess() or press Ctrl+Shift+A'); 