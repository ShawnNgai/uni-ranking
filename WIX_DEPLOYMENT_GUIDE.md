# Wix部署指南

## 🎯 部署方案概述

由于Wix主要支持静态网站，我们需要将后端和前端分离部署：

### 架构设计
```
┌─────────────────┐    API调用    ┌─────────────────┐
│   Wix前端网站   │ ────────────→ │   外部后端API   │
│  (静态HTML/CSS) │               │  (Node.js/DB)   │
└─────────────────┘               └─────────────────┘
```

## 🚀 步骤一：部署后端到免费平台

### 选择平台：Railway（推荐）
1. 访问 [Railway.app](https://railway.app)
2. 使用GitHub账号登录
3. 创建新项目
4. 连接您的GitHub仓库

### 环境配置
在Railway项目设置中添加环境变量：
```
NODE_ENV=production
PORT=3000
```

### 部署命令
Railway会自动检测package.json并部署Node.js应用。

## 🎨 步骤二：创建Wix网站

### 1. 注册Wix账号
- 访问 [Wix.com](https://www.wix.com)
- 选择"创建网站"
- 选择"空白模板"

### 2. 上传静态文件
由于Wix不支持直接上传HTML文件，我们需要：
- 将HTML内容转换为Wix页面
- 使用Wix的HTML嵌入功能

### 3. 页面结构
```
主页 (About)
├── 大学排名页面
├── 方法论页面
├── Barentsz DataLab页面
└── 新闻页面
```

## 🔧 步骤三：集成API

### 1. 修改API地址
在Wix的HTML嵌入代码中，将API_BASE_URL改为您的Railway域名：
```javascript
const API_BASE_URL = 'https://your-app-name.railway.app';
```

### 2. 处理CORS问题
在server.js中添加CORS支持：
```javascript
const cors = require('cors');
app.use(cors({
    origin: ['https://your-wix-domain.wixsite.com', 'https://your-custom-domain.com']
}));
```

## 📱 步骤四：移动端优化

### Wix响应式设计
- 使用Wix的响应式编辑器
- 确保所有页面在移动端正常显示
- 测试表格的滚动功能

## 🔒 步骤五：域名配置

### 1. 购买域名
- 在Wix购买域名，或
- 在其他平台购买后指向Wix

### 2. SSL证书
- Wix自动提供SSL证书
- 确保HTTPS访问

## 💰 成本对比

### Wix方案成本
- **Wix网站**: $14-23/月（包含域名）
- **Railway后端**: 免费（每月有限额）
- **总计**: $14-23/月

### 优势
- ✅ 无需服务器管理
- ✅ 自动SSL证书
- ✅ 内置CDN
- ✅ 拖拽式编辑器
- ✅ 24/7技术支持

## 🛠️ 技术注意事项

### 1. API限制
- Wix对API调用有频率限制
- 建议实现客户端缓存
- 考虑使用CDN缓存静态数据

### 2. 数据库选择
- Railway支持PostgreSQL（免费）
- 或继续使用SQLite（文件存储）

### 3. 文件上传
- Wix不支持文件上传到外部服务器
- 管理功能需要单独部署

## 📋 部署检查清单

### 后端部署
- [ ] Railway项目创建成功
- [ ] 环境变量配置正确
- [ ] 数据库连接正常
- [ ] API端点测试通过
- [ ] CORS配置正确

### Wix前端
- [ ] 页面结构创建完成
- [ ] API地址配置正确
- [ ] 移动端响应式测试
- [ ] 域名配置完成
- [ ] SSL证书生效

### 功能测试
- [ ] 排名数据加载正常
- [ ] 筛选功能工作正常
- [ ] 分页功能正常
- [ ] 移动端表格滚动正常
- [ ] 所有页面链接正常

## 🚨 潜在问题及解决方案

### 1. CORS错误
```javascript
// 在server.js中添加
app.use(cors({
    origin: true, // 开发时允许所有域名
    credentials: true
}));
```

### 2. API调用失败
- 检查Railway域名是否正确
- 确认环境变量配置
- 查看Railway日志

### 3. 移动端显示问题
- 使用Wix的移动端编辑器
- 测试不同设备尺寸
- 调整表格布局

## 📞 技术支持

### Wix支持
- 在线聊天支持
- 视频教程
- 社区论坛

### Railway支持
- Discord社区
- 文档完善
- GitHub Issues

---

**推荐工作流程：**
1. 先部署后端到Railway
2. 测试API是否正常工作
3. 创建Wix网站基础结构
4. 集成API并测试功能
5. 配置域名和SSL
6. 最终测试和优化 