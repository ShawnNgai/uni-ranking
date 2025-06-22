# Python运行指南

## 🚀 快速开始

### 步骤1：环境设置
```bash
# 进入项目目录
cd university_data_collector

# 运行环境设置脚本
python setup.py
```

### 步骤2：演示导出功能
```bash
# 使用示例数据演示导出功能
python demo_export.py
```

### 步骤3：查看结果
```bash
# 查看导出的文件
ls data/exports/
```

## 📋 详细运行步骤

### 1. 环境准备

#### 检查Python版本
```bash
python --version
# 确保版本 >= 3.8
```

#### 安装依赖包
```bash
# 方法1：使用setup.py（推荐）
python setup.py

# 方法2：手动安装
pip install pandas openpyxl aiohttp beautifulsoup4 loguru email-validator
```

### 2. 运行演示

#### 演示数据导出
```bash
python demo_export.py
```

这个脚本会：
- 加载示例数据（10所西班牙大学）
- 导出为CSV和Excel格式
- 显示统计信息
- 生成报告

#### 预期输出
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

📋 样本数据 (前3条):
   1. Complutense University of Madrid
      网站: https://www.ucm.es/
      官方邮箱: info@ucm.es
      校长邮箱: rector@ucm.es

   2. University of Barcelona
      网站: https://www.ub.edu/
      官方邮箱: info@ub.edu
      校长邮箱: rector@ub.edu

   3. Autonomous University of Madrid
      网站: https://www.uam.es/
      官方邮箱: informacion@uam.es
      校长邮箱: rector@uam.es

📄 导出文件:
   CSV: data/exports/demo_spain_universities_20240101_120000.csv
   Excel: data/exports/demo_spain_universities_20240101_120000.xlsx

💡 使用提示:
   - 可以使用Excel打开CSV文件
   - Excel文件包含多个工作表
   - 文件已保存在 data/exports 目录中
   - 可以运行 python quick_export.py 进行完整导出

✅ 演示完成!
```

### 3. 实际数据收集

#### 运行爬虫收集数据
```bash
python run_spain_collection.py
```

#### 导出真实数据
```bash
python quick_export.py
```

### 4. 高级功能

#### 使用完整导出脚本
```bash
# 导出为CSV格式
python scripts/export_spain_data.py --format csv

# 导出为Excel格式
python scripts/export_spain_data.py --format excel

# 导出为两种格式
python scripts/export_spain_data.py --format both

# 自定义输出目录
python scripts/export_spain_data.py --output-dir ./my_exports
```

## 🔧 故障排除

### 常见问题

#### 1. Python版本问题
```bash
# 检查版本
python --version

# 如果版本过低，请升级Python
# Windows: 从python.org下载最新版本
# Mac: brew install python
# Linux: sudo apt-get install python3.8
```

#### 2. 依赖包安装失败
```bash
# 升级pip
python -m pip install --upgrade pip

# 重新安装依赖
pip install --force-reinstall pandas openpyxl

# 或者使用conda
conda install pandas openpyxl
```

#### 3. 权限问题
```bash
# Windows: 以管理员身份运行命令提示符
# Mac/Linux: 使用sudo
sudo python setup.py
```

#### 4. 编码问题
```bash
# 确保使用UTF-8编码
export PYTHONIOENCODING=utf-8
python demo_export.py
```

### 错误信息及解决方案

#### ImportError: No module named 'pandas'
```bash
pip install pandas
```

#### ImportError: No module named 'openpyxl'
```bash
pip install openpyxl
```

#### FileNotFoundError: data/sample_spain_universities.json
```bash
# 检查文件是否存在
ls data/

# 如果不存在，重新运行setup.py
python setup.py
```

## 📊 查看结果

### 1. 查看导出文件
```bash
# 列出所有导出文件
ls -la data/exports/

# 查看CSV文件内容
head -5 data/exports/*.csv

# 查看Excel文件信息
file data/exports/*.xlsx
```

### 2. 在Excel中打开
- 双击Excel文件
- 或使用命令：`open data/exports/*.xlsx` (Mac)
- 或使用命令：`start data/exports/*.xlsx` (Windows)

### 3. 数据分析
```python
# 在Python中分析数据
import pandas as pd

# 读取CSV文件
df = pd.read_csv('data/exports/demo_spain_universities_20240101_120000.csv')

# 查看基本信息
print(df.info())
print(df.head())

# 统计信息
print(df.describe())
```

## 🎯 运行顺序建议

### 新手用户
1. `python setup.py` - 环境设置
2. `python demo_export.py` - 演示功能
3. 查看 `data/exports/` 目录中的文件

### 进阶用户
1. `python setup.py` - 环境设置
2. `python run_spain_collection.py` - 收集数据
3. `python quick_export.py` - 导出数据
4. 使用Excel分析数据

### 开发者
1. `python setup.py` - 环境设置
2. `python test_scraper.py` - 测试爬虫
3. `python scripts/collect_spain_universities.py` - 完整收集
4. `python scripts/export_spain_data.py --format both` - 完整导出

## 💡 使用技巧

### 1. 虚拟环境（推荐）
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 自动化运行
```bash
# 创建批处理脚本
echo "python setup.py && python demo_export.py" > run_demo.bat
```

### 3. 定期更新
```bash
# 创建定时任务
# Windows: 任务计划程序
# Mac/Linux: crontab
```

## 📞 获取帮助

如果遇到问题：
1. 检查Python版本是否 >= 3.8
2. 确认所有依赖包已安装
3. 查看错误信息并参考故障排除部分
4. 检查文件路径和权限

更多帮助请参考项目文档或提交Issue。 