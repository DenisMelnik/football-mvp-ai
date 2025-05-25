#!/bin/bash

# Football MVP Selector Agent - Automated Demo Script
# This script sets up the environment and runs a demonstration

set -e  # Exit on any error

# Change to the parent directory (project root)
cd "$(dirname "$0")/.."

echo "🚀 Football MVP Selector Agent - Automated Demo"
echo "=============================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_error ".env file not found!"
    print_info "Please copy env.template to .env and fill in your API keys:"
    print_info "  cp env.template .env"
    print_info "  # Edit .env with your API keys"
    exit 1
fi

print_status ".env file found"

# Check if virtual environment exists and is activated
if [ -z "$VIRTUAL_ENV" ]; then
    print_warning "Virtual environment not detected"
    if [ -d "venv" ]; then
        print_info "Activating virtual environment..."
        source venv/bin/activate
        print_status "Virtual environment activated"
    else
        print_error "Virtual environment not found!"
        print_info "Please create a virtual environment first:"
        print_info "  python -m venv venv"
        print_info "  source venv/bin/activate"
        print_info "  pip install -r requirements.txt"
        exit 1
    fi
else
    print_status "Virtual environment already activated"
fi

# Check if dependencies are installed
print_info "Checking dependencies..."
if ! python -c "import langchain_google_genai, langgraph, dotenv, requests" 2>/dev/null; then
    print_warning "Missing dependencies detected"
    print_info "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
    print_status "Dependencies installed"
else
    print_status "All dependencies are available"
fi

# Check environment variables
print_info "Checking environment variables..."
if ! python -c "
import os
from dotenv import load_dotenv
load_dotenv()

required_vars = ['RAPID_API_KEY', 'RAPID_API_HOST', 'GOOGLE_API_KEY']
missing = [var for var in required_vars if not os.getenv(var)]

if missing:
    print(f'Missing environment variables: {missing}')
    exit(1)
else:
    print('All required environment variables found')
" 2>/dev/null; then
    print_error "Environment variables are missing or invalid!"
    print_info "Please check your .env file and ensure these variables are set:"
    print_info "  RAPID_API_KEY=your_rapidapi_key"
    print_info "  RAPID_API_HOST=api-football-v1.p.rapidapi.com"
    print_info "  GOOGLE_API_KEY=your_google_api_key"
    exit 1
fi

print_status "Environment variables validated"

echo ""
print_info "Starting demo with Real Madrid vs Barcelona (2023-10-28)..."
echo ""

# Run the demo (now from demo directory)
python demo/demo.py

echo ""
print_status "Demo completed successfully!"
echo ""
print_info "You can also run the interactive version with:"
print_info "  python main.py"
echo ""
print_info "Or test different matches by modifying demo/demo.py" 