# Wix域名配置指南

## 方案选择

### 方案1：Wix域名 + 外部服务器（推荐）
- **优点**：完全控制，性能好，成本低
- **缺点**：需要自己管理服务器
- **适合**：有技术背景的用户

### 方案2：Wix代理转发
- **优点**：操作简单，Wix管理
- **缺点**：可能有延迟，功能受限
- **适合**：新手用户

## 方案1详细步骤

### 步骤1：购买域名
1. 登录Wix账户
2. 进入"域名"管理页面
3. 搜索并购买域名
4. 完成支付和激活

### 步骤2：配置DNS记录
在Wix域名管理后台添加以下记录：

#### A记录（主域名）
```
类型: A
名称: @ (或留空)
值: [您的服务器IP地址]
TTL: 3600
```

#### A记录（WWW子域名）
```
类型: A
名称: www
值: [您的服务器IP地址]
TTL: 3600
```

#### CNAME记录（可选）
```
类型: CNAME
名称: www
值: your-domain.com
TTL: 3600
```

### 步骤3：服务器配置
确保您的服务器已正确配置：

1. **Nginx配置**：
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    location / {
        proxy_pass http://localhost:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

2. **SSL证书**：
```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### 步骤4：验证配置
```bash
# 检查DNS解析
nslookup your-domain.com
dig your-domain.com

# 检查网站访问
curl -I http://your-domain.com
curl -I https://your-domain.com
```

## 方案2详细步骤

### 步骤1：创建Wix网站
1. 创建新网站
2. 选择空白模板
3. 发布网站

### 步骤2：添加重定向代码
在Wix编辑器中添加HTML元素，插入以下代码：

```html
<!DOCTYPE html>
<html>
<head>
    <title>重定向到Barentsz Uni-Ranking</title>
    <meta http-equiv="refresh" content="0; url=http://your-server-ip:3001">
</head>
<body>
    <script>
        window.location.href = "http://your-server-ip:3001";
    </script>
    <p>正在跳转到 Barentsz Uni-Ranking...</p>
</body>
</html>
```

### 步骤3：配置域名
1. 在Wix中添加您的域名
2. 设置DNS解析到Wix服务器
3. 等待DNS生效

## 常见问题解决

### 问题1：DNS解析不生效
**解决方案**：
- 检查DNS记录配置是否正确
- 等待更长时间（最多24小时）
- 清除本地DNS缓存

### 问题2：网站无法访问
**解决方案**：
- 检查服务器防火墙设置
- 确认Nginx配置正确
- 检查应用是否正常运行

### 问题3：SSL证书问题
**解决方案**：
- 确保域名DNS已生效
- 重新申请SSL证书
- 检查Nginx SSL配置

## 推荐配置

### 最佳实践：
1. **使用方案1**：Wix域名 + 外部服务器
2. **配置SSL证书**：确保HTTPS访问
3. **设置CDN**：提高访问速度
4. **定期备份**：保护数据安全

### 监控建议：
- 设置域名监控
- 配置错误告警
- 定期检查SSL证书状态

## 联系支持

如果遇到问题，可以联系：
- **Wix支持**：域名相关问题
- **服务器提供商**：服务器配置问题
- **技术团队**：应用相关问题 