# Wix简化部署指南

## 🎯 方案优势
- ✅ 无需部署后端
- ✅ 无需GitHub和Railway
- ✅ 完全在Wix内完成
- ✅ 成本更低
- ✅ 设置更简单

## 🚀 第一步：创建Wix网站

### 1. 登录Wix账号
1. 访问 [Wix.com](https://www.wix.com)
2. 点击 "Sign In" 登录您的账号
3. 点击 "Create New Site"

### 2. 选择模板
1. 选择 "Start from scratch"
2. 点击 "Choose Template"
3. 选择 "Blank Template"

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
4. 复制粘贴我们提供的完整HTML代码

### 3. 调整嵌入框大小
1. 点击嵌入框
2. 调整宽度为100%
3. 调整高度为合适大小

## 🎨 第四步：设计其他页面

### 1. Home页面（About）
1. 添加标题："About Uni-Ranking"
2. 添加文本内容：
   ```
   Welcome to Uni-Ranking, your comprehensive guide to world university rankings. 
   We provide objective, data-driven insights to help students, researchers, and 
   institutions understand global higher education excellence.
   
   Our ranking system evaluates universities across multiple dimensions including 
   research output, academic reputation, graduate employment outcomes, and 
   international collaboration.
   ```

### 2. Methodology页面
1. 添加标题："Our Methodology"
2. 创建四个卡片显示指标：
   - **Research (40%)**: Assesses the scope, quality, and influence of a university's scholarly output across disciplines.
   - **Reputation (25%)**: Reflects how the institution is regarded by the global academic and professional communities.
   - **Employment (25%)**: Gauges the career success and workplace impact of graduates in diverse industries.
   - **Internationalization (10%)**: Measures the institution's global reach and diversity in students, faculty, and collaborations.

### 3. DataLab页面
1. 添加标题："Barentsz DataLab"
2. 添加功能介绍：
   ```
   Barentsz DataLab is our advanced analytics platform that provides deep insights 
   into university performance metrics. We use cutting-edge data science techniques 
   to analyze academic excellence across multiple dimensions.
   ```

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
3. 检查排名表格是否正常显示

### 2. 发布网站
1. 点击 "Publish" 按钮
2. 确认发布设置
3. 网站正式上线

## 🔧 常见问题解决

### 1. HTML嵌入不显示
- 检查HTML代码语法
- 确保代码完整复制
- 查看浏览器控制台错误

### 2. 表格显示问题
- 调整嵌入框大小
- 检查CSS样式
- 测试移动端显示

### 3. 移动端显示问题
- 使用Wix的移动端编辑器
- 调整元素大小和位置
- 测试不同设备尺寸

## 📞 技术支持

### Wix支持
- 在线聊天：在Wix编辑器中点击 "Help"
- 视频教程：Wix学习中心
- 社区论坛：Wix社区

## 💰 成本说明

### Wix方案成本
- **Wix网站**: $14-23/月（包含域名和SSL）
- **后端**: 免费（静态数据）
- **总计**: $14-23/月

### 优势
- ✅ 无需服务器管理
- ✅ 自动SSL证书
- ✅ 内置CDN
- ✅ 拖拽式编辑器
- ✅ 24/7技术支持

---

**完成这些步骤后，您的大学排名网站就正式上线了！**

**注意：这个方案使用静态数据，如果需要更新数据，需要手动修改HTML代码中的UNIVERSITY_DATA对象。** 