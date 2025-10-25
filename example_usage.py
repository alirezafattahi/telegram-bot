#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example usage of Telegram Bot
مثال استفاده از ربات تلگرام
"""

import os
from telegram_bot import TelegramBot

def example_usage():
    """Example of how to use the bot"""
    
    # Set your bot token
    bot_token = "YOUR_BOT_TOKEN_HERE"
    
    # Create bot instance
    bot = TelegramBot(bot_token)
    
    # Run the bot
    print("🤖 Starting bot...")
    bot.run()

if __name__ == '__main__':
    example_usage()
