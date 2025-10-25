#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Telegram Bot without external dependencies
ربات تلگرام ساده بدون وابستگی خارجی
"""

import json
import sqlite3
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime
import os

class SimpleTelegramBot:
    """Simple Telegram Bot using HTTP requests"""
    
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.db_path = "bot_database.db"
        self.init_database()
    
    def init_database(self):
        """Initialize database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
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
        
        conn.commit()
        conn.close()
        print("✅ Database initialized")
    
    def send_message(self, chat_id, text, reply_markup=None):
        """Send message to chat"""
        url = f"{self.base_url}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        
        if reply_markup:
            data['reply_markup'] = json.dumps(reply_markup)
        
        try:
            req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode())
            response = urllib.request.urlopen(req)
            return json.loads(response.read().decode())
        except Exception as e:
            print(f"Error sending message: {e}")
            return None
    
    def get_updates(self, offset=None):
        """Get updates from Telegram"""
        url = f"{self.base_url}/getUpdates"
        if offset:
            url += f"?offset={offset}"
        
        try:
            response = urllib.request.urlopen(url)
            return json.loads(response.read().decode())
        except Exception as e:
            print(f"Error getting updates: {e}")
            return None
    
    def register_user(self, user):
        """Register user in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO users 
            (user_id, username, first_name, last_name, registration_date, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user['id'],
            user.get('username'),
            user.get('first_name'),
            user.get('last_name'),
            datetime.now(),
            1
        ))
        
        conn.commit()
        conn.close()
    
    def handle_message(self, message):
        """Handle incoming message"""
        chat_id = message['chat']['id']
        user = message['from']
        text = message.get('text', '')
        
        # Register user
        self.register_user(user)
        
        if text.startswith('/start'):
            welcome_text = f"""
🤖 سلام {user.get('first_name', 'کاربر')}! به ربات تلگرام خوش آمدید!

این ربات دارای قابلیت‌های زیر است:
• 📝 مدیریت پروفایل کاربری
• 📁 آپلود و دانلود فایل
• 📸 ارسال عکس
• 📊 ایجاد نظرسنجی
• 🗄️ مشاهده دیتابیس

برای شروع از دستور /help استفاده کنید.
            """
            self.send_message(chat_id, welcome_text)
        
        elif text.startswith('/help'):
            help_text = """
📋 لیست دستورات ربات:

👤 مدیریت پروفایل:
/profile - مشاهده پروفایل
/update_profile - به‌روزرسانی پروفایل

📁 مدیریت فایل:
/upload - آپلود فایل
/my_files - مشاهده فایل‌های من

📸 عکس:
/send_photo - ارسال عکس

📊 نظرسنجی:
/create_poll - ایجاد نظرسنجی جدید

🗄️ دیتابیس:
/view_database - مشاهده اطلاعات دیتابیس
/admin_stats - آمار کلی

💡 نکته: می‌توانید فایل‌ها و عکس‌ها را مستقیماً ارسال کنید!
            """
            self.send_message(chat_id, help_text)
        
        elif text.startswith('/profile'):
            user_data = self.get_user_data(user['id'])
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
            
            self.send_message(chat_id, profile_text)
        
        elif text.startswith('/update_profile'):
            update_text = """
✏️ برای به‌روزرسانی پروفایل، لطفاً اطلاعات زیر را ارسال کنید:

📧 ایمیل: example@email.com
📱 شماره تلفن: 09123456789

فرمت: 
email: your_email@example.com
phone: your_phone_number
            """
            self.send_message(chat_id, update_text)
        
        elif text.startswith('/my_files'):
            files = self.get_user_files(user['id'])
            if files:
                text = "📁 فایل‌های شما:\n\n"
                for i, file in enumerate(files, 1):
                    text += f"{i}. 📄 {file['file_name']}\n"
                    text += f"   📊 حجم: {file['file_size']} بایت\n"
                    text += f"   📅 تاریخ: {file['upload_date']}\n\n"
            else:
                text = "📭 هیچ فایلی آپلود نکرده‌اید."
            
            self.send_message(chat_id, text)
        
        elif text.startswith('/view_database'):
            stats = self.get_database_stats()
            text = f"""
🗄️ آمار دیتابیس:

👥 تعداد کاربران: {stats['users_count']}
📁 تعداد فایل‌ها: {stats['files_count']}
💾 حجم دیتابیس: {stats['db_size']} KB

📈 آمار تفصیلی:
• کاربران فعال: {stats['active_users']}
• فایل‌های امروز: {stats['today_files']}
            """
            self.send_message(chat_id, text)
        
        elif text.startswith('/admin_stats'):
            stats = self.get_database_stats()
            text = f"""
🔧 آمار مدیریتی:

📊 آمار کلی:
• کل کاربران: {stats['users_count']}
• کاربران فعال: {stats['active_users']}
• کل فایل‌ها: {stats['files_count']}
• فایل‌های امروز: {stats['today_files']}

💾 سیستم:
• حجم دیتابیس: {stats['db_size']} KB
• وضعیت: ✅ آنلاین
            """
            self.send_message(chat_id, text)
        
        else:
            # Handle profile updates
            if 'email:' in text.lower() or 'phone:' in text.lower():
                self.process_profile_update(chat_id, text, user['id'])
            else:
                self.send_message(chat_id, "❓ متوجه نشدم. از دستور /help استفاده کنید.")
    
    def process_profile_update(self, chat_id, text, user_id):
        """Process profile update"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        email = None
        phone = None
        
        lines = text.split('\n')
        for line in lines:
            if line.strip().lower().startswith('email:'):
                email = line.split(':', 1)[1].strip()
            elif line.strip().lower().startswith('phone:'):
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
            
            self.send_message(chat_id, "✅ پروفایل با موفقیت به‌روزرسانی شد!")
        else:
            self.send_message(chat_id, "❌ فرمت صحیح نیست. لطفاً دوباره تلاش کنید.")
    
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
        
        conn.close()
        
        return {
            'users_count': users_count,
            'active_users': active_users,
            'files_count': files_count,
            'today_files': today_files,
            'db_size': round(db_size, 2)
        }
    
    def run(self):
        """Run the bot"""
        print("🤖 Starting Simple Telegram Bot...")
        print("Press Ctrl+C to stop")
        
        offset = None
        
        try:
            while True:
                updates = self.get_updates(offset)
                
                if updates and updates.get('ok'):
                    for update in updates['result']:
                        offset = update['update_id'] + 1
                        
                        if 'message' in update:
                            self.handle_message(update['message'])
                
                import time
                time.sleep(1)  # Wait 1 second between requests
                
        except KeyboardInterrupt:
            print("\n⏹️ Bot stopped by user")
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main function"""
    # Get bot token
    bot_token = input("🤖 لطفاً توکن ربات خود را وارد کنید: ").strip()
    
    if not bot_token:
        print("❌ توکن ربات الزامی است!")
        return
    
    # Create and run bot
    bot = SimpleTelegramBot(bot_token)
    bot.run()

if __name__ == '__main__':
    main()
