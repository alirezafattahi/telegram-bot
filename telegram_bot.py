#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot with comprehensive features:
- User data collection and management
- File upload/download
- Photo sending
- Polling/survey system
- Database with viewing capabilities
"""

import logging
import os
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Poll
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)
from telegram.constants import ParseMode

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, token: str):
        self.token = token
        self.application = Application.builder().token(token).build()
        self.db_path = "bot_database.db"
        self.init_database()
        self.setup_handlers()
    
    def init_database(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                phone_number TEXT,
                email TEXT,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Files table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                file_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                file_name TEXT,
                file_type TEXT,
                file_size INTEGER,
                telegram_file_id TEXT,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Polls table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS polls (
                poll_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                question TEXT,
                options TEXT,
                poll_type TEXT,
                creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Poll responses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS poll_responses (
                response_id INTEGER PRIMARY KEY AUTOINCREMENT,
                poll_id INTEGER,
                user_id INTEGER,
                selected_option TEXT,
                response_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (poll_id) REFERENCES polls (poll_id),
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def setup_handlers(self):
        """Setup all bot command and message handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("profile", self.profile_command))
        self.application.add_handler(CommandHandler("update_profile", self.update_profile_command))
        self.application.add_handler(CommandHandler("upload", self.upload_command))
        self.application.add_handler(CommandHandler("my_files", self.my_files_command))
        self.application.add_handler(CommandHandler("send_photo", self.send_photo_command))
        self.application.add_handler(CommandHandler("create_poll", self.create_poll_command))
        self.application.add_handler(CommandHandler("view_database", self.view_database_command))
        self.application.add_handler(CommandHandler("admin_stats", self.admin_stats_command))
        
        # Message handlers
        self.application.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        self.application.add_handler(MessageHandler(filters.Document.ALL, self.handle_document))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
        
        # Callback query handlers
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        user_id = user.id
        
        # Register user in database
        self.register_user(user)
        
        welcome_text = f"""
🤖 سلام {user.first_name}! به ربات تلگرام خوش آمدید!

این ربات دارای قابلیت‌های زیر است:
• 📝 مدیریت پروفایل کاربری
• 📁 آپلود و دانلود فایل
• 📸 ارسال عکس
• 📊 ایجاد نظرسنجی
• 🗄️ مشاهده دیتابیس

برای شروع از دستور /help استفاده کنید.
        """
        
        keyboard = [
            [InlineKeyboardButton("📝 پروفایل من", callback_data="profile")],
            [InlineKeyboardButton("📁 فایل‌های من", callback_data="my_files")],
            [InlineKeyboardButton("📊 ایجاد نظرسنجی", callback_data="create_poll")],
            [InlineKeyboardButton("🗄️ مشاهده دیتابیس", callback_data="view_db")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
📋 لیست دستورات ربات:

👤 مدیریت پروفایل:
/profile - مشاهده پروفایل
/update_profile - به‌روزرسانی پروفایل

📁 مدیریت فایل:
/upload - آپلود فایل
/download - دانلود فایل
/my_files - مشاهده فایل‌های من

📸 عکس:
/send_photo - ارسال عکس

📊 نظرسنجی:
/create_poll - ایجاد نظرسنجی جدید

🗄️ دیتابیس:
/view_database - مشاهده اطلاعات دیتابیس
/admin_stats - آمار کلی (برای ادمین)

💡 نکته: می‌توانید فایل‌ها و عکس‌ها را مستقیماً ارسال کنید!
        """
        await update.message.reply_text(help_text)
    
    def register_user(self, user):
        """Register or update user in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO users 
            (user_id, username, first_name, last_name, registration_date, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user.id,
            user.username,
            user.first_name,
            user.last_name,
            datetime.now(),
            1
        ))
        
        conn.commit()
        conn.close()
    
    async def profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /profile command"""
        user_id = update.effective_user.id
        user_data = self.get_user_data(user_id)
        
        if user_data:
            profile_text = f"""
👤 پروفایل شما:

🆔 شناسه کاربری: {user_data['user_id']}
👤 نام: {user_data['first_name']} {user_data['last_name'] or ''}
📧 ایمیل: {user_data['email'] or 'ثبت نشده'}
📱 شماره تلفن: {user_data['phone_number'] or 'ثبت نشده'}
📅 تاریخ عضویت: {user_data['registration_date']}
            """
        else:
            profile_text = "❌ اطلاعات کاربری یافت نشد!"
        
        keyboard = [
            [InlineKeyboardButton("✏️ ویرایش پروفایل", callback_data="edit_profile")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(profile_text, reply_markup=reply_markup)
    
    def get_user_data(self, user_id):
        """Get user data from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        
        if result:
            columns = [description[0] for description in cursor.description]
            user_data = dict(zip(columns, result))
        else:
            user_data = None
        
        conn.close()
        return user_data
    
    async def update_profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /update_profile command"""
        text = """
✏️ برای به‌روزرسانی پروفایل، لطفاً اطلاعات زیر را ارسال کنید:

📧 ایمیل: example@email.com
📱 شماره تلفن: 09123456789

فرمت: 
email: your_email@example.com
phone: your_phone_number
        """
        await update.message.reply_text(text)
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages for profile updates"""
        text = update.message.text.lower()
        user_id = update.effective_user.id
        
        # Check if it's a command (starts with /)
        if text.startswith('/'):
            # Let command handlers deal with it
            return
        
        if "email:" in text or "phone:" in text:
            await self.process_profile_update(update, text, user_id)
        else:
            await update.message.reply_text("❓ متوجه نشدم. از دستور /help استفاده کنید.")
    
    async def process_profile_update(self, update: Update, text: str, user_id: int):
        """Process profile update from text message"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        email = None
        phone = None
        
        lines = text.split('\n')
        for line in lines:
            if line.strip().startswith('email:'):
                email = line.split(':', 1)[1].strip()
            elif line.strip().startswith('phone:'):
                phone = line.split(':', 1)[1].strip()
        
        if email or phone:
            cursor.execute('''
                UPDATE users 
                SET email = COALESCE(?, email), 
                    phone_number = COALESCE(?, phone_number)
                WHERE user_id = ?
            ''', (email, phone, user_id))
            
            conn.commit()
            conn.close()
            
            await update.message.reply_text("✅ پروفایل با موفقیت به‌روزرسانی شد!")
        else:
            await update.message.reply_text("❌ فرمت صحیح نیست. لطفاً دوباره تلاش کنید.")
    
    async def upload_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /upload command"""
        text = """
📁 برای آپلود فایل، کافیست فایل مورد نظر را ارسال کنید.

پشتیبانی از انواع فایل:
• 📄 اسناد (PDF, DOC, TXT, ...)
• 🖼️ تصاویر (JPG, PNG, GIF, ...)
• 🎵 فایل‌های صوتی (MP3, WAV, ...)
• 🎬 ویدیو (MP4, AVI, ...)
        """
        await update.message.reply_text(text)
    
    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle document uploads"""
        user_id = update.effective_user.id
        document = update.message.document
        
        # Save file info to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO files (user_id, file_name, file_type, file_size, telegram_file_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            user_id,
            document.file_name,
            document.mime_type,
            document.file_size,
            document.file_id
        ))
        
        conn.commit()
        conn.close()
        
        await update.message.reply_text(
            f"✅ فایل با موفقیت آپلود شد!\n"
            f"📄 نام فایل: {document.file_name}\n"
            f"📊 حجم: {document.file_size} بایت\n"
            f"🔗 شناسه فایل: {document.file_id}"
        )
    
    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle photo uploads"""
        user_id = update.effective_user.id
        photo = update.message.photo[-1]  # Get highest resolution
        
        # Save photo info to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO files (user_id, file_name, file_type, file_size, telegram_file_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            user_id,
            f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
            "image/jpeg",
            photo.file_size,
            photo.file_id
        ))
        
        conn.commit()
        conn.close()
        
        await update.message.reply_text(
            f"📸 عکس با موفقیت آپلود شد!\n"
            f"📊 حجم: {photo.file_size} بایت\n"
            f"🔗 شناسه فایل: {photo.file_id}"
        )
    
    async def my_files_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /my_files command"""
        user_id = update.effective_user.id
        files = self.get_user_files(user_id)
        
        if files:
            text = "📁 فایل‌های شما:\n\n"
            for i, file in enumerate(files, 1):
                text += f"{i}. 📄 {file['file_name']}\n"
                text += f"   📊 حجم: {file['file_size']} بایت\n"
                text += f"   📅 تاریخ: {file['upload_date']}\n\n"
        else:
            text = "📭 هیچ فایلی آپلود نکرده‌اید."
        
        keyboard = [
            [InlineKeyboardButton("📥 دانلود فایل", callback_data="download_file")],
            [InlineKeyboardButton("🗑️ حذف فایل", callback_data="delete_file")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text, reply_markup=reply_markup)
    
    def get_user_files(self, user_id):
        """Get user files from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM files WHERE user_id = ? ORDER BY upload_date DESC
        ''', (user_id,))
        
        results = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        files = [dict(zip(columns, row)) for row in results]
        
        conn.close()
        return files
    
    async def send_photo_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /send_photo command"""
        text = """
📸 برای ارسال عکس، کافیست عکس مورد نظر را ارسال کنید.

همچنین می‌توانید از عکس‌های آپلود شده قبلی استفاده کنید:
        """
        
        user_id = update.effective_user.id
        photos = self.get_user_photos(user_id)
        
        if photos:
            keyboard = []
            for photo in photos[:5]:  # Show max 5 photos
                keyboard.append([
                    InlineKeyboardButton(
                        f"📸 {photo['file_name']}", 
                        callback_data=f"send_photo_{photo['file_id']}"
                    )
                ])
            reply_markup = InlineKeyboardMarkup(keyboard)
        else:
            reply_markup = None
        
        await update.message.reply_text(text, reply_markup=reply_markup)
    
    def get_user_photos(self, user_id):
        """Get user photos from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM files 
            WHERE user_id = ? AND file_type LIKE 'image%' 
            ORDER BY upload_date DESC
        ''', (user_id,))
        
        results = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        photos = [dict(zip(columns, row)) for row in results]
        
        conn.close()
        return photos
    
    async def create_poll_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /create_poll command"""
        text = """
