# 全球大学数据收集器

## 项目概述
这是一个用于收集全球大学信息的Python项目，包括：
- 大学英文名称
- 官方邮箱地址
- 管理层邮箱信息
- 地理位置信息
- 官方网站

## 功能特性
- 🎯 多数据源支持（官方API、网页爬虫、人工验证）
- 🌍 全球范围覆盖（从西班牙开始试点）
- 📊 数据质量保证（验证和清洗）
- 🔄 自动化数据更新
- 📈 数据分析和报告
- 🔒 数据安全和隐私保护

## 技术栈
- **后端框架**: FastAPI
- **数据库**: PostgreSQL/SQLite
- **爬虫工具**: Scrapy + Selenium
- **数据处理**: Pandas + NumPy
- **异步处理**: asyncio + aiohttp

## 🚀 快速开始

### 方法一：一键运行（推荐）

#### Windows用户
```bash
# 双击运行批处理文件
run_demo.bat
```

#### Mac/Linux用户
```bash
# 给脚本执行权限
chmod +x run_demo.sh

# 运行脚本
./run_demo.sh
```

### 方法二：手动运行

#### 步骤1：环境设置
```bash
# 进入项目目录
cd university_data_collector

# 运行环境设置脚本
python setup.py
```

#### 步骤2：演示导出功能
```bash
# 使用示例数据演示导出功能
python demo_export.py
```

#### 步骤3：查看结果
```bash
# 查看导出的文件
ls data/exports/
```

### 方法三：完整功能

#### 收集真实数据
```bash
# 运行爬虫收集西班牙大学数据
python run_spain_collection.py
```

#### 导出数据
```bash
# 快速导出
python quick_export.py

# 或使用完整导出脚本
python scripts/export_spain_data.py --format both
```

## 📋 运行要求

### Python版本
- Python 3.8 或更高版本
- 检查版本：`python --version`

### 依赖包
- pandas - 数据处理
- openpyxl - Excel文件支持
- aiohttp - 异步HTTP请求
- beautifulsoup4 - HTML解析
- loguru - 日志记录
- email-validator - 邮箱验证

## 📊 输出示例

运行成功后，您将看到：

```
============================================================
📤 西班牙大学数据导出演示
============================================================
📁 使用示例数据文件: data/sample_spain_universities.json
✅ 成功加载 10 条记录
✅ CSV文件已导出: data/exports/demo_spain_universities_20240101_120000.csv
✅ Excel文件已导出: data/exports/demo_spain_universities_20240101_120000.xlsx

📊 数据统计:
   总大学数量: 10
   有官方邮箱: 10
   有校长邮箱: 10
   有行政邮箱: 10

🌍 地区分布:
   Madrid: 3
   Catalonia: 3
   Andalusia: 2
   Valencia: 1
   Navarre: 1
```

## 📁 项目结构
```
university_data_collector/
├── app/
│   ├── api/                 # API路由
│   ├── core/               # 核心配置
│   ├── models/             # 数据模型
│   ├── services/           # 业务逻辑
│   ├── scrapers/           # 爬虫模块
│   └── utils/              # 工具函数
├── data/                   # 数据存储
│   ├── sample_spain_universities.json  # 示例数据
│   └── exports/            # 导出文件
├── scripts/                # 脚本文件
├── setup.py               # 环境设置脚本
├── demo_export.py         # 演示脚本
├── quick_export.py        # 快速导出脚本
├── run_demo.bat           # Windows批处理脚本
├── run_demo.sh            # Mac/Linux Shell脚本
├── RUN_GUIDE.md           # 运行指南
├── EXPORT_GUIDE.md        # 导出指南
└── README.md              # 项目说明
```

## 🔧 故障排除

### 常见问题

#### 1. Python版本过低
```bash
# 检查版本
python --version

# 升级Python（根据操作系统）
# Windows: 从python.org下载
# Mac: brew install python
# Linux: sudo apt-get install python3.8
```

#### 2. 依赖包安装失败
```bash
# 升级pip
python -m pip install --upgrade pip

# 重新安装依赖
pip install --force-reinstall pandas openpyxl
```

#### 3. 权限问题
```bash
# Windows: 以管理员身份运行
# Mac/Linux: 使用sudo
sudo python setup.py
```

### 错误信息及解决方案

#### ImportError: No module named 'pandas'
```bash
pip install pandas
```

#### FileNotFoundError: data/sample_spain_universities.json
```bash
# 重新运行环境设置
python setup.py
```

## 📈 数据收集策略

### 西班牙大学试点方案
1. **官方数据源**
   - 西班牙教育部网站
   - 西班牙大学校长会议(CRUE)
   - 各自治区教育部门

2. **爬虫目标**
   - 大学官网联系页面
   - 学术目录网站
   - 教育排名网站

3. **数据验证**
   - 邮箱格式验证
   - 域名一致性检查
   - 人工抽样验证

## 🛠️ 高级功能

### API接口

#### 获取大学列表
```
GET /api/universities?country=spain&limit=50
```

#### 搜索大学
```
GET /api/universities/search?q=university_name
```

#### 获取大学详情
```
GET /api/universities/{university_id}
```

### 数据导出选项

#### 导出格式
- CSV格式：便于程序处理
- Excel格式：包含多个工作表，便于人工分析

#### 导出内容
- 大学基本信息
- 联系信息（邮箱、电话、地址）
- 统计信息
- 地区分布
- 城市分布

## 📞 获取帮助

### 文档
- [运行指南](RUN_GUIDE.md) - 详细的运行说明
- [导出指南](EXPORT_GUIDE.md) - 数据导出功能说明
- [使用指南](USAGE_GUIDE.md) - 项目使用说明

### 支持
如果遇到问题：
1. 检查Python版本是否 >= 3.8
2. 确认所有依赖包已安装
3. 查看错误信息并参考故障排除部分
4. 检查文件路径和权限

## 贡献指南
1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

## 许可证
MIT License 