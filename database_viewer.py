#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database viewer for Telegram Bot
"""

import sqlite3
import os
from datetime import datetime
from config import Config

class DatabaseViewer:
    """Database viewer class"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.DATABASE_PATH
    
    def view_users(self):
        """View all users"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, username, first_name, last_name, 
                   email, phone_number, registration_date, is_active
            FROM users ORDER BY registration_date DESC
        ''')
        
        users = cursor.fetchall()
        conn.close()
        
        print("\n👥 لیست کاربران:")
        print("-" * 80)
        print(f"{'ID':<10} {'نام کاربری':<15} {'نام':<15} {'ایمیل':<20} {'وضعیت':<8}")
        print("-" * 80)
        
        for user in users:
            status = "✅ فعال" if user[7] else "❌ غیرفعال"
            print(f"{user[0]:<10} {user[1] or 'N/A':<15} {user[2] or 'N/A':<15} {user[4] or 'N/A':<20} {status:<8}")
    
    def view_files(self):
        """View all files"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT f.file_id, f.user_id, f.file_name, f.file_type, 
                   f.file_size, f.upload_date, u.first_name
            FROM files f
            JOIN users u ON f.user_id = u.user_id
            ORDER BY f.upload_date DESC
        ''')
        
        files = cursor.fetchall()
        conn.close()
        
        print("\n📁 لیست فایل‌ها:")
        print("-" * 100)
        print(f"{'ID':<5} {'کاربر':<15} {'نام فایل':<20} {'نوع':<15} {'حجم':<10} {'تاریخ':<15}")
        print("-" * 100)
        
        for file in files:
            size_mb = file[4] / (1024 * 1024) if file[4] else 0
            print(f"{file[0]:<5} {file[6] or 'N/A':<15} {file[2][:20]:<20} {file[3][:15]:<15} {size_mb:.2f}MB {file[5][:15]:<15}")
    
    def view_polls(self):
        """View all polls"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.poll_id, p.user_id, p.question, p.options, 
                   p.creation_date, p.is_active, u.first_name
            FROM polls p
            JOIN users u ON p.user_id = u.user_id
            ORDER BY p.creation_date DESC
        ''')
        
        polls = cursor.fetchall()
        conn.close()
        
        print("\n📊 لیست نظرسنجی‌ها:")
        print("-" * 120)
        print(f"{'ID':<5} {'کاربر':<15} {'سوال':<40} {'گزینه‌ها':<30} {'تاریخ':<15} {'وضعیت':<8}")
        print("-" * 120)
        
        for poll in polls:
            status = "✅ فعال" if poll[5] else "❌ غیرفعال"
            question = poll[2][:40] if poll[2] else 'N/A'
            options = poll[3][:30] if poll[3] else 'N/A'
            print(f"{poll[0]:<5} {poll[6] or 'N/A':<15} {question:<40} {options:<30} {poll[4][:15]:<15} {status:<8}")
    
    def get_statistics(self):
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
        
        print("\n📊 آمار دیتابیس:")
        print("-" * 40)
        print(f"👥 کل کاربران: {users_count}")
        print(f"✅ کاربران فعال: {active_users}")
        print(f"📁 کل فایل‌ها: {files_count}")
        print(f"📁 فایل‌های امروز: {today_files}")
        print(f"📊 کل نظرسنجی‌ها: {polls_count}")
        print(f"📊 نظرسنجی‌های فعال: {active_polls}")
        print(f"💾 حجم دیتابیس: {db_size:.2f} KB")
    
    def interactive_menu(self):
        """Interactive menu for database viewing"""
        while True:
            print("\n" + "="*50)
            print("🗄️ مشاهده‌گر دیتابیس ربات تلگرام")
            print("="*50)
            print("1. 👥 مشاهده کاربران")
            print("2. 📁 مشاهده فایل‌ها")
            print("3. 📊 مشاهده نظرسنجی‌ها")
            print("4. 📈 آمار کلی")
            print("5. ❌ خروج")
            
            choice = input("\nانتخاب کنید (1-5): ").strip()
            
            if choice == '1':
                self.view_users()
            elif choice == '2':
                self.view_files()
            elif choice == '3':
                self.view_polls()
            elif choice == '4':
                self.get_statistics()
            elif choice == '5':
                print("👋 خداحافظ!")
                break
            else:
                print("❌ انتخاب نامعتبر!")
            
            input("\nبرای ادامه Enter را فشار دهید...")

def main():
    """Main function"""
    print("🗄️ مشاهده‌گر دیتابیس ربات تلگرام")
    
    # Check if database exists
    if not os.path.exists(Config.DATABASE_PATH):
        print(f"❌ دیتابیس یافت نشد: {Config.DATABASE_PATH}")
        print("ابتدا ربات را اجرا کنید تا دیتابیس ایجاد شود.")
        return
    
    # Create viewer and show menu
    viewer = DatabaseViewer()
    viewer.interactive_menu()

if __name__ == '__main__':
    main()
