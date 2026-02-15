#!/usr/bin/env python3
"""
Autodarts Installer
Main installation and management script for Autodarts Desktop
"""

import os
import sys
import subprocess
import logging
import re
from pathlib import Path
from typing import Optional, Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from config.autodarts_config import AutodartsConfig
except ImportError:
    # Fallback if running standalone
    from dataclasses import dataclass
    
    @dataclass
    class AutodartsConfig:
        """Configuration for autodarts installation"""
        service_name: str = "autodarts"
        installer_url: str = "get.autodarts.io"
        uvc_hack_url: str = "get.autodarts.io/uvc"
        user: str = "cdo-vertex"
        enable_autostart: bool = True
        log_level: str = "INFO"


class AutodartsInstaller:
    """Manages Autodarts Desktop installation and updates"""
    
    def __init__(self, config: Optional[AutodartsConfig] = None):
        self.config = config or AutodartsConfig()
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Configure logging for the installer"""
        log_level = getattr(logging, self.config.log_level.upper(), logging.INFO)
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def check_dependencies(self) -> bool:
        """Check if required system dependencies are installed"""
        dependencies = ['curl', 'systemctl']
        missing = []
        
        for dep in dependencies:
            if not self._command_exists(dep):
                missing.append(dep)
        
        if missing:
            self.logger.error(f"Missing dependencies: {', '.join(missing)}")
            if 'curl' in missing:
                self.logger.info("Install with: sudo apt install curl -y")
            return False
        
        return True
    
    def _command_exists(self, command: str) -> bool:
        """Check if a command exists in PATH"""
        return subprocess.call(
            ['which', command],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        ) == 0
    
    def _run_command(self, cmd, cwd=None, check=True, shell=False, input_text=None):
        """Run a shell command and return the result"""
        self.logger.info(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
        try:
            if shell:
                cmd = ' '.join(cmd) if isinstance(cmd, list) else cmd
            
            result = subprocess.run(
                cmd,
                cwd=cwd,
                check=check,
                capture_output=True,
                text=True,
                shell=shell,
                input=input_text
            )
            if result.stdout:
                self.logger.debug(result.stdout)
            return result
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed: {e}")
            if e.stderr:
                self.logger.error(f"STDERR: {e.stderr}")
            raise
    
    def is_installed(self) -> bool:
        """Check if autodarts service exists"""
        try:
            result = self._run_command(
                ['systemctl', 'list-unit-files', self.config.service_name + '.service'],
                check=False
            )
            return self.config.service_name in result.stdout
        except Exception as e:
            self.logger.warning(f"Could not check if installed: {e}")
            return False
    
    def get_installed_version(self) -> Optional[str]:
        """Get the currently installed version of autodarts"""
        try:
            result = self._run_command(
                ['autodarts', '--version'],
                check=False
            )
            if result.returncode == 0:
                match = re.search(r'(\d+\.\d+\.\d+)', result.stdout)
                if match:
                    return match.group(1)
            
            result = self._run_command(
                ['systemctl', 'show', self.config.service_name, '--property=Description'],
                check=False
            )
            if result.returncode == 0:
                match = re.search(r'(\d+\.\d+\.\d+)', result.stdout)
                if match:
                    return match.group(1)
                    
            return None
        except Exception as e:
            self.logger.warning(f"Could not get installed version: {e}")
            return None
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get the status of the autodarts service"""
        try:
            result = self._run_command(
                ['systemctl', 'is-active', self.config.service_name],
                check=False
            )
            is_active = result.stdout.strip() == 'active'
            
            result = self._run_command(
                ['systemctl', 'is-enabled', self.config.service_name],
                check=False
            )
            is_enabled = result.stdout.strip() == 'enabled'
            
            return {
                'active': is_active,
                'enabled': is_enabled,
                'status': 'running' if is_active else 'stopped'
            }
        except Exception as e:
            self.logger.warning(f"Could not get service status: {e}")
            return {'active': False, 'enabled': False, 'status': 'unknown'}
    
    def stop_service(self) -> bool:
        """Stop the autodarts service if running"""
        try:
            self.logger.info(f"Stopping {self.config.service_name} service")
            self._run_command(
                ['sudo', 'systemctl', 'stop', self.config.service_name],
                check=False
            )
            return True
        except Exception as e:
            self.logger.warning(f"Could not stop service: {e}")
            return False
    
    def start_service(self) -> bool:
        """Start the autodarts service"""
        try:
            self.logger.info(f"Starting {self.config.service_name} service")
            self._run_command(
                ['sudo', 'systemctl', 'start', self.config.service_name]
            )
            return True
        except Exception as e:
            self.logger.error(f"Could not start service: {e}")
            return False
    
    def restart_service(self) -> bool:
        """Restart the autodarts service"""
        try:
            self.logger.info(f"Restarting {self.config.service_name} service")
            self._run_command(
                ['sudo', 'systemctl', 'restart', self.config.service_name]
            )
            return True
        except Exception as e:
            self.logger.error(f"Could not restart service: {e}")
            return False
    
    def enable_service(self) -> bool:
        """Enable autodarts service to start on boot"""
        try:
            self.logger.info(f"Enabling {self.config.service_name} service")
            self._run_command(
                ['sudo', 'systemctl', 'enable', self.config.service_name]
            )
            return True
        except Exception as e:
            self.logger.error(f"Could not enable service: {e}")
            return False
    
    def disable_service(self) -> bool:
        """Disable autodarts service from starting on boot"""
        try:
            self.logger.info(f"Disabling {self.config.service_name} service")
            self._run_command(
                ['sudo', 'systemctl', 'disable', self.config.service_name]
            )
            return True
        except Exception as e:
            self.logger.error(f"Could not disable service: {e}")
            return False
    
    def view_logs(self, follow: bool = False, lines: int = 50) -> bool:
        """View service logs"""
        try:
            cmd = ['journalctl', '-u', self.config.service_name, '-n', str(lines)]
            if follow:
                cmd.append('-f')
            
            self.logger.info(f"Viewing logs for {self.config.service_name}")
            if follow:
                self.logger.info("Press Ctrl+C to stop following logs")
            
            subprocess.run(cmd)
            return True
        except Exception as e:
            self.logger.error(f"Could not view logs: {e}")
            return False
    
    def install(self, version: Optional[str] = None, 
                enable_autostart: Optional[bool] = None) -> bool:
        """Install autodarts using the official installer"""
        self.logger.info("Starting autodarts installation")
        
        if not self.check_dependencies():
            return False
        
        if self.is_installed():
            self.logger.warning("Autodarts is already installed. Use update() to upgrade.")
            return False
        
        installer_cmd = f"bash <(curl -sL {self.config.installer_url})"
        
        autostart = enable_autostart if enable_autostart is not None else self.config.enable_autostart
        if not autostart:
            installer_cmd += " -n"
        
        if version:
            installer_cmd += f" {version}"
        
        try:
            self.logger.info(f"Running installer: {installer_cmd}")
            result = self._run_command(installer_cmd, shell=True, check=True)
            
            self.logger.info("Installation completed successfully")
            
            if not self.is_installed():
                self.logger.error("Installation completed but service not found")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Installation failed: {e}")
            return False
    
    def update(self, version: Optional[str] = None) -> bool:
        """Update autodarts to the latest or specific version"""
        self.logger.info("Starting autodarts update")
        
        if not self.is_installed():
            self.logger.error("Autodarts is not installed. Use install() instead.")
            return False
        
        current_version = self.get_installed_version()
        if current_version:
            self.logger.info(f"Current version: {current_version}")
        
        self.stop_service()
        
        service_status = self.get_service_status()
        was_enabled = service_status.get('enabled', False)
        
        installer_cmd = f"bash <(curl -sL {self.config.installer_url})"
        
        if not was_enabled:
            installer_cmd += " -n"
        
        if version:
            installer_cmd += f" {version}"
            self.logger.info(f"Updating to version: {version}")
        else:
            self.logger.info("Updating to latest version")
        
        try:
            self.logger.info(f"Running installer: {installer_cmd}")
            result = self._run_command(installer_cmd, shell=True, check=True)
            
            if service_status.get('active', False):
                self.start_service()
            
            new_version = self.get_installed_version()
            if new_version:
                self.logger.info(f"Updated to version: {new_version}")
            
            self.logger.info("Update completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Update failed: {e}")
            self.start_service()
            return False
    
    def install_uvc_hack(self) -> bool:
        """Install the UVC hack for USB camera bandwidth issues"""
        self.logger.info("Installing UVC hack")
        
        if not self.check_dependencies():
            return False
        
        self.logger.warning("The UVC hack will not work on systems with UEFI Secure Boot enabled")
        self.logger.info("Make sure at least one camera is connected")
        
        try:
            cmd = f"bash <(curl -sL {self.config.uvc_hack_url})"
            self.logger.info(f"Running UVC hack installer: {cmd}")
            
            result = self._run_command(cmd, shell=True, check=True)
            
            self.logger.info("UVC hack installed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"UVC hack installation failed: {e}")
            return False
    
    def uninstall_uvc_hack(self) -> bool:
        """Uninstall the UVC hack"""
        self.logger.info("Uninstalling UVC hack")
        
        try:
            cmd = f"bash <(curl -sL {self.config.uvc_hack_url}) --uninstall"
            self.logger.info(f"Running UVC hack uninstaller: {cmd}")
            
            result = self._run_command(cmd, shell=True, check=True)
            
            self.logger.info("UVC hack uninstalled successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"UVC hack uninstall failed: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get current installation status"""
        installed = self.is_installed()
        
        status = {
            'installed': installed,
            'version': self.get_installed_version() if installed else None,
        }
        
        if installed:
            service_status = self.get_service_status()
            status.update(service_status)
        
        return status


def main():
    """Main entry point for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Autodarts Desktop Installer/Updater',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'action',
        choices=['install', 'update', 'status', 'start', 'stop', 'restart', 
                'enable', 'disable', 'logs', 'uvc-install', 'uvc-uninstall'],
        help='Action to perform'
    )
    parser.add_argument('--version', type=str, help='Specific version to install')
    parser.add_argument('--no-autostart', action='store_true', help='Do not enable autostart on boot')
    parser.add_argument('--follow', action='store_true', help='Follow logs in real-time')
    parser.add_argument('--lines', type=int, default=50, help='Number of log lines')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    config = AutodartsConfig(enable_autostart=not args.no_autostart)
    installer = AutodartsInstaller(config)
    
    if args.action == 'install':
        success = installer.install(version=args.version, enable_autostart=not args.no_autostart)
        sys.exit(0 if success else 1)
    elif args.action == 'update':
        success = installer.update(version=args.version)
        sys.exit(0 if success else 1)
    elif args.action == 'status':
        status = installer.get_status()
        print("\nAutodarts Status:")
        print("-" * 50)
        for key, value in status.items():
            print(f"{key:20s}: {value}")
        sys.exit(0)
    elif args.action == 'start':
        sys.exit(0 if installer.start_service() else 1)
    elif args.action == 'stop':
        sys.exit(0 if installer.stop_service() else 1)
    elif args.action == 'restart':
        sys.exit(0 if installer.restart_service() else 1)
    elif args.action == 'enable':
        sys.exit(0 if installer.enable_service() else 1)
    elif args.action == 'disable':
        sys.exit(0 if installer.disable_service() else 1)
    elif args.action == 'logs':
        installer.view_logs(follow=args.follow, lines=args.lines)
        sys.exit(0)
    elif args.action == 'uvc-install':
        sys.exit(0 if installer.install_uvc_hack() else 1)
    elif args.action == 'uvc-uninstall':
        sys.exit(0 if installer.uninstall_uvc_hack() else 1)


if __name__ == '__main__':
    main()
