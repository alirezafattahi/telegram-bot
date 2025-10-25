#!/bin/bash

# Docker Logs Script for Telegram Bot
# اسکریپت مشاهده لاگ‌های Docker برای ربات تلگرام

set -e

echo "📋 Telegram Bot Docker Logs"
echo "==========================="

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

# Parse command line arguments
FOLLOW=false
SERVICE=""
LINES=100

while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--follow)
            FOLLOW=true
            shift
            ;;
        -s|--service)
            SERVICE="$2"
            shift 2
            ;;
        -n|--lines)
            LINES="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  -f, --follow     Follow log output"
            echo "  -s, --service    Service name (telegram-bot, database-viewer, bot-monitor)"
            echo "  -n, --lines      Number of lines to show (default: 100)"
            echo "  -h, --help       Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

print_header "📋 Showing Telegram Bot Logs..."

# Show logs
if [ -n "$SERVICE" ]; then
    print_status "Showing logs for service: $SERVICE"
    if [ "$FOLLOW" = true ]; then
        docker compose logs -f --tail="$LINES" "$SERVICE"
    else
        docker compose logs --tail="$LINES" "$SERVICE"
    fi
else
    print_status "Showing logs for all services"
    if [ "$FOLLOW" = true ]; then
        docker compose logs -f --tail="$LINES"
    else
        docker compose logs --tail="$LINES"
    fi
fi

print_header "✅ Logs displayed successfully!"
print_status "Use -f flag to follow logs in real-time"
print_status "Use -s flag to show logs for specific service"
