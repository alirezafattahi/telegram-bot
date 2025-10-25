#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Startup script for Telegram Bot
"""

import os
import sys
from telegram_bot import TelegramBot
from config import Config

def main():
    """Main startup function"""
    print("🤖 Starting Telegram Bot...")
    
    # Validate configuration
    if not Config.validate():
        sys.exit(1)
    
    # Create bot instance
    try:
        bot = TelegramBot(Config.BOT_TOKEN)
        print("✅ Bot initialized successfully!")
        print(f"📊 Database: {Config.DATABASE_PATH}")
        print(f"🔧 Log Level: {Config.LOG_LEVEL}")
        print("🚀 Starting bot...")
        
        # Run bot
        bot.run()
        
    except KeyboardInterrupt:
        print("\n⏹️ Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
