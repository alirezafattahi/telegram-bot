# 🐳 Docker Deployment Guide - راهنمای استقرار Docker

راهنمای کامل برای اجرای ربات تلگرام با Docker

## 📋 پیش‌نیازها

### نصب Docker و Docker Compose
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker compose

# CentOS/RHEL
sudo yum install docker docker compose

# یا با استفاده از Docker Desktop
# دانلود از: https://www.docker.com/products/docker-desktop
```

### بررسی نصب
```bash
docker --version
docker compose --version
```

## 🚀 اجرای سریع

### 1️⃣ **کلون کردن پروژه**
```bash
git clone <repository-url>
cd telegram-bot
```

### 2️⃣ **تنظیم متغیرهای محیطی**
```bash
# کپی کردن فایل نمونه
cp docker.env .env

# ویرایش فایل .env
nano .env
```

### 3️⃣ **اجرای ربات**
```bash
# اجرای خودکار
./docker-run.sh

# یا اجرای دستی
docker compose up -d
```

## ⚙️ تنظیمات

### فایل `.env`
```bash
# Bot Configuration
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
BOT_USERNAME=your_bot_username

# Database Configuration
DATABASE_PATH=/app/data/bot_database.db

# Logging Configuration
LOG_LEVEL=INFO

# File Configuration
MAX_FILE_SIZE=50
MAX_POLL_OPTIONS=10

# Admin Configuration
ADMIN_USER_IDS=123456789,987654321
```

## 🎯 دستورات Docker

### اجرای ربات
```bash
# اجرای کامل
./docker-run.sh

# اجرای دستی
docker compose up -d

# اجرای با لاگ
docker compose up
```

### توقف ربات
```bash
# توقف کامل
./docker-stop.sh

# توقف دستی
docker compose down

# توقف و حذف volumes
docker compose down -v
```

### مشاهده لاگ‌ها
```bash
# مشاهده لاگ‌ها
./docker-logs.sh

# مشاهده لاگ‌های زنده
./docker-logs.sh -f

# مشاهده لاگ‌های سرویس خاص
./docker-logs.sh -s telegram-bot

# مشاهده آخرین 50 خط
./docker-logs.sh -n 50
```

### مدیریت سرویس‌ها
```bash
# مشاهده وضعیت
docker compose ps

# راه‌اندازی مجدد
docker compose restart

# مشاهده دیتابیس
docker compose --profile tools run database-viewer

# مانیتورینگ
docker compose --profile monitoring up bot-monitor
```

## 🔧 تنظیمات پیشرفته

### Docker Compose Profiles

#### سرویس اصلی (پیش‌فرض)
```bash
docker compose up -d
```

#### ابزارها (Tools)
```bash
docker compose --profile tools up database-viewer
```

#### مانیتورینگ (Monitoring)
```bash
docker compose --profile monitoring up bot-monitor
```

### تنظیمات Volume
```yaml
volumes:
  - ./data:/app/data          # دیتابیس
  - ./logs:/app/logs          # لاگ‌ها
```

### تنظیمات Network
```yaml
networks:
  bot-network:
    driver: bridge
```

## 📊 مانیتورینگ

### Health Check
```bash
# بررسی وضعیت سلامت
docker compose ps

# بررسی لاگ‌های سلامت
docker compose logs telegram-bot | grep health
```

### آمار استفاده
```bash
# آمار منابع
docker stats

# آمار سرویس خاص
docker stats telegram-bot
```

## 🛠️ عیب‌یابی

### مشکلات رایج

#### 1. خطای "Container not found"
```bash
# بررسی containers
docker ps -a

# راه‌اندازی مجدد
docker compose up -d
```

#### 2. خطای "Permission denied"
```bash
# تنظیم مجوزها
chmod +x docker-*.sh

# اجرا با sudo (در صورت نیاز)
sudo docker compose up -d
```

#### 3. خطای "Port already in use"
```bash
# بررسی پورت‌های استفاده شده
netstat -tulpn | grep :8443

# تغییر پورت در docker compose.yml
```

#### 4. خطای "Database locked"
```bash
# توقف سرویس
docker compose down

# حذف دیتابیس (در صورت نیاز)
rm -f data/bot_database.db

# راه‌اندازی مجدد
docker compose up -d
```

### لاگ‌های خطا
```bash
# مشاهده تمام لاگ‌ها
docker compose logs

# مشاهده لاگ‌های خطا
docker compose logs | grep ERROR

# مشاهده لاگ‌های اخیر
docker compose logs --tail=100
```

## 🔄 به‌روزرسانی

### به‌روزرسانی کد
```bash
# دریافت آخرین تغییرات
git pull

# ساخت مجدد image
docker compose build

# راه‌اندازی مجدد
docker compose up -d
```

### به‌روزرسانی Docker
```bash
# به‌روزرسانی Docker
sudo apt update && sudo apt upgrade docker.io

# به‌روزرسانی Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker compose
sudo chmod +x /usr/local/bin/docker compose
```

## 📁 ساختار فایل‌ها

```
telegram-bot/
├── Dockerfile                 # Docker image definition
├── docker compose.yml        # Docker Compose configuration
├── .dockerignore            # Docker ignore file
├── docker.env              # Environment template
├── docker-run.sh           # Run script
├── docker-stop.sh          # Stop script
├── docker-logs.sh          # Logs script
├── data/                   # Database directory
├── logs/                   # Logs directory
└── src/                    # Source code
```

## 🚀 Production Deployment

### تنظیمات Production
```yaml
# docker compose.prod.yml
version: '3.8'
services:
  telegram-bot:
    restart: always
    environment:
      - LOG_LEVEL=WARNING
    volumes:
      - /var/lib/telegram-bot/data:/app/data
      - /var/lib/telegram-bot/logs:/app/logs
```

### اجرای Production
```bash
docker compose -f docker compose.yml -f docker compose.prod.yml up -d
```

## 📞 پشتیبانی

### گزارش مشکل
1. بررسی لاگ‌ها: `./docker-logs.sh`
2. بررسی وضعیت: `docker compose ps`
3. بررسی منابع: `docker stats`
4. گزارش مشکل با جزئیات

### دستورات مفید
```bash
# پاک‌سازی کامل
docker compose down -v --rmi all

# بازسازی کامل
docker compose build --no-cache

# مشاهده حجم استفاده
docker system df

# پاک‌سازی سیستم
docker system prune -a
```

---

**نکته:** این راهنما برای اجرای ربات در محیط Docker طراحی شده است. برای اجرای محلی، از راهنمای اصلی استفاده کنید.
