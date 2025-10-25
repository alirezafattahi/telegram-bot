#!/bin/bash

# Docker Run Script for Telegram Bot
# اسکریپت اجرای Docker برای ربات تلگرام

set -e

echo "🐳 Docker Telegram Bot Runner"
echo "=============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p data logs

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from template..."
    cp docker.env .env
    print_warning "Please edit .env file and add your bot token!"
    print_warning "Example: TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
    exit 1
fi

# Load environment variables
source .env

# Check if bot token is set
if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ "$TELEGRAM_BOT_TOKEN" = "your_bot_token_here" ]; then
    print_error "TELEGRAM_BOT_TOKEN is not set or is default value!"
    print_error "Please edit .env file and set your bot token."
    exit 1
fi

print_header "🚀 Starting Telegram Bot with Docker..."

# Build the image
print_status "Building Docker image..."
docker compose build

# Start the services
print_status "Starting services..."
docker compose up -d

# Wait for bot to start
print_status "Waiting for bot to start..."
sleep 5

# Check if bot is running
if docker compose ps | grep -q "Up"; then
    print_status "✅ Bot is running successfully!"
    print_status "Container status:"
    docker compose ps
    
    print_header "📋 Useful Commands:"
    echo "  View logs: docker compose logs -f"
    echo "  Stop bot: docker compose down"
    echo "  Restart bot: docker compose restart"
    echo "  View database: docker compose --profile tools run database-viewer"
    echo "  Monitor bot: docker compose --profile monitoring up bot-monitor"
    
else
    print_error "❌ Bot failed to start!"
    print_error "Check logs with: docker compose logs"
    exit 1
fi

print_header "🎉 Telegram Bot is now running in Docker!"
print_status "Check your bot in Telegram and send /start command."
