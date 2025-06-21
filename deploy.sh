#!/bin/bash

# Barentsz Uni-Ranking 一键部署脚本
# 使用方法: ./deploy.sh your-domain.com

DOMAIN=$1
PROJECT_DIR="/var/www/barentsz-uni-ranking"
NGINX_CONF="/etc/nginx/sites-available/barentsz-uni-ranking"

echo "🚀 开始部署 Barentsz Uni-Ranking 到域名: $DOMAIN"

# 检查域名参数
if [ -z "$DOMAIN" ]; then
    echo "❌ 请提供域名参数"
    echo "使用方法: ./deploy.sh your-domain.com"
    exit 1
fi

# 更新系统
echo "📦 更新系统包..."
sudo apt update && sudo apt upgrade -y

# 安装Node.js
echo "📦 安装 Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装Nginx
echo "📦 安装 Nginx..."
sudo apt install nginx -y

# 安装PM2
echo "📦 安装 PM2..."
sudo npm install -g pm2

# 安装Certbot
echo "📦 安装 Certbot..."
sudo apt install certbot python3-certbot-nginx -y

# 创建项目目录
echo "📁 创建项目目录..."
sudo mkdir -p $PROJECT_DIR
sudo chown $USER:$USER $PROJECT_DIR

# 复制项目文件（假设当前目录是项目目录）
echo "📋 复制项目文件..."
cp -r . $PROJECT_DIR/

# 安装依赖
echo "📦 安装项目依赖..."
cd $PROJECT_DIR
npm install --production

# 创建Nginx配置
echo "⚙️ 配置 Nginx..."
sudo tee $NGINX_CONF > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

# 启用Nginx配置
sudo ln -sf $NGINX_CONF /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx

# 配置防火墙
echo "🔥 配置防火墙..."
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

# 启动应用
echo "🚀 启动应用..."
pm2 start server.js --name "barentsz-uni-ranking"
pm2 startup
pm2 save

# 获取SSL证书
echo "🔒 获取SSL证书..."
sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

# 设置自动续期
echo "⏰ 设置SSL证书自动续期..."
(crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -

echo "✅ 部署完成！"
echo "🌐 网站地址: https://$DOMAIN"
echo "📊 PM2状态: pm2 status"
echo "📝 查看日志: pm2 logs barentsz-uni-ranking"
echo "🔧 Nginx状态: sudo systemctl status nginx" 