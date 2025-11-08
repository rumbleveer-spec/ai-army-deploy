#!/bin/bash

# Hostinger-specific deployment script
# Optimized for Hostinger shared hosting

echo "🌐 Hostinger Deployment Script"
echo "=============================="

# Hostinger Configuration
FTP_HOST="${HOSTINGER_FTP_HOST}"
FTP_USER="${HOSTINGER_FTP_USER}"
FTP_PASS="${HOSTINGER_FTP_PASS}"
REMOTE_DIR="public_html"

# Function: Deploy via FTP
deploy_ftp() {
    local site_name=$1
    local local_dir=$2

    echo "📤 Uploading $site_name to Hostinger..."

    lftp -f "
    open $FTP_HOST
    user $FTP_USER $FTP_PASS
    lcd $local_dir
    cd $REMOTE_DIR/$site_name
    mirror --reverse --delete --verbose --exclude-glob .git
    bye
    "

    echo "✅ $site_name uploaded successfully!"
}

# Deploy all sites
for i in {1..15}; do
    deploy_ftp "site$i" "/path/to/site$i"
done

echo "🎉 All sites deployed to Hostinger!"
