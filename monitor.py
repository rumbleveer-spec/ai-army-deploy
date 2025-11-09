#!/usr/bin/env python3
"""
Site Monitoring - Check health of all deployed sites
"""

import json
import requests
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

class SiteMonitor:
    def __init__(self, config_file='config.json'):
        with open(config_file, 'r') as f:
            self.config = json.load(f)

    def check_site(self, site):
        """Check if site is accessible"""
        if 'health_check_url' not in site:
            return None

        try:
            start = time.time()
            response = requests.get(site['health_check_url'], timeout=10)
            response_time = (time.time() - start) * 1000  # ms

            return {
                'site': site['name'],
                'url': site['health_check_url'],
                'status': 'UP' if response.status_code == 200 else 'DOWN',
                'status_code': response.status_code,
                'response_time': round(response_time, 2),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'site': site['name'],
                'url': site['health_check_url'],
                'status': 'ERROR',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def check_all(self):
        """Check all sites"""
        print("🔍 Monitoring Sites...")
        print("=" * 70)

        results = []

        for site in self.config['sites']:
            result = self.check_site(site)
            if result:
                results.append(result)

                status_icon = '✅' if result['status'] == 'UP' else '❌'
                print(f"{status_icon} {result['site']}: {result['status']}")
                if result['status'] == 'UP':
                    print(f"   Response time: {result['response_time']}ms")

        print("=" * 70)

        # Alert if any site is down
        down_sites = [r for r in results if r['status'] != 'UP']
        if down_sites:
            self.send_alert(down_sites)

        return results

    def send_alert(self, down_sites):
        """Send alert for down sites"""
        print(f"⚠️  ALERT: {len(down_sites)} site(s) are down!")
        # Implement Slack/Email notification here

if __name__ == '__main__':
    monitor = SiteMonitor()
    monitor.check_all()
