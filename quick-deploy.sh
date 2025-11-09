#!/bin/bash

# Quick Deploy Script - AI Army Deploy

echo "🚀 AI Army Quick Deploy"
echo "======================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Run deployment
echo ""
echo "Choose action:"
echo "1. Deploy all sites"
echo "2. Deploy single site"
echo "3. List sites"
echo "4. Check status"
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        python3 deploy.py all
        ;;
    2)
        read -p "Enter site name: " site_name
        python3 deploy.py site --name "$site_name"
        ;;
    3)
        python3 deploy.py list
        ;;
    4)
        python3 deploy.py status
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac
