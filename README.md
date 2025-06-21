# 大学排名网站 (Uni-Ranking)

这是一个完整的大学排名网站项目，提供全球大学排名数据展示、筛选和管理功能。

## 功能特性

- **主页** - 网站介绍和统计信息
- **排名页面** - 完整的大学排名列表，支持筛选和分页
- **方法论页面** - 详细介绍排名方法
- **评分系统页面** - 评分计算方法和权重说明
- **媒体页面** - 新闻发布和媒体报道
- **数据管理页面** - 上传和管理大学排名数据

## 数据导入功能

### 支持的文件格式
- **CSV文件** (.csv)
- **Excel文件** (.xlsx, .xls)

### 必需字段
- `university_name` - 大学名称
- `country` - 国家
- `region` - 地区
- `score` - 总分

### 可选字段
- `rank` - 排名
- `research_performance` - 研究表现
- `quality_of_education` - 教育质量
- `alumni_employment` - 校友就业
- `quality_of_faculty` - 师资质量
- `publications` - 出版物
- `influence` - 影响力
- `citations` - 引用
- `broad_impact` - 广泛影响
- `patents` - 专利
- `year` - 年份

### 数据导入步骤
1. 访问 `/admin` 页面
2. 下载Excel模板文件
3. 按照模板格式填写数据
4. 上传文件到系统
5. 查看导入结果

## 安装和运行

1. 安装依赖：
```bash
npm install
```

2. 启动服务器：
```bash
npm start
```

3. 访问网站：`http://localhost:3000`

## 技术栈

- **后端**: Node.js, Express.js, SQLite3
- **前端**: HTML5, CSS3, JavaScript
- **数据库**: SQLite

## 项目结构

```
├── server.js              # 主服务器文件
├── package.json           # 项目配置
├── public/               # 静态文件
│   ├── css/             # 样式文件
│   ├── js/              # JavaScript文件
│   └── *.html           # HTML页面
├── data/                # 数据文件目录
│   └── sample_data.csv  # 示例数据文件
└── database/             # 数据库文件
```

## API接口

- `GET /api/universities` - 获取大学排名
- `GET /api/countries` - 获取国家列表
- `GET /api/regions` - 获取地区列表
- `GET /api/years` - 获取年份列表
- `POST /api/import` - 导入数据文件
- `GET /api/template` - 下载数据模板
- `DELETE /api/universities` - 清空所有数据

## 数据库结构

项目使用 SQLite 数据库存储大学排名数据。`universities` 表包含以下字段：

| 字段名          | 数据类型    | 描述                     |
| --------------- | ----------- | ------------------------ |
| `id`            | `INTEGER`   | 主键, 自增              |
| `rank`          | `INTEGER`   | 排名                     |
| `university`    | `TEXT`      | 大学名称 (必需)          |
| `country`       | `TEXT`      | 所在国家                 |
| `research`      | `REAL`      | 研究分数                 |
| `reputation`    | `REAL`      | 声誉分数                 |
| `employment`    | `REAL`      | 就业分数                 |
| `international` | `REAL`      | 国际化分数               |
| `total_score`   | `REAL`      | 总分                     |
| `star_rating`   | `TEXT`      | 星级评价                 |
| `year`          | `INTEGER`   | 年份                     |

### 数据导入

- **上传文件**: 你可以通过 `/admin` 页面上传 `CSV` 或 `XLSX` 格式的数据文件。
- **文件格式**: 上传的文件应包含以下列标题 (大小写不敏感):
  - **必需**: `University`, `Country`, `Total_Score`
  - **可选**: `Rank`, `Research`, `Reputation`, `Employment`, `International`, `Star_Rating`, `year`
- **下载模板**: 你可以在 `/admin` 页面下载一个格式化的Excel模板，以确保数据格式正确。
- **清空数据**: 你可以在 `/admin` 页面清空数据库中的所有排名数据。 