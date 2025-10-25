#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run Simple Telegram Bot
اجرای ربات تلگرام ساده
"""

import os
from simple_telegram_bot import SimpleTelegramBot

def main():
    """Main function"""
    print("🤖 ربات تلگرام ساده")
    print("=" * 30)
    
    # Get bot token from environment or user input
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        print("❌ لطفاً متغیر محیطی TELEGRAM_BOT_TOKEN را تنظیم کنید.")
        print("مثال: export TELEGRAM_BOT_TOKEN='your_bot_token_here'")
        print("\nیا توکن را مستقیماً در کد وارد کنید:")
        print("bot_token = 'YOUR_BOT_TOKEN_HERE'")
        return
    
    print(f"✅ توکن ربات: {bot_token[:10]}...")
    print("🚀 شروع ربات...")
    
    # Create and run bot
    bot = SimpleTelegramBot(bot_token)
    bot.run()

if __name__ == '__main__':
    main()