📊 برای ایجاد نظرسنجی، لطفاً اطلاعات زیر را ارسال کنید:

فرمت:
سوال: سوال نظرسنجی شما
گزینه1: گزینه اول
گزینه2: گزینه دوم
گزینه3: گزینه سوم
...

مثال:
سوال: بهترین زبان برنامه‌نویسی کدام است؟
گزینه1: Python
گزینه2: JavaScript
گزینه3: Java
        """
        await update.message.reply_text(text)
    
    async def view_database_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /view_database command"""
        stats = self.get_database_stats()
        
        text = f"""
🗄️ آمار دیتابیس:

👥 تعداد کاربران: {stats['users_count']}
📁 تعداد فایل‌ها: {stats['files_count']}
📊 تعداد نظرسنجی‌ها: {stats['polls_count']}
💾 حجم دیتابیس: {stats['db_size']} KB

📈 آمار تفصیلی:
• کاربران فعال: {stats['active_users']}
• فایل‌های امروز: {stats['today_files']}
• نظرسنجی‌های فعال: {stats['active_polls']}
        """
        
        keyboard = [
            [InlineKeyboardButton("👥 لیست کاربران", callback_data="list_users")],
            [InlineKeyboardButton("📁 لیست فایل‌ها", callback_data="list_files")],
            [InlineKeyboardButton("📊 لیست نظرسنجی‌ها", callback_data="list_polls")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text, reply_markup=reply_markup)
    
    def get_database_stats(self):
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get file size
        db_size = os.path.getsize(self.db_path) / 1024  # KB
        
        # Count users
        cursor.execute('SELECT COUNT(*) FROM users')
        users_count = cursor.fetchone()[0]
        
        # Count active users
        cursor.execute('SELECT COUNT(*) FROM users WHERE is_active = 1')
        active_users = cursor.fetchone()[0]
        
        # Count files
        cursor.execute('SELECT COUNT(*) FROM files')
        files_count = cursor.fetchone()[0]
        
        # Count today's files
        cursor.execute('''
            SELECT COUNT(*) FROM files 
            WHERE DATE(upload_date) = DATE('now')
        ''')
        today_files = cursor.fetchone()[0]
        
        # Count polls
        cursor.execute('SELECT COUNT(*) FROM polls')
        polls_count = cursor.fetchone()[0]
        
        # Count active polls
        cursor.execute('SELECT COUNT(*) FROM polls WHERE is_active = 1')
        active_polls = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'users_count': users_count,
            'active_users': active_users,
            'files_count': files_count,
            'today_files': today_files,
            'polls_count': polls_count,
            'active_polls': active_polls,
            'db_size': round(db_size, 2)
        }
    
    async def admin_stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /admin_stats command"""
        stats = self.get_database_stats()
        
        text = f"""
