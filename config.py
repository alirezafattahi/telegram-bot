#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration file for Telegram Bot
"""

import os
from typing import Optional

class Config:
    """Bot configuration class"""
    
    # Bot settings
    BOT_TOKEN: Optional[str] = os.getenv('TELEGRAM_BOT_TOKEN')
    BOT_USERNAME: Optional[str] = os.getenv('BOT_USERNAME', 'your_bot_username')
    
    # Database settings
    DATABASE_PATH: str = os.getenv('DATABASE_PATH', 'bot_database.db')
    
    # Logging settings
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # File settings
    MAX_FILE_SIZE: int = int(os.getenv('MAX_FILE_SIZE', '50')) * 1024 * 1024  # 50MB default
    ALLOWED_FILE_TYPES: list = [
        'image/jpeg', 'image/png', 'image/gif',
        'application/pdf', 'text/plain',
        'audio/mpeg', 'video/mp4',
        'application/zip'
    ]
    
    # Poll settings
    MAX_POLL_OPTIONS: int = int(os.getenv('MAX_POLL_OPTIONS', '10'))
    MAX_POLL_QUESTION_LENGTH: int = int(os.getenv('MAX_POLL_QUESTION_LENGTH', '300'))
    
    # Admin settings
    ADMIN_USER_IDS: list = [
        int(user_id) for user_id in os.getenv('ADMIN_USER_IDS', '').split(',')
        if user_id.strip()
    ]
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        if not cls.BOT_TOKEN:
            print("❌ TELEGRAM_BOT_TOKEN is required!")
            return False
        return True
    
    @classmethod
    def get_database_url(cls) -> str:
        """Get database URL"""
        return f"sqlite:///{cls.DATABASE_PATH}"
