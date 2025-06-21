@echo off
echo 开始备份 Barentsz Uni-Ranking 项目...

set backup_dir=backup_2025_01_27_%time:~0,2%%time:~3,2%%time:~6,2%
set backup_dir=%backup_dir: =0%

echo 创建备份目录: %backup_dir%
mkdir %backup_dir%

echo 备份核心文件...
copy package.json %backup_dir%\
copy package-lock.json %backup_dir%\
copy README.md %backup_dir%\
copy server.js %backup_dir%\
copy test_api.js %backup_dir%\

echo 备份前端文件...
xcopy public %backup_dir%\public /E /I /Y

echo 备份数据库文件...
xcopy database %backup_dir%\database /E /I /Y

echo 备份数据文件...
xcopy data %backup_dir%\data /E /I /Y

echo 备份上传文件...
xcopy uploads %backup_dir%\uploads /E /I /Y

echo 备份完成！
echo 备份目录: %backup_dir%
pause 