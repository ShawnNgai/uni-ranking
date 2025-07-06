// 移动端性能优化脚本
(function() {
    'use strict';
    
    // 检测移动设备
    function isMobileDevice() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
               window.innerWidth <= 768;
    }
    
    // 检测网络连接
    function isSlowConnection() {
        return navigator.connection && (
            navigator.connection.effectiveType === 'slow-2g' ||
            navigator.connection.effectiveType === '2g' ||
            navigator.connection.effectiveType === '3g'
        );
    }
    
    // 移动端优化
    function optimizeForMobile() {
        if (!isMobileDevice()) return;
        
        console.log('应用移动端优化...');
        
        // 禁用不必要的动画
        const style = document.createElement('style');
        style.textContent = `
            @media (max-width: 768px) {
                .fade-in { animation: none !important; }
                .card { transition: none !important; }
                .btn { transition: none !important; }
            }
        `;
        document.head.appendChild(style);
        
        // 预加载关键资源
        if (!isSlowConnection()) {
            const preloadLinks = [
                '/api/mobile-universities?limit=5&sortBy=rank&sortOrder=ASC&year=2025'
            ];
            
            preloadLinks.forEach(url => {
                const link = document.createElement('link');
                link.rel = 'prefetch';
                link.href = url;
                document.head.appendChild(link);
            });
        }
        
        // 优化图片加载
        const images = document.querySelectorAll('img');
        images.forEach(img => {
            img.loading = 'lazy';
        });
        
        // 减少重绘和回流
        const cards = document.querySelectorAll('.card');
        cards.forEach(card => {
            card.style.willChange = 'auto';
        });
    }
    
    // 错误处理优化
    function setupErrorHandling() {
        window.addEventListener('error', function(e) {
            console.error('页面错误:', e.error);
            
            // 如果是移动端数据加载错误，尝试使用默认数据
            if (e.error && e.error.message && e.error.message.includes('fetch')) {
                console.log('尝试使用默认数据...');
                // 这里可以触发默认数据加载
            }
        });
        
        window.addEventListener('unhandledrejection', function(e) {
            console.error('未处理的Promise拒绝:', e.reason);
        });
    }
    
    // 性能监控
    function setupPerformanceMonitoring() {
        if ('performance' in window) {
            window.addEventListener('load', function() {
                setTimeout(function() {
                    const perfData = performance.getEntriesByType('navigation')[0];
                    console.log('页面加载性能:', {
                        domContentLoaded: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
                        loadComplete: perfData.loadEventEnd - perfData.loadEventStart,
                        totalTime: perfData.loadEventEnd - perfData.fetchStart
                    });
                }, 0);
            });
        }
    }
    
    // 初始化
    function init() {
        optimizeForMobile();
        setupErrorHandling();
        setupPerformanceMonitoring();
        
        // 添加移动端标识
        if (isMobileDevice()) {
            document.body.classList.add('mobile-device');
        }
    }
    
    // 页面加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // 导出函数供其他脚本使用
    window.MobileOptimizer = {
        isMobileDevice: isMobileDevice,
        isSlowConnection: isSlowConnection,
        optimizeForMobile: optimizeForMobile
    };
    
})(); 