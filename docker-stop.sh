#!/bin/bash

# Docker Stop Script for Telegram Bot
# اسکریپت توقف Docker برای ربات تلگرام

set -e

echo "🛑 Stopping Telegram Bot Docker Container"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Check if Docker Compose is installed
if ! command -v docker compose &> /dev/null; then
    print_error "Docker Compose is not installed."
    exit 1
fi

print_header "🛑 Stopping Telegram Bot..."

# Stop all services
print_status "Stopping all services..."
docker compose down

# Stop with profiles
print_status "Stopping monitoring services..."
docker compose --profile monitoring down 2>/dev/null || true

print_status "Stopping tool services..."
docker compose --profile tools down 2>/dev/null || true

# Remove containers
print_status "Removing containers..."
docker compose rm -f

# Show status
print_status "Current container status:"
docker compose ps

print_header "✅ Telegram Bot stopped successfully!"
print_status "All containers have been stopped and removed."
