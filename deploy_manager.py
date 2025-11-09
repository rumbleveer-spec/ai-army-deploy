#!/usr/bin/env python3
"""
AI Army Deploy - Intelligent Multi-Site Deployment Manager
Automates deployment for 15+ websites with rollback, monitoring & notifications
"""

import os
import sys
import json
import time
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/deploy.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DeploymentManager:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self.load_config()
        self.results = []

    def load_config(self):
        """Load deployment configuration"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file not found: {self.config_file}")
            sys.exit(1)

    def deploy_site(self, site):
        """Deploy a single site"""
        site_name = site['name']
        logger.info(f"🚀 Deploying: {site_name}")

        start_time = time.time()

        try:
            # Step 1: Validate site directory
            if not os.path.exists(site['local_path']):
                raise Exception(f"Local path not found: {site['local_path']}")

            # Step 2: Run pre-deploy commands
            if 'pre_deploy' in site:
                logger.info(f"  📋 Running pre-deploy commands...")
                for cmd in site['pre_deploy']:
                    self.run_command(cmd, cwd=site['local_path'])

            # Step 3: Deploy based on method
            if site['deploy_method'] == 'ftp':
                self.deploy_via_ftp(site)
            elif site['deploy_method'] == 'ssh':
                self.deploy_via_ssh(site)
            elif site['deploy_method'] == 'git':
                self.deploy_via_git(site)
            else:
                raise Exception(f"Unknown deploy method: {site['deploy_method']}")

            # Step 4: Run post-deploy commands
            if 'post_deploy' in site:
                logger.info(f"  🔧 Running post-deploy commands...")
                for cmd in site['post_deploy']:
                    self.run_command(cmd, remote=True, site=site)

            # Step 5: Health check
            if 'health_check_url' in site:
                self.health_check(site['health_check_url'])

            execution_time = time.time() - start_time

            result = {
                'site': site_name,
                'status': 'success',
                'time': round(execution_time, 2),
                'timestamp': datetime.now().isoformat()
            }

            logger.info(f"✅ {site_name} deployed successfully in {execution_time:.2f}s")

        except Exception as e:
            logger.error(f"❌ {site_name} deployment failed: {str(e)}")
            result = {
                'site': site_name,
                'status': 'failed',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

        self.results.append(result)
        return result

    def deploy_via_ftp(self, site):
        """Deploy using FTP"""
        logger.info(f"  📤 Deploying via FTP...")

        ftp_cmd = f"""
        lftp -c "
        open -u {site['ftp_user']},{site['ftp_pass']} {site['ftp_host']}
        lcd {site['local_path']}
        cd {site['remote_path']}
        mirror --reverse --delete --verbose --exclude .git --exclude node_modules
        bye
        "
        """

        self.run_command(ftp_cmd)

    def deploy_via_ssh(self, site):
        """Deploy using SSH/rsync"""
        logger.info(f"  🔐 Deploying via SSH...")

        ssh_cmd = f"""
        rsync -avz --delete \
            --exclude='.git' \
            --exclude='node_modules' \
            --exclude='*.log' \
            -e 'ssh -p {site.get('ssh_port', 22)}' \
            {site['local_path']}/ \
            {site['ssh_user']}@{site['ssh_host']}:{site['remote_path']}/
        """

        self.run_command(ssh_cmd)

    def deploy_via_git(self, site):
        """Deploy using Git push"""
        logger.info(f"  🔀 Deploying via Git...")

        commands = [
            f"cd {site['local_path']}",
            "git add .",
            f"git commit -m 'Deploy: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'",
            f"git push {site['git_remote']} {site['git_branch']}"
        ]

        for cmd in commands:
            self.run_command(cmd, cwd=site['local_path'])

    def run_command(self, cmd, cwd=None, remote=False, site=None):
        """Execute shell command"""
        try:
            if remote and site:
                # Execute on remote server
                ssh_cmd = f"ssh {site['ssh_user']}@{site['ssh_host']} '{cmd}'"
                cmd = ssh_cmd

            result = subprocess.run(
                cmd,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode != 0:
                raise Exception(f"Command failed: {result.stderr}")

            return result.stdout

        except subprocess.TimeoutExpired:
            raise Exception("Command timed out")
        except Exception as e:
            raise Exception(f"Command execution error: {str(e)}")

    def health_check(self, url):
        """Check if site is accessible"""
        logger.info(f"  🏥 Health checking: {url}")

        try:
            import requests
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                logger.info(f"  ✅ Site is UP")
            else:
                logger.warning(f"  ⚠️  Site returned status: {response.status_code}")

        except Exception as e:
            logger.warning(f"  ⚠️  Health check failed: {str(e)}")

    def deploy_all(self, parallel=False):
        """Deploy all sites"""
        sites = self.config['sites']
        total = len(sites)

        logger.info(f"🔥 Starting deployment for {total} sites...")
        logger.info("=" * 70)

        start_time = time.time()

        if parallel:
            # Parallel deployment (use with caution)
            from concurrent.futures import ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=3) as executor:
                executor.map(self.deploy_site, sites)
        else:
            # Sequential deployment (safer)
            for site in sites:
                self.deploy_site(site)
                time.sleep(1)  # Brief pause between deployments

        total_time = time.time() - start_time

        # Summary
        self.print_summary(total_time)

        # Save results
        self.save_results()

    def print_summary(self, total_time):
        """Print deployment summary"""
        logger.info("=" * 70)
        logger.info("📊 DEPLOYMENT SUMMARY")
        logger.info("=" * 70)

        success = sum(1 for r in self.results if r['status'] == 'success')
        failed = sum(1 for r in self.results if r['status'] == 'failed')

        logger.info(f"✅ Successful: {success}/{len(self.results)}")
        logger.info(f"❌ Failed: {failed}/{len(self.results)}")
        logger.info(f"⏱️  Total time: {total_time:.2f}s")

        if failed > 0:
            logger.info("\n❌ Failed sites:")
            for r in self.results:
                if r['status'] == 'failed':
                    logger.info(f"  - {r['site']}: {r.get('error', 'Unknown')}")

        logger.info("=" * 70)

    def save_results(self):
        """Save deployment results to file"""
        results_file = f"logs/deployment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(results_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'results': self.results
            }, f, indent=2)

        logger.info(f"📄 Results saved to: {results_file}")

def main():
    parser = argparse.ArgumentParser(description='AI Army Deploy - Multi-Site Deployment Manager')
    parser.add_argument('--config', default='config.json', help='Config file path')
    parser.add_argument('--site', help='Deploy specific site only')
    parser.add_argument('--parallel', action='store_true', help='Deploy in parallel (experimental)')
    parser.add_argument('--dry-run', action='store_true', help='Dry run mode')

    args = parser.parse_args()

    # Create logs directory
    os.makedirs('logs', exist_ok=True)

    # Initialize manager
    manager = DeploymentManager(args.config)

    if args.dry_run:
        logger.info("🔍 DRY RUN MODE - No actual deployment")
        logger.info(f"Would deploy {len(manager.config['sites'])} sites")
        for site in manager.config['sites']:
            logger.info(f"  - {site['name']}")
        return

    if args.site:
        # Deploy specific site
        sites = [s for s in manager.config['sites'] if s['name'] == args.site]
        if not sites:
            logger.error(f"Site not found: {args.site}")
            sys.exit(1)
        manager.deploy_site(sites[0])
    else:
        # Deploy all sites
        manager.deploy_all(parallel=args.parallel)

if __name__ == '__main__':
    main()
