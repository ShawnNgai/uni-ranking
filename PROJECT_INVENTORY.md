# Barentsz Uni-Ranking 项目清单

## 项目概述
- **项目名称**: Barentsz Uni-Ranking
- **版本**: 1.0.0
- **创建时间**: 2025-01-27
- **技术栈**: Node.js, Express, SQLite, HTML5, CSS3, JavaScript

## 核心文件

### 配置文件
- `package.json` - 项目配置和依赖管理
- `package-lock.json` - 依赖版本锁定
- `README.md` - 项目说明文档

### 服务器文件
- `server.js` - 主服务器文件 (19KB, 598行)
- `test_api.js` - API测试文件 (1KB, 31行)

## 前端文件 (public/)

### HTML页面
- `index.html` - 主页 (About Us)
- `rankings.html` - 大学排名页面
- `methodology.html` - 方法论页面
- `rating-system.html` - Barentsz DataLab页面
- `media.html` - 新闻与见解页面
- `admin.html` - 管理页面

### 样式文件
- `css/style.css` - 主样式文件 (包含Logo样式)

### JavaScript文件
- `js/main.js` - 主要JavaScript功能
- `js/nav.js` - 导航栏功能
- `js/rankings.js` - 排名页面功能
- `js/admin.js` - 管理页面功能
- `js/admin-access.js` - 管理访问控制

### 图片和Logo文件
- `images/logo.svg` - SVG版本Logo
- `images/logo.png` - PNG版本Logo (占位符)
- `images/logo-guidelines.md` - Logo使用指南

## 数据文件

### 数据库
- `database/rankings.db` - SQLite数据库文件

### 数据源
- `data/sample_data.csv` - 示例数据文件

### 上传文件
- `uploads/` - 文件上传目录

## 备份文件
- `backup_project.ps1` - PowerShell备份脚本
- `backup.bat` - 批处理备份脚本

## 项目特性

### 功能特性
1. **大学排名展示** - 支持2024和2025年数据
2. **数据筛选和排序** - 多维度筛选功能
3. **分页显示** - 支持大量数据分页
4. **数据管理** - 文件上传和数据导入
5. **管理界面** - 管理员功能
6. **响应式设计** - 适配各种设备

### 技术特性
1. **RESTful API** - 完整的后端API
2. **SQLite数据库** - 轻量级数据存储
3. **文件上传** - 支持CSV文件导入
4. **自动数据导入** - 服务器启动时自动导入数据
5. **安全访问控制** - 管理页面访问控制

### 设计特性
1. **现代UI设计** - 美观的用户界面
2. **Barentsz品牌Logo** - 独特的品牌标识
3. **响应式布局** - 适配桌面和移动设备
4. **专业配色方案** - 蓝色主题配色

## 部署信息

### 服务器配置
- **端口**: 3001 (可配置)
- **数据库**: SQLite
- **静态文件**: Express静态文件服务
- **文件上传**: Multer中间件

### 依赖包
- express: ^4.18.2
- sqlite3: ^5.1.6
- multer: ^1.4.5-lts.1
- csv-parser: ^3.0.0
- axios: ^1.5.0

## 安全特性
1. **管理页面隐藏** - 通过特殊URL访问
2. **文件类型验证** - 只允许CSV文件上传
3. **数据验证** - 输入数据验证和清理
4. **错误处理** - 完善的错误处理机制

## 维护信息
- **最后更新**: 2025-01-27
- **状态**: 准备部署
- **备份状态**: 需要手动备份
- **测试状态**: 功能测试通过

## 部署建议
1. 确保Node.js环境已安装
2. 运行 `npm install` 安装依赖
3. 配置环境变量（如需要）
4. 运行 `node server.js` 启动服务器
5. 访问 `http://localhost:3001` 查看网站

## 注意事项
- 数据库文件包含敏感数据，需要安全保护
- 管理页面需要特殊访问方式
- 建议定期备份数据库文件
- 生产环境部署前需要安全配置 