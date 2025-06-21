# Wix网站设置步骤指南

## 🎯 第一步：创建Wix网站

### 1. 登录Wix账号
1. 访问 [Wix.com](https://www.wix.com)
2. 点击 "Sign In" 登录您的账号
3. 点击 "Create New Site"

### 2. 选择模板
1. 选择 "Start from scratch"
2. 点击 "Choose Template"
3. 选择 "Blank Template" 或任何简洁的模板

### 3. 进入编辑器
1. 点击 "Edit Site"
2. 进入Wix网站编辑器

## 🏗️ 第二步：创建页面结构

### 1. 添加页面
在左侧菜单中点击 "Pages" → "Add Page"：

**创建以下页面：**
- **Home** (主页 - About)
- **Rankings** (大学排名)
- **Methodology** (方法论)
- **DataLab** (Barentsz DataLab)
- **News** (新闻资讯)

### 2. 设置页面标题
为每个页面设置合适的标题和URL。

## 🔧 第三步：配置大学排名页面

### 1. 编辑Rankings页面
1. 点击 "Rankings" 页面
2. 清空页面内容（删除默认元素）

### 2. 添加HTML嵌入
1. 在左侧工具栏中找到 "Embed" → "HTML"
2. 拖拽到页面中央
3. 点击 "Enter Code"
4. 粘贴我们提供的HTML代码

### 3. 修改API地址
在HTML代码中找到这一行：
```javascript
const API_BASE_URL = 'https://your-app-name.railway.app';
```
将其替换为您的Railway域名。

## 🎨 第四步：设计其他页面

### 1. Home页面（About）
1. 添加标题："About Uni-Ranking"
2. 添加文本内容（从index.html复制）
3. 添加Logo和图片

### 2. Methodology页面
1. 添加标题："Our Methodology"
2. 创建网格布局显示四个指标
3. 添加详细说明

### 3. DataLab页面
1. 添加标题："Barentsz DataLab"
2. 添加功能介绍
3. 添加相关链接

### 4. News页面
1. 添加标题："News & Insights"
2. 创建新闻卡片布局
3. 添加示例新闻内容

## 🔗 第五步：配置导航菜单

### 1. 编辑导航菜单
1. 点击页面顶部的导航菜单
2. 点击 "Edit Menu"
3. 添加所有页面链接

### 2. 设置下拉菜单
为"World University Ranking"添加下拉菜单：
- 2025 Ranking
- 2024 Ranking

## 📱 第六步：移动端优化

### 1. 切换到移动端视图
1. 点击编辑器顶部的手机图标
2. 检查所有页面在移动端的显示

### 2. 调整布局
1. 调整文字大小和间距
2. 确保表格可以水平滚动
3. 优化按钮和表单元素

## 🌐 第七步：配置域名

### 1. 连接您的域名
1. 点击 "Settings" → "Domains"
2. 点击 "Connect Domain"
3. 选择 "I own a domain"
4. 输入您的域名

### 2. 设置DNS记录
按照Wix的指示设置DNS记录：
- 添加CNAME记录
- 等待DNS传播（可能需要24小时）

## ✅ 第八步：测试和发布

### 1. 预览网站
1. 点击 "Preview" 按钮
2. 测试所有页面和功能
3. 检查API连接是否正常

### 2. 发布网站
1. 点击 "Publish" 按钮
2. 确认发布设置
3. 网站正式上线

## 🔧 常见问题解决

### 1. HTML嵌入不显示
- 检查HTML代码语法
- 确保API地址正确
- 查看浏览器控制台错误

### 2. API调用失败
- 确认Railway服务正常运行
- 检查CORS设置
- 验证API端点URL

### 3. 移动端显示问题
- 使用Wix的移动端编辑器
- 调整元素大小和位置
- 测试不同设备尺寸

## 📞 技术支持

### Wix支持
- 在线聊天：在Wix编辑器中点击 "Help"
- 视频教程：Wix学习中心
- 社区论坛：Wix社区

### 技术文档
- 查看我们提供的部署文档
- 检查Railway部署状态
- 监控API响应时间

---

**完成这些步骤后，您的大学排名网站就正式上线了！** 