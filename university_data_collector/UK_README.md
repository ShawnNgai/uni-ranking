# 🇬🇧 英国大学邮箱收集器

## 项目概述
专门收集英国所有正规大学（公立和私立）的邮箱信息，并输出为CSV格式。

## 功能特性
- 🎯 收集英国所有正规大学邮箱
- 📧 提取多种类型邮箱（招生、国际、联系、信息等）
- 📊 输出CSV格式数据
- 🔍 邮箱格式验证
- 🚀 一键运行脚本

## 快速开始

### 方法一：一键运行（推荐）

#### Windows用户
```bash
# 双击运行批处理文件
run_uk.bat
```

#### Mac/Linux用户
```bash
# 给脚本执行权限
chmod +x run_uk.sh

# 运行脚本
./run_uk.sh
```

### 方法二：手动运行

#### 步骤1：安装依赖
```bash
pip install aiohttp loguru email-validator
```

#### 步骤2：运行演示
```bash
# 使用示例数据演示
python run_uk_demo.py
```

#### 步骤3：收集真实数据
```bash
# 收集真实大学邮箱
python run_uk_collection.py
```

## 输出格式

### CSV文件结构
| 字段名 | 说明 |
|--------|------|
| university_name | 大学英文名称 |
| website | 官方网站 |
| general_email | 通用邮箱 |
| admissions_email | 招生邮箱 |
| international_email | 国际学生邮箱 |
| contact_email | 联系邮箱 |
| info_email | 信息邮箱 |
| all_emails | 所有邮箱（分号分隔） |

### 示例输出
```csv
university_name,website,general_email,admissions_email,international_email,contact_email,info_email,all_emails
University of Oxford,https://www.ox.ac.uk/,admissions@ox.ac.uk,admissions@ox.ac.uk,international.office@ox.ac.uk,contact@ox.ac.uk,info@ox.ac.uk,"admissions@ox.ac.uk; international.office@ox.ac.uk; contact@ox.ac.uk; info@ox.ac.uk"
University of Cambridge,https://www.cam.ac.uk/,admissions@cam.ac.uk,admissions@cam.ac.uk,international@cam.ac.uk,contact@cam.ac.uk,info@cam.ac.uk,"admissions@cam.ac.uk; international@cam.ac.uk; contact@cam.ac.uk; info@cam.ac.uk"
```

## 大学列表

基于[Wikipedia英国大学列表](https://en.wikipedia.org/wiki/List_of_universities_in_the_United_Kingdom)，包含：

### 主要大学
- University of Oxford
- University of Cambridge
- Imperial College London
- University College London
- London School of Economics and Political Science
- University of Edinburgh
- King's College London
- University of Manchester
- University of Bristol
- University of Warwick

### 完整列表
共包含100+所英国正规大学，包括：
- 公立大学
- 私立大学
- 伦敦大学联盟成员
- 苏格兰、威尔士、北爱尔兰大学

## 技术实现

### 数据收集策略
1. **网站爬取**: 访问大学官方网站
2. **联系页面**: 优先查找联系页面
3. **邮箱提取**: 使用正则表达式提取邮箱
4. **格式验证**: 验证邮箱格式有效性
5. **分类整理**: 按类型分类邮箱

### 爬取目标页面
- `/contact` - 联系页面
- `/contact-us` - 联系我们
- `/about/contact` - 关于我们/联系
- `/admissions` - 招生页面
- `/international` - 国际学生页面

### 邮箱类型识别
- **admissions**: 包含"admission"关键词
- **international**: 包含"international"关键词
- **contact**: 包含"contact"关键词
- **info**: 包含"info"关键词
- **general**: 其他通用邮箱

## 运行要求

### Python版本
- Python 3.8 或更高版本

### 依赖包
- aiohttp - 异步HTTP请求
- loguru - 日志记录
- email-validator - 邮箱验证

## 故障排除

### 常见问题

#### 1. 网络连接问题
```bash
# 检查网络连接
ping www.ox.ac.uk
```

#### 2. 依赖包安装失败
```bash
# 升级pip
python -m pip install --upgrade pip

# 重新安装依赖
pip install --force-reinstall aiohttp loguru email-validator
```

#### 3. 权限问题
```bash
# Windows: 以管理员身份运行
# Mac/Linux: 使用sudo
sudo python3 run_uk_collection.py
```

### 错误信息及解决方案

#### ImportError: No module named 'aiohttp'
```bash
pip install aiohttp
```

#### ConnectionError: 网络连接失败
- 检查网络连接
- 尝试使用VPN
- 稍后重试

## 数据质量

### 验证机制
1. **格式验证**: 使用email-validator验证邮箱格式
2. **域名检查**: 验证邮箱域名与大学网站域名一致性
3. **过滤机制**: 过滤掉明显的无效邮箱（noreply、test等）

### 数据统计
- 总大学数量: 100+
- 预期邮箱收集率: 70-90%
- 数据更新频率: 建议每月更新

## 使用建议

### 最佳实践
1. **定期更新**: 建议每月运行一次收集真实数据
2. **数据备份**: 保存历史数据文件
3. **质量检查**: 人工抽查验证邮箱有效性
4. **合规使用**: 遵守相关法律法规和网站使用条款

### 数据用途
- 学术研究
- 教育机构联系
- 国际合作
- 招生宣传

## 许可证
MIT License

## 贡献
欢迎提交Issue和Pull Request来改进项目。 