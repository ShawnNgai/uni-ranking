# Barentsz Uni-Ranking 项目备份脚本
# 创建时间: 2025-01-27

# 设置备份目录名称
$backupDir = "backup_2025_01_27_$(Get-Date -Format 'HHmmss')"

# 创建备份目录
Write-Host "创建备份目录: $backupDir" -ForegroundColor Green
New-Item -ItemType Directory -Name $backupDir -Force | Out-Null

# 复制核心文件
Write-Host "备份核心文件..." -ForegroundColor Yellow
Copy-Item "package.json" -Destination "$backupDir/" -Force
Copy-Item "package-lock.json" -Destination "$backupDir/" -Force
Copy-Item "README.md" -Destination "$backupDir/" -Force
Copy-Item "server.js" -Destination "$backupDir/" -Force
Copy-Item "test_api.js" -Destination "$backupDir/" -Force

# 复制public目录（前端文件）
Write-Host "备份前端文件..." -ForegroundColor Yellow
Copy-Item "public" -Destination "$backupDir/" -Recurse -Force

# 复制database目录（数据库文件）
Write-Host "备份数据库文件..." -ForegroundColor Yellow
Copy-Item "database" -Destination "$backupDir/" -Recurse -Force

# 复制data目录（数据文件）
Write-Host "备份数据文件..." -ForegroundColor Yellow
Copy-Item "data" -Destination "$backupDir/" -Recurse -Force

# 复制uploads目录（上传文件）
Write-Host "备份上传文件..." -ForegroundColor Yellow
Copy-Item "uploads" -Destination "$backupDir/" -Recurse -Force

# 创建备份信息文件
$backupInfo = @"
Barentsz Uni-Ranking 项目备份信息
====================================
备份时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
备份目录: $backupDir
项目版本: 1.0.0

包含的文件和目录:
- package.json (项目配置)
- package-lock.json (依赖锁定)
- README.md (项目说明)
- server.js (服务器代码)
- test_api.js (API测试)
- public/ (前端文件)
  - index.html (主页)
  - rankings.html (排名页面)
  - methodology.html (方法论页面)
  - rating-system.html (评分系统页面)
  - media.html (新闻页面)
  - admin.html (管理页面)
  - css/style.css (样式文件)
  - js/ (JavaScript文件)
  - images/ (图片和Logo文件)
- database/ (数据库文件)
- data/ (数据文件)
- uploads/ (上传文件)

备份完成！
"@

$backupInfo | Out-File -FilePath "$backupDir/backup_info.txt" -Encoding UTF8

Write-Host "备份完成！" -ForegroundColor Green
Write-Host "备份目录: $backupDir" -ForegroundColor Cyan
Write-Host "备份信息已保存到: $backupDir/backup_info.txt" -ForegroundColor Cyan

# 显示备份目录内容
Write-Host "`n备份目录内容:" -ForegroundColor Yellow
Get-ChildItem -Path $backupDir -Recurse | Select-Object FullName, Length | Format-Table -AutoSize 