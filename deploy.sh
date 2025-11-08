#!/bin/bash

# AI Army Deploy - Master Deployment Script
# Automated deployment for 15 websites

set -e

echo "🚀 AI Army HQ - Master Deployment System"
echo "========================================"

# Configuration
DEPLOY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$DEPLOY_DIR/config.yml"
LOG_DIR="$DEPLOY_DIR/logs"
mkdir -p "$LOG_DIR"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Load environment
if [ -f ".env" ]; then
    export $(cat .env | xargs)
else
    echo "${RED}❌ .env file not found!${NC}"
    exit 1
fi

# Function: Deploy single site
deploy_site() {
    local site_name=$1
    local site_dir=$2
    local site_url=$3

    echo "${YELLOW}📦 Deploying: $site_name${NC}"

    # Git pull latest
    cd "$site_dir" || return 1
    git pull origin main

    # Install dependencies
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    elif [ -f "package.json" ]; then
        npm install --production
    fi

    # Build if needed
    if [ -f "build.sh" ]; then
        bash build.sh
    fi

    # Restart service
    if command -v systemctl &> /dev/null; then
        sudo systemctl restart "$site_name"
    fi

    echo "${GREEN}✅ $site_name deployed successfully!${NC}"
    echo "🌐 URL: $site_url"
    echo ""
}

# Function: Deploy all sites
deploy_all() {
    local total_sites=15
    local deployed=0
    local failed=0

    echo "🔥 Deploying ALL 15 websites..."
    echo ""

    # Read sites from config
    while IFS=',' read -r name dir url; do
        if deploy_site "$name" "$dir" "$url"; then
            ((deployed++))
        else
            ((failed++))
            echo "${RED}❌ Failed to deploy $name${NC}"
        fi
    done < <(tail -n +2 "$CONFIG_FILE")

    echo "========================================"
    echo "${GREEN}✅ Deployed: $deployed/$total_sites${NC}"
    if [ $failed -gt 0 ]; then
        echo "${RED}❌ Failed: $failed/$total_sites${NC}"
    fi
    echo "========================================"
}

# Function: Check status
check_status() {
    echo "📊 Checking deployment status..."
    echo ""

    while IFS=',' read -r name dir url; do
        if curl -s --head "$url" | grep "200 OK" > /dev/null; then
            echo "${GREEN}✅ $name - ONLINE${NC} ($url)"
        else
            echo "${RED}❌ $name - OFFLINE${NC} ($url)"
        fi
    done < <(tail -n +2 "$CONFIG_FILE")
}

# Main menu
case "${1:-}" in
    "all")
        deploy_all
        ;;
    "status")
        check_status
        ;;
    "site")
        if [ -z "$2" ]; then
            echo "${RED}Usage: $0 site <site_name>${NC}"
            exit 1
        fi
        # Deploy specific site
        grep "^$2," "$CONFIG_FILE" | while IFS=',' read -r name dir url; do
            deploy_site "$name" "$dir" "$url"
        done
        ;;
    *)
        echo "Usage: $0 {all|status|site <name>}"
        echo ""
        echo "Commands:"
        echo "  all          - Deploy all 15 websites"
        echo "  status       - Check deployment status"
        echo "  site <name>  - Deploy specific website"
        exit 1
        ;;
esac

echo "🎉 Done!"
