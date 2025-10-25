# 🐳 Docker Quick Start Guide

راهنمای سریع اجرای ربات تلگرام با Docker

## ✅ مشکل حل شد!

مشکل `sqlite3` در `requirements.txt` حل شد. حالا می‌توانید ربات را با Docker اجرا کنید.

## 🚀 اجرای سریع

### 1️⃣ **تنظیم توکن**
```bash
# کپی کردن فایل نمونه
cp docker.env .env

# ویرایش فایل .env
nano .env
```

در فایل `.env` توکن ربات خود را وارد کنید:
```bash
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 2️⃣ **اجرای ربات**
```bash
# اجرای خودکار
./docker-quick-start.sh

# یا اجرای دستی
docker compose up -d
```

## 📋 دستورات مفید

### اجرا و توقف
```bash
# اجرای ربات
docker compose up -d

# توقف ربات
docker compose down

# راه‌اندازی مجدد
docker compose restart
```

### مشاهده وضعیت
```bash
# وضعیت containers
docker compose ps

# مشاهده لاگ‌ها
docker compose logs -f

# مشاهده لاگ‌های اخیر
docker compose logs --tail=100
```

### مدیریت دیتابیس
```bash
# مشاهده دیتابیس
docker compose --profile tools run database-viewer

# پشتیبان‌گیری از دیتابیس
docker cp telegram-bot:/app/data/bot_database.db ./backup.db
```

## 🔧 عیب‌یابی

### بررسی وضعیت
```bash
# بررسی containers
docker ps -a

# بررسی logs
docker compose logs telegram-bot

# بررسی منابع
docker stats
```

### مشکلات رایج

#### 1. خطای "Container not found"
```bash
# راه‌اندازی مجدد
docker compose down
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
# بررسی پورت‌ها
netstat -tulpn | grep :8443

# تغییر پورت در docker compose.yml
```

## 📊 مانیتورینگ

### Health Check
```bash
# بررسی سلامت
docker compose ps

# بررسی لاگ‌های سلامت
docker compose logs | grep health
```

### آمار استفاده
```bash
# آمار منابع
docker stats

# آمار سرویس خاص
docker stats telegram-bot
```

## 🎯 تست ربات

1. **اجرای ربات:**
   ```bash
   ./docker-quick-start.sh
   ```

2. **بررسی وضعیت:**
   ```bash
   docker compose ps
   ```

3. **مشاهده لاگ‌ها:**
   ```bash
   docker compose logs -f
   ```

4. **تست در تلگرام:**
   - به ربات خود پیام دهید
   - دستور `/start` را ارسال کنید
   - دستورات مختلف را تست کنید

## 📁 ساختار فایل‌ها

```
telegram-bot/
├── Dockerfile                 # Docker image
├── docker compose.yml        # Docker Compose
├── requirements-docker.txt   # Dependencies
├── docker.env               # Environment template
├── .env                     # Your environment
├── data/                    # Database directory
├── logs/                    # Logs directory
└── docker-*.sh             # Helper scripts
```

## 🎉 موفقیت!

ربات شما حالا با Docker اجرا می‌شود و آماده استفاده است!

### دستورات نهایی:
```bash
# اجرا
./docker-quick-start.sh

# مشاهده وضعیت
docker compose ps

# مشاهده لاگ‌ها
docker compose logs -f

# توقف
docker compose down
```

**نکته:** تمام فایل‌های Docker آماده است و مشکل `sqlite3` حل شده است! 🚀
