# Railway部署步骤指南

## 🎯 第一步：准备GitHub仓库

### 1. 创建GitHub仓库
1. 访问 [GitHub.com](https://github.com)
2. 点击 "New repository"
3. 仓库名称：`uni-ranking`
4. 选择 "Public"
5. 点击 "Create repository"

### 2. 上传代码到GitHub
```bash
# 在您的项目目录中执行
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/uni-ranking.git
git push -u origin main
```

## 🚀 第二步：部署到Railway

### 1. 注册Railway账号
1. 访问 [Railway.app](https://railway.app)
2. 点击 "Start a New Project"
3. 选择 "Deploy from GitHub repo"
4. 使用GitHub账号登录

### 2. 连接GitHub仓库
1. 在Railway中选择您的 `uni-ranking` 仓库
2. 点击 "Deploy Now"
3. Railway会自动检测Node.js项目并开始部署

### 3. 配置环境变量
在Railway项目设置中：
1. 点击项目名称
2. 选择 "Variables" 标签
3. 添加以下环境变量：
   ```
   NODE_ENV=production
   PORT=3000
   ```

### 4. 获取部署域名
1. 部署完成后，Railway会提供一个域名
2. 格式类似：`https://uni-ranking-production-xxxx.up.railway.app`
3. 复制这个域名，稍后在Wix中使用

## ✅ 第三步：测试API

### 1. 测试API端点
在浏览器中访问以下URL测试：
- `https://your-railway-domain.up.railway.app/api/countries`
- `https://your-railway-domain.up.railway.app/api/universities?limit=5`

### 2. 检查数据
确保API返回正确的JSON数据格式。

## 📝 重要提示

### 数据库文件
- SQLite数据库文件会自动创建
- 2024年数据会在首次启动时自动导入
- 数据库文件存储在Railway的临时存储中

### 日志查看
- 在Railway项目页面查看部署日志
- 如果部署失败，检查package.json和依赖项

### 免费额度
- Railway免费层每月有使用限制
- 监控使用情况避免超出免费额度

---

**下一步：配置Wix网站**
完成Railway部署后，我们将继续配置Wix前端。 