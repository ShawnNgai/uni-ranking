const rateLimit = require('express-rate-limit');
const hpp = require('hpp');
const xss = require('xss-clean');
const { validationRules } = require('../security-config');

// 输入验证中间件
function validateInput(req, res, next) {
    const errors = [];
    
    // 验证查询参数
    if (req.query.search) {
        const search = req.query.search;
        if (search.length < validationRules.university.minLength || 
            search.length > validationRules.university.maxLength) {
            errors.push('搜索关键词长度无效');
        }
        if (!validationRules.university.pattern.test(search)) {
            errors.push('搜索关键词包含无效字符');
        }
    }
    
    if (req.query.country) {
        const country = req.query.country;
        if (country.length < validationRules.country.minLength || 
            country.length > validationRules.country.maxLength) {
            errors.push('国家名称长度无效');
        }
        if (!validationRules.country.pattern.test(country)) {
            errors.push('国家名称包含无效字符');
        }
    }
    
    if (req.query.year) {
        const year = parseInt(req.query.year);
        if (isNaN(year) || year < validationRules.year.min || year > validationRules.year.max) {
            errors.push('年份无效');
        }
    }
    
    if (req.query.rank) {
        const rank = parseInt(req.query.rank);
        if (isNaN(rank) || rank < validationRules.rank.min || rank > validationRules.rank.max) {
            errors.push('排名无效');
        }
    }
    
    if (errors.length > 0) {
        return res.status(400).json({
            error: '输入验证失败',
            details: errors
        });
    }
    
    next();
}

// SQL注入防护中间件
function sqlInjectionProtection(req, res, next) {
    const sqlPattern = /(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION|SCRIPT)\b)/i;
    
    const checkValue = (value) => {
        if (typeof value === 'string' && sqlPattern.test(value)) {
            return true;
        }
        return false;
    };
    
    // 检查查询参数
    for (let key in req.query) {
        if (checkValue(req.query[key])) {
            return res.status(403).json({
                error: '检测到潜在的安全威胁',
                message: '请求被安全系统阻止'
            });
        }
    }
    
    // 检查请求体
    if (req.body) {
        for (let key in req.body) {
            if (checkValue(req.body[key])) {
                return res.status(403).json({
                    error: '检测到潜在的安全威胁',
                    message: '请求被安全系统阻止'
                });
            }
        }
    }
    
    next();
}

// 请求日志中间件
function requestLogger(req, res, next) {
    const start = Date.now();
    
    res.on('finish', () => {
        const duration = Date.now() - start;
        const logData = {
            timestamp: new Date().toISOString(),
            method: req.method,
            url: req.url,
            status: res.statusCode,
            duration: `${duration}ms`,
            ip: req.ip || req.connection.remoteAddress,
            userAgent: req.get('User-Agent')
        };
        
        // 记录安全相关事件
        if (res.statusCode >= 400) {
            console.warn('安全警告:', logData);
        } else {
            console.log('访问日志:', logData);
        }
    });
    
    next();
}

// 异常检测中间件
function anomalyDetection(req, res, next) {
    // 检测异常请求模式
    const suspiciousPatterns = [
        /\.\.\//, // 路径遍历
        /<script/i, // XSS尝试
        /javascript:/i, // JavaScript协议
        /data:text\/html/i, // 数据URI
        /on\w+\s*=/i, // 事件处理器
    ];
    
    const url = req.url.toLowerCase();
    const userAgent = req.get('User-Agent') || '';
    
    for (let pattern of suspiciousPatterns) {
        if (pattern.test(url) || pattern.test(userAgent)) {
            console.warn('检测到可疑请求:', {
                url: req.url,
                userAgent: userAgent,
                ip: req.ip,
                timestamp: new Date().toISOString()
            });
            
            return res.status(403).json({
                error: '请求被安全系统阻止',
                message: '检测到可疑活动'
            });
        }
    }
    
    next();
}

// 文件上传安全检查
function fileUploadSecurity(req, res, next) {
    if (!req.file) {
        return next();
    }
    
    const allowedTypes = [
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'text/csv'
    ];
    
    const maxSize = 5 * 1024 * 1024; // 5MB
    
    if (!allowedTypes.includes(req.file.mimetype)) {
        return res.status(400).json({
            error: '不支持的文件类型',
            message: '只允许上传Excel或CSV文件'
        });
    }
    
    if (req.file.size > maxSize) {
        return res.status(400).json({
            error: '文件过大',
            message: '文件大小不能超过5MB'
        });
    }
    
    next();
}

// 健康检查端点
function healthCheck(req, res) {
    const health = {
        status: 'healthy',
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        memory: process.memoryUsage(),
        version: process.version
    };
    
    res.status(200).json(health);
}

module.exports = {
    validateInput,
    sqlInjectionProtection,
    requestLogger,
    anomalyDetection,
    fileUploadSecurity,
    healthCheck
}; 