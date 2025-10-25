#!/bin/bash

# Quick Start Script for Docker Telegram Bot
# اسکریپت شروع سریع Docker برای ربات تلگرام

set -e

echo "🚀 Quick Start - Docker Telegram Bot"
echo "===================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}$1${NC}"
}

# Check Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed!"
    print_status "Please install Docker first:"
    echo "  Ubuntu/Debian: sudo apt install docker.io docker compose"
    echo "  CentOS/RHEL: sudo yum install docker docker compose"
    exit 1
fi

# Check Docker Compose
if ! command -v docker compose &> /dev/null; then
    print_error "Docker Compose is not installed!"
    exit 1
fi

print_header "🐳 Setting up Docker Telegram Bot..."

# Create directories
print_status "Creating directories..."
mkdir -p data logs

# Check if .env exists
if [ ! -f ".env" ]; then
    print_warning "Creating .env file from template..."
    cp docker.env .env
    print_warning "⚠️  Please edit .env file and add your bot token!"
    print_warning "   Example: TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
    print_warning "   Then run this script again."
    exit 1
fi

# Load environment
source .env

# Check bot token
if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ "$TELEGRAM_BOT_TOKEN" = "your_bot_token_here" ]; then
    print_error "TELEGRAM_BOT_TOKEN is not set!"
    print_status "Please edit .env file and set your bot token."
    exit 1
fi

print_header "🔧 Building and starting bot..."

# Build image
print_status "Building Docker image..."
docker compose build

# Start services
print_status "Starting services..."
docker compose up -d

# Wait for startup
print_status "Waiting for bot to start..."
sleep 10

# Check status
if docker compose ps | grep -q "Up"; then
    print_header "✅ Bot is running successfully!"
    
    print_status "📋 Container status:"
    docker compose ps
    
    print_header "🎯 Next steps:"
    echo "1. Open Telegram and find your bot"
    echo "2. Send /start command"
    echo "3. Test bot functionality"
    
    print_header "📋 Useful commands:"
    echo "  View logs: ./docker-logs.sh"
    echo "  Stop bot: ./docker-stop.sh"
    echo "  Restart: docker compose restart"
    echo "  Database viewer: docker compose --profile tools run database-viewer"
    
    print_header "🎉 Your Telegram Bot is now running in Docker!"
    
else
    print_error "❌ Bot failed to start!"
    print_error "Check logs: ./docker-logs.sh"
    exit 1
fi
