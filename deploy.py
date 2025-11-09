#!/usr/bin/env python3
"""
AI Army Deploy - Multi-site Deployment Automation
Deploys multiple websites to Hostinger or any hosting platform
"""

import os
import subprocess
import sys
import time
import json
from datetime import datetime
from pathlib import Path
import ftplib
import paramiko

# Configuration
CONFIG_FILE = 'sites-config.json'
LOG_DIR = 'logs'

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

class DeployManager:
    def __init__(self, config_file=CONFIG_FILE):
        self.config_file = config_file
        self.sites = self.load_config()
        self.log_dir = Path(LOG_DIR)
        self.log_dir.mkdir(exist_ok=True)

    def load_config(self):
        """Load sites configuration"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"{Colors.RED}❌ Config file not found: {self.config_file}{Colors.END}")
            sys.exit(1)

    def log(self, message, level='INFO'):
        """Write to log file"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_file = self.log_dir / f"deploy-{datetime.now().strftime('%Y%m%d')}.log"

        with open(log_file, 'a') as f:
            f.write(f"[{timestamp}] {level}: {message}\n")

    def print_banner(self):
        """Print deployment banner"""
        print(f"{Colors.BLUE}{Colors.BOLD}")
        print("="*70)
        print("🚀 AI ARMY DEPLOY - Multi-Site Deployment System")
        print("="*70)
        print(f"{Colors.END}")

    def deploy_via_ftp(self, site):
        """Deploy site via FTP"""
        try:
            print(f"{Colors.YELLOW}📤 Deploying {site['name']} via FTP...{Colors.END}")

            ftp = ftplib.FTP(site['ftp_host'])
            ftp.login(site['ftp_user'], site['ftp_pass'])
            ftp.cwd(site['remote_path'])

            # Upload files
            local_path = Path(site['local_path'])
            for file_path in local_path.rglob('*'):
                if file_path.is_file():
                    relative_path = file_path.relative_to(local_path)

                    # Create directories
                    remote_dir = str(relative_path.parent).replace('\\', '/')
                    if remote_dir != '.':
                        try:
                            ftp.mkd(remote_dir)
                        except:
                            pass

                    # Upload file
                    remote_file = str(relative_path).replace('\\', '/')
                    with open(file_path, 'rb') as f:
                        ftp.storbinary(f'STOR {remote_file}', f)

                    print(f"  ✓ Uploaded: {remote_file}")

            ftp.quit()
            print(f"{Colors.GREEN}✅ {site['name']} deployed successfully!{Colors.END}")
            self.log(f"Deployed {site['name']} successfully", 'SUCCESS')
            return True

        except Exception as e:
            print(f"{Colors.RED}❌ Failed to deploy {site['name']}: {str(e)}{Colors.END}")
            self.log(f"Failed to deploy {site['name']}: {str(e)}", 'ERROR')
            return False

    def deploy_via_ssh(self, site):
        """Deploy site via SSH/rsync"""
        try:
            print(f"{Colors.YELLOW}📤 Deploying {site['name']} via SSH...{Colors.END}")

            cmd = [
                'rsync', '-avz',
                '--exclude', '.git',
                '--exclude', 'node_modules',
                '--exclude', '__pycache__',
                site['local_path'] + '/',
                f"{site['ssh_user']}@{site['ssh_host']}:{site['remote_path']}"
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"{Colors.GREEN}✅ {site['name']} deployed successfully!{Colors.END}")
                self.log(f"Deployed {site['name']} successfully", 'SUCCESS')
                return True
            else:
                print(f"{Colors.RED}❌ Failed: {result.stderr}{Colors.END}")
                self.log(f"Failed to deploy {site['name']}: {result.stderr}", 'ERROR')
                return False

        except Exception as e:
            print(f"{Colors.RED}❌ Error: {str(e)}{Colors.END}")
            self.log(f"Error deploying {site['name']}: {str(e)}", 'ERROR')
            return False

    def check_site_status(self, site):
        """Check if site is online"""
        try:
            import requests
            response = requests.get(site['url'], timeout=5)
            return response.status_code == 200
        except:
            return False

    def deploy_all(self):
        """Deploy all sites"""
        self.print_banner()

        total = len(self.sites)
        successful = 0
        failed = 0

        print(f"\n{Colors.BOLD}Deploying {total} websites...{Colors.END}\n")

        for i, site in enumerate(self.sites, 1):
            print(f"\n[{i}/{total}] {Colors.BOLD}{site['name']}{Colors.END}")
            print(f"URL: {site['url']}")

            # Choose deployment method
            if site.get('method') == 'ssh':
                success = self.deploy_via_ssh(site)
            else:
                success = self.deploy_via_ftp(site)

            if success:
                successful += 1

                # Check status
                time.sleep(2)
                if self.check_site_status(site):
                    print(f"{Colors.GREEN}🌐 Site is ONLINE{Colors.END}")
                else:
                    print(f"{Colors.YELLOW}⚠️  Site check failed (may take time to load){Colors.END}")
            else:
                failed += 1

            print("-" * 70)

        # Summary
        print(f"\n{Colors.BOLD}DEPLOYMENT SUMMARY:{Colors.END}")
        print("="*70)
        print(f"{Colors.GREEN}✅ Successful: {successful}/{total}{Colors.END}")
        if failed > 0:
            print(f"{Colors.RED}❌ Failed: {failed}/{total}{Colors.END}")
        print("="*70)

        self.log(f"Deployment completed: {successful} success, {failed} failed", 'INFO')

    def deploy_single(self, site_name):
        """Deploy single site"""
        self.print_banner()

        site = next((s for s in self.sites if s['name'] == site_name), None)

        if not site:
            print(f"{Colors.RED}❌ Site '{site_name}' not found in config{Colors.END}")
            return

        print(f"\n{Colors.BOLD}Deploying: {site['name']}{Colors.END}\n")

        if site.get('method') == 'ssh':
            self.deploy_via_ssh(site)
        else:
            self.deploy_via_ftp(site)

    def list_sites(self):
        """List all configured sites"""
        self.print_banner()
        print(f"\n{Colors.BOLD}Configured Sites:{Colors.END}\n")

        for i, site in enumerate(self.sites, 1):
            print(f"{i}. {Colors.BOLD}{site['name']}{Colors.END}")
            print(f"   URL: {site['url']}")
            print(f"   Method: {site.get('method', 'ftp').upper()}")
            print(f"   Local: {site['local_path']}")
            print()

def main():
    import argparse

    parser = argparse.ArgumentParser(description='AI Army Deploy - Multi-site deployment')
    parser.add_argument('action', choices=['all', 'site', 'list', 'status'], 
                       help='Action to perform')
    parser.add_argument('--name', help='Site name (for site action)')

    args = parser.parse_args()

    manager = DeployManager()

    if args.action == 'all':
        manager.deploy_all()
    elif args.action == 'site':
        if not args.name:
            print(f"{Colors.RED}❌ Please provide site name with --name{Colors.END}")
            sys.exit(1)
        manager.deploy_single(args.name)
    elif args.action == 'list':
        manager.list_sites()
    elif args.action == 'status':
        manager.print_banner()
        print(f"\n{Colors.BOLD}Checking site status...{Colors.END}\n")
        for site in manager.sites:
            status = "🟢 ONLINE" if manager.check_site_status(site) else "🔴 OFFLINE"
            print(f"{site['name']:30} {status:10} {site['url']}")

if __name__ == '__main__':
    main()
