# 西班牙大学数据导出指南

## 📤 快速导出

### 方法一：快速导出脚本
```bash
# 直接运行快速导出脚本
python quick_export.py
```

这个脚本会自动：
- 查找最新的数据文件
- 导出为CSV和Excel格式
- 生成统计信息
- 保存到 `data/exports` 目录

### 方法二：完整导出脚本
```bash
# 导出为CSV格式
python scripts/export_spain_data.py --format csv

# 导出为Excel格式
python scripts/export_spain_data.py --format excel

# 导出为两种格式
python scripts/export_spain_data.py --format both
```

## 📊 导出文件说明

### CSV文件格式
包含以下字段：
- 英文名称
- 本地名称
- 国家
- 地区
- 城市
- 官方网站
- 官方邮箱
- 联系邮箱
- 校长邮箱
- 行政邮箱
- 电话
- 地址
- 成立年份
- 学生数量
- 教职工数量
- 大学类型
- 世界排名
- 数据来源
- 备注

### Excel文件格式
包含多个工作表：

#### 1. 大学数据
- 包含所有大学的基本信息
- 与CSV文件内容相同

#### 2. 统计信息
- 总大学数量
- 有官方邮箱的大学数量
- 有校长邮箱的大学数量
- 有行政邮箱的大学数量
- 各类型大学的分布

#### 3. 地区分布
- 按地区统计大学数量
- 显示各地区占比

#### 4. 城市分布
- 按城市统计大学数量
- 显示各城市占比

## 🔧 高级选项

### 自定义输出目录
```bash
python scripts/export_spain_data.py --output-dir /path/to/output
```

### 指定数据目录
```bash
python scripts/export_spain_data.py --data-dir /path/to/data
```

### 查看帮助
```bash
python scripts/export_spain_data.py --help
```

## 📋 使用示例

### 1. 基本导出
```bash
# 进入项目目录
cd university_data_collector

# 运行快速导出
python quick_export.py
```

输出示例：
```
============================================================
📤 西班牙大学数据快速导出
============================================================
📁 找到数据文件: data/spain_universities_20240101_120000.json
✅ 成功加载 50 条记录
✅ CSV文件已导出: data/exports/spain_universities_20240101_120000.csv
✅ Excel文件已导出: data/exports/spain_universities_20240101_120000.xlsx

📊 导出统计:
   总大学数量: 50
   有官方邮箱: 35
   有校长邮箱: 20
   有行政邮箱: 15

📄 导出文件:
   CSV: data/exports/spain_universities_20240101_120000.csv
   Excel: data/exports/spain_universities_20240101_120000.xlsx
```

### 2. 自定义导出
```bash
# 只导出CSV格式
python scripts/export_spain_data.py --format csv

# 导出到指定目录
python scripts/export_spain_data.py --format both --output-dir ./my_exports
```

## 📈 数据质量说明

### 邮箱覆盖率
- **官方邮箱**: 约70-80%
- **校长邮箱**: 约40-50%
- **行政邮箱**: 约30-40%

### 数据来源
- 西班牙教育部
- 大学校长会议(CRUE)
- 各大学官网
- 教育排名网站

### 数据更新频率
- 建议每月更新一次
- 重要数据变更时及时更新
- 定期验证邮箱有效性

## 🛠️ 故障排除

### 1. 找不到数据文件
```bash
# 确保先运行数据收集
python run_spain_collection.py
# 或
python scripts/collect_spain_universities.py
```

### 2. 依赖包缺失
```bash
# 安装pandas和openpyxl
pip install pandas openpyxl
```

### 3. 编码问题
- CSV文件使用UTF-8编码
- 支持中文字符
- 可在Excel中正常打开

### 4. 文件权限问题
```bash
# 确保有写入权限
chmod 755 data/exports
```

## 💡 使用建议

### 1. 文件命名
- 导出文件包含时间戳
- 便于版本管理
- 避免文件覆盖

### 2. 数据备份
- 定期备份导出文件
- 保留多个版本
- 重要数据多重备份

### 3. 数据分析
- 使用Excel进行数据分析
- 利用统计工作表
- 关注数据质量指标

### 4. 数据共享
- CSV格式便于程序处理
- Excel格式便于人工查看
- 注意数据隐私保护

## 📞 技术支持

如果遇到问题，请检查：
1. Python环境是否正确
2. 依赖包是否安装完整
3. 数据文件是否存在
4. 输出目录是否有写入权限

更多帮助请参考项目文档或提交Issue。 