const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const multer = require('multer');
const XLSX = require('xlsx');
const fs = require('fs');
const fetch = require('node-fetch');
const csv = require('csv-parser');

const app = express();
const port = 3001;
const dbPath = 'database/rankings.db';
const dbDir = path.dirname(dbPath);

// Ensure the database directory exists
if (!fs.existsSync(dbDir)) {
    fs.mkdirSync(dbDir, { recursive: true });
}

// Connect to SQLite database
const db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error('Could not connect to database', err.message);
        return;
    }
    console.log('Connected to SQLite database');
    initDatabase();
});

// Serve static files from the 'public' directory
app.use(express.static('public'));
app.use(express.json()); // for parsing application/json
app.use(cors({
    origin: [
        'https://*.wixsite.com',
        'https://*.wix.com',
        'http://localhost:3000',
        'http://localhost:3001'
    ],
    credentials: true
}));

// Admin access control middleware
app.use('/admin', (req, res, next) => {
    // 检查是否有正确的访问参数
    const adminKey = req.query.key || req.headers['x-admin-key'];
    const correctKey = 'barentsz2024'; // 您可以修改这个密钥
    
    if (adminKey === correctKey) {
        next(); // 允许访问
    } else {
        res.status(404).send('Page not found'); // 返回404，不暴露admin页面存在
    }
});

// Configure multer for file uploads
const upload = multer({ dest: 'uploads/' });

// Database initialization
function initDatabase() {
  // Create universities table
  db.run(`CREATE TABLE IF NOT EXISTS universities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rank INTEGER,
    university TEXT NOT NULL,
    country TEXT,
    research REAL DEFAULT 0,
    reputation REAL DEFAULT 0,
    employment REAL DEFAULT 0,
    international REAL DEFAULT 0,
    total_score REAL DEFAULT 0,
    star_rating TEXT,
    year INTEGER DEFAULT 2024
  )`, (err) => {
    if (err) {
      console.error('创建表失败:', err);
    } else {
      console.log('数据库表创建成功');
      
      // 强制导入2024年数据
      console.log('开始强制导入2024年数据...');
      import2024Data();
    }
  });
}

// 从Google Sheet导入数据
async function importDataFromGoogleSheet() {
    try {
        console.log('开始从Google Sheet下载数据...');
        
        // 使用最新的Google Sheet链接
        const googleSheetUrl = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT4lglkLyg-yV8giRzuQaGj1SESG6DDS0zwbHhooi8m77SOJ2OlMwO7dGlkv4pHs9R195Uw7hHzUUJb/pub?output=csv';
        
        const response = await fetch(googleSheetUrl);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        console.log('成功下载CSV数据，开始解析...');
        
        const data = [];
        response.body.pipe(csv())
            .on('data', (row) => {
                const mappedRow = {
                    rank: row.Rank,
                    university: row.University,
                    country: row['Country&Regions'], // 处理特殊列名
                    research: row.Research,
                    reputation: row.Reputation,
                    employment: row.Employment,
                    international: row.International,
                    total_score: row.Total_Score,
                    star_rating: row.Star_Rating,
                    year: row.year // 使用表格中的年份
                };
                data.push(mappedRow);
            })
            .on('end', () => {
                console.log(`解析完成，共 ${data.length} 条数据`);
                insertImportedData(data);
            })
            .on('error', (error) => {
                console.error('解析CSV数据失败:', error);
            });

    } catch (error) {
        console.error('从 Google Sheet 导入数据失败:', error);
    }
}

// 导入2024年数据
async function import2024Data() {
    try {
        console.log('开始导入2024年数据...');
        
        // 从Google Sheet导入2024年数据
        const googleSheetUrl = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT4lglkLyg-yV8giRzuQaGj1SESG6DDS0zwbHhooi8m77SOJ2OlMwO7dGlkv4pHs9R195Uw7hHzUUJb/pub?output=csv';
        
        const response = await fetch(googleSheetUrl);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        console.log('成功下载2024年CSV数据，开始解析...');
        
        const data = [];
        response.body.pipe(csv())
            .on('data', (row) => {
                const mappedRow = {
                    rank: row.Rank,
                    university: row.University,
                    country: row['Country&Regions'],
                    research: row.Research,
                    reputation: row.Reputation,
                    employment: row.Employment,
                    international: row.International,
                    total_score: row.Total_Score,
                    star_rating: row.Star_Rating,
                    year: 2024 // 强制设置为2024年
                };
                data.push(mappedRow);
            })
            .on('end', () => {
                console.log(`2024年数据解析完成，共 ${data.length} 条数据`);
                insertImportedData(data);
            })
            .on('error', (error) => {
                console.error('解析2024年CSV数据失败:', error);
            });

    } catch (error) {
        console.error('导入2024年数据失败:', error);
    }
}

