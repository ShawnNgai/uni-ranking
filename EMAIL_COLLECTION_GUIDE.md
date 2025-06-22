# 大学官方邮箱收集系统使用指南

## 📋 项目概述

本系统用于收集排名501-1000的大学官方邮箱，采用多种策略确保获取准确的联系信息。

## 🎯 功能特点

- **多策略收集**: 结合Google搜索、官网解析、Selenium自动化
- **智能筛选**: 自动过滤非官方邮箱，优先选择admissions、info等官方邮箱
- **批量处理**: 支持分批处理，避免内存溢出
- **进度保存**: 自动保存进度，支持断点续传
- **多格式导出**: 支持JSON和CSV格式导出

## 📊 数据概览

- **目标大学**: 排名501-1000的大学 (500所)
- **主要国家**: 中国(65所)、美国(62所)、英国(33所)等
- **收集字段**: 排名、大学名称、国家、官方邮箱、联系邮箱、网站

## 🚀 快速开始

### 方法1: 使用批处理文件 (推荐)

1. 双击运行 `run_email_collector.bat`
2. 系统会自动安装依赖并启动收集器
3. 等待收集完成

### 方法2: 手动运行

```bash
# 安装依赖
pip install -r requirements_email_collector.txt

# 运行简化版收集器 (推荐新手)
python simple_email_collector.py

# 运行完整版收集器 (需要Chrome浏览器)
python university_email_collector.py
```

## 📁 输出文件

### 测试阶段
- `universities_emails_test.json` - 测试结果(JSON格式)
- `universities_emails_test.csv` - 测试结果(CSV格式)

### 完整结果
- `universities_emails_final.json` - 完整结果(JSON格式)
- `universities_emails_final.csv` - 完整结果(CSV格式)

### 进度文件
- `progress_simple_*.json` - 进度保存文件
- `email_collection_simple.log` - 运行日志

## 🔧 收集策略

### 策略1: 官网搜索
1. 通过Google搜索大学官网
2. 解析官网页面提取邮箱
3. 访问联系页面获取更多邮箱

### 策略2: Google搜索
1. 搜索"大学名 + official email"
2. 搜索"大学名 + contact email"
3. 搜索"大学名 + admissions email"

### 策略3: 智能筛选
- 过滤example.com、test.com等测试邮箱
- 过滤noreply、webmaster等非官方邮箱
- 优先选择admissions@、info@、contact@等官方邮箱

## 📈 预期结果

- **成功率**: 预计60-80%的大学能获取到官方邮箱
- **处理时间**: 约2-4小时(取决于网络速度)
- **数据质量**: 经过多重验证的官方邮箱

## ⚠️ 注意事项

1. **网络要求**: 需要稳定的网络连接
2. **时间限制**: 避免在高峰时段运行
3. **浏览器要求**: 完整版需要Chrome浏览器
4. **存储空间**: 确保有足够磁盘空间

## 🛠️ 故障排除

### 常见问题

1. **依赖安装失败**
   ```bash
   pip install --upgrade pip
   pip install -r requirements_email_collector.txt
   ```

2. **Chrome浏览器问题**
   - 使用简化版收集器
   - 或手动安装Chrome浏览器

3. **网络连接问题**
   - 检查网络连接
   - 尝试使用VPN
   - 增加请求间隔时间

4. **内存不足**
   - 减少批处理大小
   - 关闭其他程序

## 📞 技术支持

如遇到问题，请查看：
1. 运行日志文件
2. 检查网络连接
3. 确认Python版本(建议3.7+)

## 📋 数据格式示例

```json
{
  "rank": 501,
  "university": "Liverpool John Moores University",
  "country": "United Kingdom",
  "research": 68.5,
  "reputation": 65.2,
  "employment": 70.1,
  "international": 72.3,
  "total_score": 69.5,
  "star_rating": "★★★",
  "year": 2025,
  "website": "https://www.ljmu.ac.uk",
  "official_email": "admissions@ljmu.ac.uk",
  "contact_email": "info@ljmu.ac.uk",
  "all_emails_found": 3
}
```

## 🎉 完成后的使用

收集完成后，您可以：
1. 使用CSV文件进行数据分析
2. 导入到Excel进行进一步处理
3. 用于邮件营销或学术研究
4. 结合其他数据进行综合分析 