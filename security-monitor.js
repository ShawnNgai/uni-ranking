// 安全监控脚本
const fs = require('fs');
const path = require('path');

class SecurityMonitor {
    constructor() {
        this.logFile = path.join(__dirname, 'logs/security.log');
        this.alertFile = path.join(__dirname, 'logs/alerts.log');
        this.stats = {
            totalRequests: 0,
            blockedRequests: 0,
            suspiciousIPs: new Set(),
            errorCount: 0,
            lastAlert: null
        };
        
        this.ensureLogDirectory();
    }
    
    ensureLogDirectory() {
        const logDir = path.dirname(this.logFile);
        if (!fs.existsSync(logDir)) {
            fs.mkdirSync(logDir, { recursive: true });
        }
    }
    
    logSecurityEvent(event) {
        const logEntry = {
            timestamp: new Date().toISOString(),
            ...event
        };
        
        fs.appendFileSync(this.logFile, JSON.stringify(logEntry) + '\n');
        
        // 更新统计
        this.stats.totalRequests++;
        if (event.type === 'blocked') {
            this.stats.blockedRequests++;
        }
        if (event.suspicious) {
            this.stats.suspiciousIPs.add(event.ip);
        }
    }
    
    logAlert(alert) {
        const alertEntry = {
            timestamp: new Date().toISOString(),
            level: 'ALERT',
            ...alert
        };
        
        fs.appendFileSync(this.alertFile, JSON.stringify(alertEntry) + '\n');
        this.stats.lastAlert = new Date();
        
        // 控制台输出警报
        console.error('🚨 安全警报:', alert);
    }
    
    checkAnomalies() {
        const now = new Date();
        const oneHourAgo = new Date(now.getTime() - 60 * 60 * 1000);
        
        // 检查异常模式
        if (this.stats.blockedRequests > 10) {
            this.logAlert({
                type: 'high_blocked_requests',
                message: `检测到大量被阻止的请求: ${this.stats.blockedRequests}`,
                threshold: 10,
                actual: this.stats.blockedRequests
            });
        }
        
        if (this.stats.suspiciousIPs.size > 5) {
            this.logAlert({
                type: 'multiple_suspicious_ips',
                message: `检测到多个可疑IP地址: ${this.stats.suspiciousIPs.size}`,
                ips: Array.from(this.stats.suspiciousIPs)
            });
        }
        
        if (this.stats.errorCount > 20) {
            this.logAlert({
                type: 'high_error_rate',
                message: `检测到高错误率: ${this.stats.errorCount} 个错误`,
                threshold: 20,
                actual: this.stats.errorCount
            });
        }
    }
    
    getSecurityReport() {
        return {
            timestamp: new Date().toISOString(),
            stats: {
                totalRequests: this.stats.totalRequests,
                blockedRequests: this.stats.blockedRequests,
                suspiciousIPs: this.stats.suspiciousIPs.size,
                errorCount: this.stats.errorCount,
                blockRate: this.stats.totalRequests > 0 ? 
                    (this.stats.blockedRequests / this.stats.totalRequests * 100).toFixed(2) + '%' : '0%'
            },
            lastAlert: this.stats.lastAlert,
            status: this.getSecurityStatus()
        };
    }
    
    getSecurityStatus() {
        const blockRate = this.stats.totalRequests > 0 ? 
            this.stats.blockedRequests / this.stats.totalRequests : 0;
        
        if (blockRate > 0.1) {
            return 'HIGH_RISK';
        } else if (blockRate > 0.05) {
            return 'MEDIUM_RISK';
        } else {
            return 'LOW_RISK';
        }
    }
    
    resetStats() {
        this.stats = {
            totalRequests: 0,
            blockedRequests: 0,
            suspiciousIPs: new Set(),
            errorCount: 0,
            lastAlert: null
        };
    }
}

// 创建全局安全监控实例
const securityMonitor = new SecurityMonitor();

// 定期检查异常
setInterval(() => {
    securityMonitor.checkAnomalies();
}, 5 * 60 * 1000); // 每5分钟检查一次

// 定期重置统计（每天）
setInterval(() => {
    securityMonitor.resetStats();
}, 24 * 60 * 60 * 1000); // 每24小时重置一次

module.exports = securityMonitor; 