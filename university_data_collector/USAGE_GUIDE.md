# 全球大学数据收集器 - 使用指南

## 🚀 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境

```bash
# 复制环境配置文件
cp env.example .env

# 编辑配置文件（可选）
# 主要配置项：
# - DATABASE_URL: 数据库连接
# - REQUEST_DELAY: 请求间隔
# - TIMEOUT: 超时时间
```

### 3. 快速测试

```bash
# 运行快速测试
python run_spain_collection.py
```

### 4. 完整数据收集

```bash
# 运行完整的数据收集脚本
python scripts/collect_spain_universities.py
```

## 📊 数据收集策略

### 西班牙大学试点方案

#### 1. 官方数据源
- **西班牙教育部**: https://www.educacionyfp.gob.es/
- **CRUE (大学校长会议)**: https://www.crue.org/
- **各自治区教育部门**

#### 2. 大学目录网站
- **Study in Spain**: https://www.studyinspain.info/
- **Universia**: https://www.universia.net/
- **Erasmus+ 合作大学列表**

#### 3. 排名网站
- **QS World Rankings**: https://www.topuniversities.com/
- **Times Higher Education**: https://www.timeshighereducation.com/
- **Shanghai Ranking**: http://www.shanghairanking.com/

#### 4. 大学官网爬取
- 联系页面
- 关于我们页面
- 组织结构页面

## 🔧 技术实现

### 数据收集流程

1. **多源数据收集**
   - 官方API接口
   - 网页爬虫
   - 公开数据集

2. **数据清洗和验证**
   - 邮箱格式验证
   - 域名一致性检查
   - 去重处理

3. **数据存储**
   - JSON格式导出
   - 数据库存储
   - 备份管理

### 邮箱提取策略

1. **联系页面优先**
   - `/contacto`
   - `/contact`
   - `/about/contact`

2. **关键词识别**
   - 校长邮箱: rector, president, rectorado
   - 行政邮箱: admin, secretaria, secretary
   - 官方邮箱: info, contacto, contact

3. **域名验证**
   - 教育域名: .edu, .ac, .university
   - 国家域名: .es, .edu.es
   - 排除无效域名

## 📈 扩展计划

### 其他国家实现

1. **法国大学**
   - 法国教育部
   - Campus France
   - 大学校长会议

2. **德国大学**
   - DAAD (德国学术交流中心)
   - 德国大学校长会议
   - 各州教育部门

3. **意大利大学**
   - 意大利教育部
   - CRUI (意大利大学校长会议)
   - 地区教育部门

4. **英国大学**
   - UCAS
   - 英国大学联盟
   - 各大学官网

### 数据质量提升

1. **自动化验证**
   - 邮箱有效性检查
   - 网站可访问性验证
   - 数据一致性检查

2. **人工审核**
   - 抽样验证
   - 数据准确性检查
   - 反馈机制

3. **持续更新**
   - 定期数据刷新
   - 变更检测
   - 版本管理

## 🛠️ 高级功能

### 1. API服务

```python
# 启动API服务
uvicorn app.main:app --reload

# API端点
GET /api/universities?country=spain&limit=50
GET /api/universities/search?q=university_name
GET /api/universities/{university_id}
```

### 2. 数据导出

```python
# 导出为Excel
python scripts/export_to_excel.py

# 导出为CSV
python scripts/export_to_csv.py

# 导出为JSON
python scripts/export_to_json.py
```

### 3. 数据分析

```python
# 生成统计报告
python scripts/generate_report.py

# 数据可视化
python scripts/visualize_data.py
```

## 🔒 注意事项

### 1. 法律合规
- 遵守robots.txt
- 合理设置请求间隔
- 尊重网站使用条款

### 2. 数据隐私
- 仅收集公开信息
- 不存储个人敏感数据
- 遵守GDPR等隐私法规

### 3. 技术限制
- 避免过度请求
- 处理反爬虫机制
- 错误重试机制

## 📞 技术支持

### 常见问题

1. **依赖安装失败**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --force-reinstall
   ```

2. **网络连接问题**
   - 检查网络连接
   - 配置代理设置
   - 调整超时时间

3. **数据质量问题**
   - 检查邮箱格式
   - 验证网站可访问性
   - 人工抽样检查

### 联系支持

- 项目仓库: [GitHub链接]
- 问题反馈: [Issues页面]
- 技术文档: [Wiki页面]

## 📝 更新日志

### v1.0.0 (2024-01-XX)
- ✅ 西班牙大学数据收集
- ✅ 基础爬虫框架
- ✅ 数据清洗和验证
- ✅ JSON格式导出
- ✅ 统计报告生成

### 计划功能
- 🔄 多国家支持
- 🔄 API服务
- 🔄 数据库存储
- �� 数据可视化
- 🔄 自动化更新 