// 将解析后的数据插入数据库
function insertImportedData(data) {
    console.log('开始插入数据到数据库...');
    
    const stmt = db.prepare(`INSERT INTO universities (
        rank, university, country, research, reputation, employment,
        international, total_score, star_rating, year
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`);

    let successCount = 0;
    let errorCount = 0;

    db.serialize(() => {
        db.run('BEGIN TRANSACTION');
        
        data.forEach((row, index) => {
            const values = [
                parseInt(row.rank) || null,
                row.university,
                row.country,
                parseFloat(row.research) || 0,
                parseFloat(row.reputation) || 0,
                parseFloat(row.employment) || 0,
                parseFloat(row.international) || 0,
                parseFloat(row.total_score) || 0,
                row.star_rating || '',
                parseInt(row.year) || new Date().getFullYear()
            ];
            
            stmt.run(values, (err) => {
              if (err) {
                console.error(`插入第 ${index + 1} 行数据失败:`, err, '数据:', row);
                errorCount++;
              } else {
                successCount++;
              }
            });
        });
        
        db.run('COMMIT', (err) => {
            if (err) {
                console.error('提交事务失败:', err);
            } else {
                console.log(`数据插入完成: 成功 ${successCount} 条，失败 ${errorCount} 条`);
            }
        });
    });

    stmt.finalize();
}

// API路由

// 获取大学排名列表（支持筛选和分页）
app.get('/api/universities', (req, res) => {
  const {
    page = 1,
    limit = 20,
    country,
    search,
    sortBy = 'rank',
    sortOrder = 'ASC',
    year
  } = req.query;

  let query = 'SELECT * FROM universities WHERE 1=1';
  let params = [];

  if (country) {
    query += ' AND country LIKE ?';
    params.push(`%${country}%`);
  }
  
  if (year) {
    query += ' AND year = ?';
    params.push(year);
  }

  if (search) {
    query += ' AND (university LIKE ? OR country LIKE ?)';
    params.push(`%${search}%`, `%${search}%`);
  }

  // 获取总数
  db.get(`SELECT COUNT(*) as total FROM (${query})`, params, (err, countRow) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }

    const total = countRow.total;
    const offset = (page - 1) * limit;

    // 添加排序和分页
    query += ` ORDER BY ${sortBy} ${sortOrder} LIMIT ? OFFSET ?`;
    params.push(parseInt(limit), offset);

    db.all(query, params, (err, rows) => {
      if (err) {
        res.status(500).json({ error: err.message });
        return;
      }

      res.json({
        universities: rows,
        pagination: {
          page: parseInt(page),
          limit: parseInt(limit),
          total,
          totalPages: Math.ceil(total / limit)
        }
      });
    });
  });
});

// 获取单个大学详情
app.get('/api/universities/:id', (req, res) => {
  const { id } = req.params;
  
  db.get('SELECT * FROM universities WHERE id = ?', [id], (err, row) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    
    if (!row) {
      res.status(404).json({ error: '大学未找到' });
      return;
    }
    
    res.json(row);
  });
});

// 获取国家列表
app.get('/api/countries', (req, res) => {
  db.all('SELECT DISTINCT country FROM universities ORDER BY country', (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    res.json(rows.map(row => row.country));
  });
});

// 获取地区列表
app.get('/api/regions', (req, res) => {
  db.all('SELECT DISTINCT university FROM universities ORDER BY university', (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    res.json(rows.map(row => row.university));
  });
});

// 获取年份列表
app.get('/api/years', (req, res) => {
  db.all('SELECT DISTINCT year FROM universities ORDER BY year DESC', (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    res.json(rows.map(row => row.year));
  });
});

// 数据导入功能
app.post('/api/import', upload.single('file'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: '请选择文件' });
  }

  const filePath = req.file.path;
  const fileExt = path.extname(req.file.originalname).toLowerCase();

  try {
    let data = [];

    if (fileExt === '.csv') {
      // 处理CSV文件
      const csv = require('csv-parser');
      const results = [];
      
      fs.createReadStream(filePath)
        .pipe(csv())
        .on('data', (row) => results.push(row))
        .on('end', () => {
          data = results;
          processData(data, res);
        });
    } else if (fileExt === '.xlsx' || fileExt === '.xls') {
      // 处理Excel文件
      const workbook = XLSX.readFile(filePath);
      const sheetName = workbook.SheetNames[0];
      const worksheet = workbook.Sheets[sheetName];
      data = XLSX.utils.sheet_to_json(worksheet);
      processData(data, res);
    } else {
      res.status(400).json({ error: '不支持的文件格式' });
    }
  } catch (error) {
    res.status(500).json({ error: '文件处理失败: ' + error.message });
  }
});

