#!/usr/bin/env python3
"""
Autodarts Setup Script
Complete setup workflow for autodarts installation
"""

import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.autodarts_installer import AutodartsInstaller

try:
    from config.autodarts_config import AutodartsConfig
except ImportError:
    from dataclasses import dataclass
    
    @dataclass
    class AutodartsConfig:
        service_name: str = "autodarts"
        installer_url: str = "get.autodarts.io"
        uvc_hack_url: str = "get.autodarts.io/uvc"
        user: str = "cdo-vertex"
        enable_autostart: bool = True
        log_level: str = "INFO"


def setup_autodarts(config=None):
    """Complete autodarts setup workflow"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("AUTODARTS SETUP")
    logger.info("=" * 60)
    
    installer = AutodartsInstaller(config)
    
    logger.info("\n[1/4] Checking system dependencies...")
    if not installer.check_dependencies():
        logger.error("Missing dependencies!")
        logger.info("Install curl with: sudo apt install curl -y")
        return False
    logger.info("✓ Dependencies OK")
    
    logger.info("\n[2/4] Installing/Updating Autodarts...")
    if not installer.is_installed():
        logger.info("Installing Autodarts...")
        if not installer.install():
            logger.error("Installation failed")
            return False
        logger.info("✓ Autodarts installed")
    else:
        current = installer.get_installed_version()
        logger.info(f"Current version: {current or 'unknown'}")
        logger.info("Updating Autodarts...")
        if not installer.update():
            logger.error("Update failed")
            return False
        new_version = installer.get_installed_version()
        logger.info(f"✓ Updated to version: {new_version or 'unknown'}")
    
    logger.info("\n[3/4] Configuring service...")
    status = installer.get_service_status()
    
    if not status.get('enabled', False):
        installer.enable_service()
        logger.info("✓ Autostart enabled")
    else:
        logger.info("✓ Autostart already enabled")
    
    logger.info("\n[4/4] Starting service...")
    if not status.get('active', False):
        if installer.start_service():
            logger.info("✓ Service started")
        else:
            logger.warning("Could not start service")
    else:
        logger.info("✓ Service already running")
    
    logger.info("\n" + "=" * 60)
    logger.info("SETUP COMPLETE")
    logger.info("=" * 60)
    
    final_status = installer.get_status()
    logger.info(f"\nAutodarts Status:")
    logger.info(f"  Version:  {final_status.get('version', 'unknown')}")
    logger.info(f"  Running:  {final_status.get('active', False)}")
    logger.info(f"  Enabled:  {final_status.get('enabled', False)}")
    
    return True


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Autodarts Setup Script')
    parser.add_argument('--no-autostart', action='store_true', help='Do not enable autostart on boot')
    parser.add_argument('--version', type=str, help='Install specific version')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    config = AutodartsConfig(enable_autostart=not args.no_autostart)
    
    success = setup_autodarts(config)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
