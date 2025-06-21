# Barentsz Uni-Ranking 部署指南

## 部署前准备

### 1. 环境要求
- **Node.js**: 版本 16.0 或更高
- **npm**: 版本 8.0 或更高
- **操作系统**: Windows, macOS, Linux
- **内存**: 最少 512MB RAM
- **存储**: 最少 100MB 可用空间

### 2. 检查环境
```bash
node --version
npm --version
```

## 本地部署

### 1. 安装依赖
```bash
npm install
```

### 2. 启动服务器
```bash
node server.js
```

### 3. 访问网站
打开浏览器访问: `http://localhost:3001`

## 生产环境部署

### 1. 服务器准备
- 确保服务器已安装 Node.js
- 配置防火墙开放端口 3001
- 准备域名和SSL证书（推荐）

### 2. 文件上传
将以下文件和目录上传到服务器：
```
├── package.json
├── package-lock.json
├── server.js
├── README.md
├── public/
├── database/
├── data/
└── uploads/
```

### 3. 安装依赖
```bash
npm install --production
```

### 4. 配置环境变量（可选）
创建 `.env` 文件：
```env
PORT=3001
NODE_ENV=production
```

### 5. 使用PM2管理进程（推荐）
```bash
# 安装PM2
npm install -g pm2

# 启动应用
pm2 start server.js --name "barentsz-uni-ranking"

# 设置开机自启
pm2 startup
pm2 save

# 查看状态
pm2 status
pm2 logs barentsz-uni-ranking
```

### 6. 使用Nginx反向代理（推荐）
创建Nginx配置文件：
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## 数据库管理

### 1. 数据库备份
```bash
# 备份数据库
cp database/rankings.db database/rankings_backup_$(date +%Y%m%d_%H%M%S).db
```

### 2. 数据库恢复
```bash
# 恢复数据库
cp database/rankings_backup_YYYYMMDD_HHMMSS.db database/rankings.db
```

## 安全配置

### 1. 防火墙设置
```bash
# 只开放必要端口
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### 2. SSL证书配置
使用Let's Encrypt免费SSL证书：
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 3. 定期备份
创建自动备份脚本：
```bash
#!/bin/bash
# 备份脚本
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/barentsz-uni-ranking"
mkdir -p $BACKUP_DIR
cp -r /path/to/project $BACKUP_DIR/backup_$DATE
```

## 监控和维护

### 1. 日志监控
```bash
# 查看应用日志
pm2 logs barentsz-uni-ranking

# 查看系统日志
sudo journalctl -u nginx
```

### 2. 性能监控
```bash
# 查看系统资源
htop
df -h
free -h
```

### 3. 定期更新
```bash
# 更新依赖
npm update

# 重启应用
pm2 restart barentsz-uni-ranking
```

## 故障排除

### 1. 常见问题
- **端口被占用**: 修改 `server.js` 中的端口号
- **数据库连接失败**: 检查数据库文件权限
- **文件上传失败**: 检查 `uploads` 目录权限

### 2. 日志分析
```bash
# 查看错误日志
pm2 logs barentsz-uni-ranking --err

# 查看实时日志
pm2 logs barentsz-uni-ranking --lines 100
```

## 扩展部署

### 1. 负载均衡
使用多个实例：
```bash
pm2 start server.js -i max --name "barentsz-uni-ranking"
```

### 2. 数据库优化
- 考虑迁移到 PostgreSQL 或 MySQL
- 配置数据库连接池
- 实施数据库分片

### 3. 缓存策略
- 实施 Redis 缓存
- 配置静态文件缓存
- 启用 Gzip 压缩

## 联系信息
- **技术支持**: info@uni-ranking.com
- **文档更新**: 2025-01-27
- **版本**: 1.0.0 