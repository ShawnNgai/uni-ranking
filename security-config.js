// 安全配置文件
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const hpp = require('hpp');
const xss = require('xss-clean');

// 安全中间件配置
const securityConfig = {
    // Helmet 安全头配置
    helmet: helmet({
        contentSecurityPolicy: {
            directives: {
                defaultSrc: ["'self'"],
                styleSrc: ["'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com"],
                scriptSrc: ["'self'", "'unsafe-inline'"],
                imgSrc: ["'self'", "data:", "https:"],
                fontSrc: ["'self'", "https://cdnjs.cloudflare.com"],
                connectSrc: ["'self'"],
                frameSrc: ["'none'"],
                objectSrc: ["'none'"],
                upgradeInsecureRequests: []
            }
        },
        hsts: {
            maxAge: 31536000,
            includeSubDomains: true,
            preload: true
        },
        noSniff: true,
        referrerPolicy: { policy: 'strict-origin-when-cross-origin' }
    }),

    // 速率限制配置
    rateLimit: {
        windowMs: 15 * 60 * 1000, // 15分钟
        max: 100, // 限制每个IP 15分钟内最多100个请求
        message: {
            error: '请求过于频繁，请稍后再试',
            retryAfter: '15分钟'
        },
        standardHeaders: true,
        legacyHeaders: false
    },

    // API速率限制（更严格）
    apiRateLimit: {
        windowMs: 15 * 60 * 1000, // 15分钟
        max: 50, // API请求限制更严格
        message: {
            error: 'API请求过于频繁',
            retryAfter: '15分钟'
        }
    },

    // 文件上传限制
    uploadLimit: {
        windowMs: 60 * 60 * 1000, // 1小时
        max: 10, // 每小时最多10个文件上传
        message: {
            error: '文件上传过于频繁',
            retryAfter: '1小时'
        }
    }
};

// 输入验证规则
const validationRules = {
    university: {
        minLength: 2,
        maxLength: 200,
        pattern: /^[a-zA-Z0-9\s\-\.\(\)]+$/
    },
    country: {
        minLength: 2,
        maxLength: 100,
        pattern: /^[a-zA-Z\s\-]+$/
    },
    year: {
        min: 2020,
        max: 2030
    },
    rank: {
        min: 1,
        max: 10000
    },
    score: {
        min: 0,
        max: 100
    }
};

// 日志配置
const logConfig = {
    // 安全事件日志
    security: {
        enabled: true,
        level: 'warn',
        format: 'combined'
    },
    
    // 访问日志
    access: {
        enabled: true,
        level: 'info',
        format: 'combined'
    },
    
    // 错误日志
    error: {
        enabled: true,
        level: 'error',
        format: 'combined'
    }
};

// 监控配置
const monitoringConfig = {
    // 异常检测
    anomaly: {
        enabled: true,
        threshold: {
            requestsPerMinute: 100,
            errorRate: 0.1, // 10%错误率
            responseTime: 5000 // 5秒
        }
    },
    
    // 健康检查
    healthCheck: {
        enabled: true,
        interval: 30000, // 30秒
        timeout: 5000 // 5秒
    }
};

module.exports = {
    securityConfig,
    validationRules,
    logConfig,
    monitoringConfig
}; 