// 处理导入的数据
function processData(data, res) {
  if (data.length === 0) {
    return res.status(400).json({ error: '文件中没有数据' });
  }

  // 验证数据格式
  const requiredFields = ['university', 'country', 'total_score'];
  const firstRow = data[0];
  
  for (let field of requiredFields) {
    if (!(field in firstRow)) {
      return res.status(400).json({ 
        error: `缺少必需字段: ${field}`,
        requiredFields: requiredFields,
        sampleData: firstRow
      });
    }
  }

  // 开始导入数据
  const stmt = db.prepare(`INSERT INTO universities (
    rank, university, country, research, reputation, employment,
    international, total_score, star_rating, year
  ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`);

  let successCount = 0;
  let errorCount = 0;

  data.forEach((row, index) => {
    try {
      // Map user-provided headers to our snake_case schema
      const mappedRow = {
        rank: row.Rank || row.rank || index + 1,
        university: row.University || row.university,
        country: row.Country || row.country,
        research: row.Research || row.research,
        reputation: row.Reputation || row.reputation,
        employment: row.Employment || row.employment,
        international: row.International || row.international,
        total_score: row.Total_Score || row.total_score,
        star_rating: row.Star_Rating || row.star_rating,
        year: row.year
      };

      const values = [
        mappedRow.rank,
        mappedRow.university,
        mappedRow.country,
        parseFloat(mappedRow.research) || 0,
        parseFloat(mappedRow.reputation) || 0,
        parseFloat(mappedRow.employment) || 0,
        parseFloat(mappedRow.international) || 0,
        parseFloat(mappedRow.total_score) || 0,
        mappedRow.star_rating || '',
        parseInt(mappedRow.year) || new Date().getFullYear()
      ];

      stmt.run(values, function(err) {
        if (err) {
          errorCount++;
          console.error(`导入第${index + 1}行数据失败:`, err);
        } else {
          successCount++;
        }
      });
    } catch (error) {
      errorCount++;
      console.error(`处理第${index + 1}行数据失败:`, error);
    }
  });

  stmt.finalize((err) => {
    if (err) {
      res.status(500).json({ error: '数据导入失败: ' + err.message });
    } else {
      res.json({ 
        message: '数据导入完成',
        successCount: successCount,
        errorCount: errorCount,
        totalCount: data.length
      });
    }
  });
}

// 获取数据导入模板
app.get('/api/template', (req, res) => {
  const template = [
    {
      Rank: 1,
      University: "Example University",
      Country: "Example Country",
      Research: 90.1,
      Reputation: 90.2,
      Employment: 90.3,
      International: 90.4,
      Total_Score: 95.5,
      Star_Rating: "5 Stars",
      year: 2025
    }
  ];

  const worksheet = XLSX.utils.json_to_sheet(template);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "Template");
  
  const buffer = XLSX.write(workbook, { type: 'buffer', bookType: 'xlsx' });
  
  res.setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
  res.setHeader('Content-Disposition', 'attachment; filename=university_template.xlsx');
  res.send(buffer);
});

// 清空数据库
app.delete('/api/universities', (req, res) => {
  db.run('DELETE FROM universities', (err) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    res.json({ message: '所有数据已清空' });
  });
});

// 页面路由
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/rankings', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'rankings.html'));
});

app.get('/methodology', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'methodology.html'));
});

app.get('/rating-system', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'rating-system.html'));
});

app.get('/media', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'media.html'));
});

app.get('/admin', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'admin.html'));
});

// 导入2024年数据的API端点
app.post('/api/import-2024', async (req, res) => {
    try {
        console.log('开始导入2024年数据...');
        
        // 首先清空2024年的数据
        db.run('DELETE FROM universities WHERE year = 2024', (err) => {
            if (err) {
                console.error('清空2024年数据失败:', err);
                return res.status(500).json({ error: '清空2024年数据失败' });
            }
            
            console.log('已清空2024年数据，开始导入新数据...');
            
            // 从Google Sheet导入2024年数据
            const googleSheetUrl = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT4lglkLyg-yV8giRzuQaGj1SESG6DDS0zwbHhooi8m77SOJ2OlMwO7dGlkv4pHs9R195Uw7hHzUUJb/pub?output=csv';
            
            fetch(googleSheetUrl)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    
                    const data = [];
                    response.body.pipe(csv())
                        .on('data', (row) => {
                            const mappedRow = {
                                rank: row.Rank,
                                university: row.University,
                                country: row['Country&Regions'],
                                research: row.Research,
                                reputation: row.Reputation,
                                employment: row.Employment,
                                international: row.International,
                                total_score: row.Total_Score,
                                star_rating: row.Star_Rating,
                                year: 2024 // 强制设置为2024年
                            };
                            data.push(mappedRow);
                        })
                        .on('end', () => {
                            console.log(`2024年数据解析完成，共 ${data.length} 条数据`);
                            insertImportedData(data);
                            res.json({ 
                                success: true, 
                                message: `成功导入 ${data.length} 条2024年数据`,
                                count: data.length 
                            });
                        })
                        .on('error', (error) => {
                            console.error('解析2024年CSV数据失败:', error);
                            res.status(500).json({ error: '解析2024年数据失败' });
                        });
                })
                .catch(error => {
                    console.error('下载2024年数据失败:', error);
                    res.status(500).json({ error: '下载2024年数据失败' });
                });
                
        });
        
    } catch (error) {
        console.error('导入2024年数据失败:', error);
        res.status(500).json({ error: '导入2024年数据失败' });
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
}); 