🔧 آمار مدیریتی:

📊 آمار کلی:
• کل کاربران: {stats['users_count']}
• کاربران فعال: {stats['active_users']}
• کل فایل‌ها: {stats['files_count']}
• فایل‌های امروز: {stats['today_files']}
• کل نظرسنجی‌ها: {stats['polls_count']}
• نظرسنجی‌های فعال: {stats['active_polls']}

💾 سیستم:
• حجم دیتابیس: {stats['db_size']} KB
• وضعیت: ✅ آنلاین
        """
        
        await update.message.reply_text(text)
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle callback queries"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "profile":
            await self.profile_command(update, context)
        elif query.data == "my_files":
            await self.my_files_command(update, context)
        elif query.data == "create_poll":
            await self.create_poll_command(update, context)
        elif query.data == "view_db":
            await self.view_database_command(update, context)
        elif query.data == "edit_profile":
            await self.update_profile_command(update, context)
        elif query.data.startswith("send_photo_"):
            file_id = query.data.split("_")[2]
            await self.send_stored_photo(update, context, file_id)
        elif query.data == "download_file":
            await self.show_download_options(update, context)
        elif query.data.startswith("download_"):
            file_id = query.data.split("_")[1]
            await self.download_file(update, context, file_id)
        elif query.data.startswith("delete_"):
            file_id = query.data.split("_")[1]
            await self.delete_file(update, context, file_id)
    
    async def send_stored_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE, file_id: str):
        """Send a stored photo"""
        try:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=file_id,
                caption="📸 عکس ارسال شده از گالری شما"
            )
        except Exception as e:
            await query.edit_message_text(f"❌ خطا در ارسال عکس: {str(e)}")
    
    async def show_download_options(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show download options for user files"""
        user_id = update.effective_user.id
        files = self.get_user_files(user_id)
        
        if not files:
            await update.callback_query.edit_message_text("📭 هیچ فایلی برای دانلود وجود ندارد.")
            return
        
        text = "📥 انتخاب فایل برای دانلود:\n\n"
        keyboard = []
        
        for i, file in enumerate(files[:10]):  # Limit to 10 files
            text += f"{i+1}. 📄 {file['file_name']}\n"
            keyboard.append([
                InlineKeyboardButton(
                    f"📥 {file['file_name'][:20]}...",
                    callback_data=f"download_{file['file_id']}"
                )
            ])
        
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="my_files")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    
    async def download_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE, file_id: str):
        """Download a file"""
        try:
            # Get file info from database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM files WHERE telegram_file_id = ?', (file_id,))
            file_data = cursor.fetchone()
            conn.close()
            
            if not file_data:
                await update.callback_query.edit_message_text("❌ فایل یافت نشد.")
                return
            
            # Send the file
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=file_id,
                caption=f"📥 {file_data[2]}"  # file_name
            )
            
            await update.callback_query.answer("✅ فایل ارسال شد!")
            
        except Exception as e:
            await update.callback_query.edit_message_text(f"❌ خطا در دانلود فایل: {str(e)}")
    
    async def delete_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE, file_id: str):
        """Delete a file from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM files WHERE telegram_file_id = ?', (file_id,))
            conn.commit()
            conn.close()
            
            await update.callback_query.edit_message_text("✅ فایل حذف شد.")
            
        except Exception as e:
            await update.callback_query.edit_message_text(f"❌ خطا در حذف فایل: {str(e)}")
    
    def run(self):
        """Start the bot"""
        logger.info("Starting Telegram Bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Main function"""
    # Get bot token from environment variable
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        print("❌ لطفاً متغیر محیطی TELEGRAM_BOT_TOKEN را تنظیم کنید.")
        print("مثال: export TELEGRAM_BOT_TOKEN='your_bot_token_here'")
        return
    
    # Create and run bot
    bot = TelegramBot(bot_token)
    bot.run()

if __name__ == '__main__':
    main()
