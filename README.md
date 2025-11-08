# 🚀 AI Army Deploy

> Master Deployment Package for 15 Websites - Automated Deployment System

[![Deployment](https://img.shields.io/badge/deployment-automated-success)](https://github.com/rumbleveer-spec/ai-army-deploy)
[![Hostinger](https://img.shields.io/badge/hosting-hostinger-blue)](https://hostinger.com)
[![Bash](https://img.shields.io/badge/bash-5.0+-green)](https://www.gnu.org/software/bash/)

## 🎯 Overview

AI Army Deploy is a powerful automated deployment system designed to manage and deploy 15+ websites simultaneously with a single command. Perfect for agencies, developers managing multiple projects, or anyone who needs efficient multi-site deployment.

## ✨ Features

- 🚀 **One-Command Deployment** - Deploy all 15 sites with a single command
- 🌐 **Hostinger Optimized** - Built specifically for Hostinger hosting
- 🔄 **Automatic Updates** - Pull latest code from Git and deploy
- 📊 **Status Monitoring** - Real-time health checks for all sites
- 🔐 **Secure Configuration** - Environment-based credentials management
- 📝 **Detailed Logging** - Track all deployments with timestamped logs
- 🐳 **Docker Support** - Local testing with Docker Compose
- ⚡ **Parallel Deployment** - Deploy multiple sites simultaneously

## 🚀 Quick Start

### Prerequisites

- Bash 5.0+
- Git
- SSH access to server
- Hostinger account (or any hosting with FTP/SSH)

### Installation

```bash
# Clone the repository
git clone https://github.com/rumbleveer-spec/ai-army-deploy.git
cd ai-army-deploy

# Make scripts executable
chmod +x deploy.sh hostinger-deploy.sh

# Configure environment
cp .env.example .env
# Edit .env with your credentials
nano .env

# Update site configuration
nano config.yml
```

### Configuration

Edit `config.yml` with your site details:

```csv
site_name,directory,url
mysite1,/var/www/mysite1,https://mysite1.com
mysite2,/var/www/mysite2,https://mysite2.com
...
```

## 📖 Usage

### Deploy All Sites

```bash
./deploy.sh all
```

### Deploy Specific Site

```bash
./deploy.sh site mysite1
```

### Check Status

```bash
./deploy.sh status
```

### Hostinger Deployment

```bash
# Via FTP
./hostinger-deploy.sh

# Via SSH (if available)
ssh user@server "cd /path && ./deploy.sh all"
```

## 🏗️ Architecture

```
ai-army-deploy/
├── deploy.sh              # Main deployment script
├── hostinger-deploy.sh    # Hostinger-specific script
├── config.yml             # Site configuration
├── docker-compose.yml     # Local testing setup
├── .env.example           # Environment template
├── logs/                  # Deployment logs
│   ├── deploy-YYYYMMDD.log
│   └── errors.log
└── README.md             # This file
```

## 🔧 Advanced Features

### Automated Backups

Enable automatic backups before deployment:

```bash
# In .env
AUTO_BACKUP=true
BACKUP_DIR=/backups
```

### Slack Notifications

Get deployment notifications in Slack:

```bash
# In .env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx
```

### Rollback

Rollback to previous deployment:

```bash
./deploy.sh rollback site1
```

## 🎯 Deployment Workflow

1. **Pull Latest Code** - Fetch updates from Git
2. **Install Dependencies** - npm/pip install
3. **Build Assets** - Run build scripts
4. **Run Tests** - Execute test suites
5. **Deploy** - Copy files to production
6. **Restart Services** - Reload web services
7. **Verify** - Health check all sites
8. **Notify** - Send deployment notifications

## 📊 Monitoring

Monitor all sites with built-in health checks:

```bash
# Check all sites
./deploy.sh status

# Monitor continuously
watch -n 60 './deploy.sh status'
```

## 🐳 Docker Development

Test deployments locally with Docker:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔒 Security

- ✅ Environment-based credentials
- ✅ No hardcoded passwords
- ✅ SSH key authentication
- ✅ Encrypted connections
- ✅ Access logs

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Troubleshooting

### FTP Connection Failed

```bash
# Test FTP connection
lftp -u username,password ftp.example.com
```

### Permission Denied

```bash
# Fix file permissions
chmod +x deploy.sh
chmod 600 .env
```

### Site Not Loading

```bash
# Check logs
tail -f logs/deploy-$(date +%Y%m%d).log

# Verify site status
curl -I https://yoursite.com
```

## 📞 Support

- 📧 Email: support@example.com
- 💬 Issues: [GitHub Issues](https://github.com/rumbleveer-spec/ai-army-deploy/issues)
- 📖 Docs: [Full Documentation](https://docs.example.com)

## 🙏 Acknowledgments

- Hostinger for reliable hosting
- Open source community
- All contributors

---

**Built with ❤️ for Developers by Developers**

[Documentation](https://docs.example.com) • [Report Bug](https://github.com/rumbleveer-spec/ai-army-deploy/issues) • [Request Feature](https://github.com/rumbleveer-spec/ai-army-deploy/issues)
