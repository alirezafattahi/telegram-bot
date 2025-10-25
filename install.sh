#!/bin/bash

# Telegram Bot Installation Script
# اسکریپت نصب ربات تلگرام

echo "🤖 نصب ربات تلگرام پیشرفته"
echo "================================"

# Check Python version
echo "🔍 بررسی نسخه Python..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python3 نصب نیست. لطفاً ابتدا Python3 را نصب کنید."
    exit 1
fi

# Create virtual environment
echo "📦 ایجاد محیط مجازی..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 فعال‌سازی محیط مجازی..."
source venv/bin/activate

# Install requirements
echo "📥 نصب وابستگی‌ها..."
pip install --upgrade pip
pip install python-telegram-bot==20.7

# Create .env file template
echo "📝 ایجاد فایل تنظیمات..."
cat > .env.example << EOF
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
BOT_USERNAME=your_bot_username
DATABASE_PATH=bot_database.db
LOG_LEVEL=INFO
MAX_FILE_SIZE=50
MAX_POLL_OPTIONS=10
ADMIN_USER_IDS=123456789,987654321
EOF

# Make scripts executable
chmod +x run_bot.py
chmod +x database_viewer.py

echo "✅ نصب با موفقیت انجام شد!"
echo ""
echo "📋 مراحل بعدی:"
echo "1. توکن ربات خود را از @BotFather دریافت کنید"
echo "2. فایل .env را ایجاد کنید و توکن را وارد کنید:"
echo "   cp .env.example .env"
echo "   nano .env"
echo "3. ربات را اجرا کنید:"
echo "   python run_bot.py"
echo ""
echo "🗄️ برای مشاهده دیتابیس:"
echo "   python database_viewer.py"
echo ""
echo "📚 برای راهنمای کامل، فایل README.md را مطالعه کنید."
