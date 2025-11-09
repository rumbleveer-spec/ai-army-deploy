# 🚀 AI Army Deploy

> Professional Multi-Site Deployment Automation System

[![Python](https://img.shields.io/badge/python-3.8+-blue)](https://python.org)
[![Bash](https://img.shields.io/badge/bash-5.0+-green)](https://www.gnu.org/software/bash/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## ✨ Features

- 🎯 **Multi-Site Deployment** - Deploy 15+ websites simultaneously
- 🔄 **FTP & SSH Support** - Multiple deployment methods
- 📊 **Status Monitoring** - Real-time health checks
- 📝 **Detailed Logging** - Track all deployments
- ⚡ **Quick Deploy** - One-command deployment
- 🐳 **Docker Support** - Container-based deployment
- 🔐 **Secure** - Environment-based credentials

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- FTP/SSH access to hosting
- rsync (for SSH deployments)

### Installation

```bash
# Clone repository
git clone https://github.com/rumbleveer-spec/ai-army-deploy.git
cd ai-army-deploy

# Install dependencies
pip3 install -r requirements.txt

# Configure sites
cp sites-config.example.json sites-config.json
# Edit sites-config.json with your site details
```

## 📖 Usage

### Deploy All Sites

```bash
python3 deploy.py all
```

### Deploy Single Site

```bash
python3 deploy.py site --name mysite
```

### List Configured Sites

```bash
python3 deploy.py list
```

### Check Site Status

```bash
python3 deploy.py status
```

### Quick Deploy Script

```bash
chmod +x quick-deploy.sh
./quick-deploy.sh
```

## ⚙️ Configuration

Edit `sites-config.json`:

```json
{
  "sites": [
    {
      "name": "mysite",
      "url": "https://mysite.com",
      "method": "ftp",
      "local_path": "./sites/mysite",
      "ftp_host": "ftp.mysite.com",
      "ftp_user": "username",
      "ftp_pass": "password",
      "remote_path": "/public_html"
    }
  ]
}
```

### Deployment Methods

**FTP:**
```json
{
  "method": "ftp",
  "ftp_host": "ftp.example.com",
  "ftp_user": "username",
  "ftp_pass": "password",
  "remote_path": "/public_html"
}
```

**SSH/rsync:**
```json
{
  "method": "ssh",
  "ssh_host": "server.example.com",
  "ssh_user": "deploy",
  "remote_path": "/var/www/site"
}
```

## 📁 Project Structure

```
ai-army-deploy/
├── deploy.py              # Main deployment script
├── quick-deploy.sh        # Quick deploy wrapper
├── sites-config.json      # Site configurations
├── requirements.txt       # Python dependencies
├── sites/                 # Site source files
│   ├── site1/
│   ├── site2/
│   └── site3/
├── logs/                  # Deployment logs
└── README.md
```

## 🔧 Advanced Features

### Batch Deployment

```python
from deploy import DeployManager

manager = DeployManager()
manager.deploy_all()
```

### Custom Deployment

```python
manager = DeployManager('custom-config.json')
manager.deploy_single('mysite')
```

### Status Check

```python
for site in manager.sites:
    online = manager.check_site_status(site)
    print(f"{site['name']}: {'Online' if online else 'Offline'}")
```

## 📊 Logging

Logs are stored in `logs/` directory:

```
logs/
├── deploy-20251109.log
├── deploy-20251108.log
└── errors.log
```

## 🐳 Docker Deployment

```bash
# Build image
docker build -t ai-army-deploy .

# Run deployment
docker run -v $(pwd)/sites:/app/sites ai-army-deploy all
```

## 🌐 Hostinger Deployment

```bash
# Configure Hostinger details in sites-config.json
{
  "name": "mysite",
  "method": "ftp",
  "ftp_host": "ftp.hostinger.com",
  "ftp_user": "u123456789",
  "ftp_pass": "your_password",
  "remote_path": "/public_html"
}

# Deploy
python3 deploy.py site --name mysite
```

## 🛠️ Troubleshooting

### FTP Connection Failed

```bash
# Test FTP connection
ftp ftp.example.com
# Enter username and password
```

### SSH Permission Denied

```bash
# Setup SSH keys
ssh-keygen -t rsa
ssh-copy-id user@server.com
```

### Site Not Loading

```bash
# Check logs
tail -f logs/deploy-$(date +%Y%m%d).log

# Verify deployment
python3 deploy.py status
```

## 📄 License

MIT License - see LICENSE file

## 🤝 Contributing

Contributions welcome! Open issues or submit PRs.

## 📞 Support

- GitHub Issues: [Report Bug](https://github.com/rumbleveer-spec/ai-army-deploy/issues)
- Documentation: [Full Docs](https://github.com/rumbleveer-spec/ai-army-deploy/wiki)

---

**Built with ❤️ for Developers | Powered by AI Army HQ**
