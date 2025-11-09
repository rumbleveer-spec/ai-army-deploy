#!/usr/bin/env python3
"""
Rollback Manager - Revert to previous deployment
"""

import os
import sys
import json
import shutil
from datetime import datetime

class RollbackManager:
    def __init__(self):
        self.backup_dir = 'backups'
        os.makedirs(self.backup_dir, exist_ok=True)

    def create_backup(self, site_name, site_path):
        """Create backup before deployment"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(
            self.backup_dir,
            f"{site_name}_{timestamp}"
        )

        print(f"💾 Creating backup: {backup_path}")
        shutil.copytree(site_path, backup_path, symlinks=True)

        # Keep only last 5 backups
        self.cleanup_old_backups(site_name)

        return backup_path

    def list_backups(self, site_name):
        """List available backups for a site"""
        backups = []

        for item in os.listdir(self.backup_dir):
            if item.startswith(site_name):
                path = os.path.join(self.backup_dir, item)
                backups.append({
                    'name': item,
                    'path': path,
                    'timestamp': item.split('_', 1)[1] if '_' in item else 'unknown'
                })

        backups.sort(key=lambda x: x['timestamp'], reverse=True)
        return backups

    def rollback(self, site_name, site_path, backup_name=None):
        """Rollback to a backup"""
        backups = self.list_backups(site_name)

        if not backups:
            print(f"❌ No backups found for {site_name}")
            return False

        # Use latest backup if not specified
        if not backup_name:
            backup = backups[0]
        else:
            backup = next((b for b in backups if b['name'] == backup_name), None)
            if not backup:
                print(f"❌ Backup not found: {backup_name}")
                return False

        print(f"🔄 Rolling back to: {backup['name']}")

        # Remove current deployment
        if os.path.exists(site_path):
            shutil.rmtree(site_path)

        # Restore from backup
        shutil.copytree(backup['path'], site_path, symlinks=True)

        print(f"✅ Rollback complete!")
        return True

    def cleanup_old_backups(self, site_name, keep=5):
        """Keep only last N backups"""
        backups = self.list_backups(site_name)

        if len(backups) > keep:
            for backup in backups[keep:]:
                print(f"🗑️  Removing old backup: {backup['name']}")
                shutil.rmtree(backup['path'])

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python rollback.py <site_name> <site_path> [backup_name]")
        sys.exit(1)

    site_name = sys.argv[1]
    site_path = sys.argv[2]
    backup_name = sys.argv[3] if len(sys.argv) > 3 else None

    manager = RollbackManager()
    manager.rollback(site_name, site_path, backup_name)
