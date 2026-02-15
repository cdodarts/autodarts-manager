#!/usr/bin/env python3
"""
Example usage of the Autodarts Installer module

This demonstrates various ways to use the installer in your application.
"""

from autodarts_installer import AutodartsInstaller, AutodartsConfig
from pathlib import Path
import sys


def example_basic_install():
    """Example: Basic installation with default settings"""
    print("Example 1: Basic Installation")
    print("-" * 50)
    
    installer = AutodartsInstaller()
    
    # Check if already installed
    if installer.is_installed():
        print("Autodarts is already installed")
        return
    
    # Perform installation
    if installer.install():
        print("✓ Installation successful!")
    else:
        print("✗ Installation failed")
        sys.exit(1)


def example_custom_install():
    """Example: Installation with custom configuration"""
    print("\nExample 2: Custom Installation")
    print("-" * 50)
    
    # Create custom configuration
    config = AutodartsConfig(
        install_dir=Path("/home/pi/custom/autodarts"),
        venv_dir=Path("/home/pi/custom/autodarts/venv"),
        user="pi"
    )
    
    installer = AutodartsInstaller(config)
    
    if installer.install():
        print(f"✓ Installed to custom location: {config.install_dir}")
    else:
        print("✗ Installation failed")


def example_update():
    """Example: Update existing installation"""
    print("\nExample 3: Update Existing Installation")
    print("-" * 50)
    
    installer = AutodartsInstaller()
    
    # Check if installed
    if not installer.is_installed():
        print("Autodarts is not installed. Cannot update.")
        return
    
    # Get version info
    current = installer.get_current_version()
    latest = installer.get_latest_version()
    
    print(f"Current version: {current[:8] if current else 'Unknown'}")
    print(f"Latest version:  {latest[:8] if latest else 'Unknown'}")
    
    if current == latest:
        print("Already at latest version!")
        return
    
    # Perform update
    print("\nUpdating...")
    if installer.update():
        print("✓ Update successful!")
    else:
        print("✗ Update failed")


def example_check_status():
    """Example: Check installation status"""
    print("\nExample 4: Check Status")
    print("-" * 50)
    
    installer = AutodartsInstaller()
    status = installer.get_status()
    
    print(f"Installed:        {status['installed']}")
    print(f"Install Dir:      {status['install_dir']}")
    print(f"Current Version:  {status['current_version'][:8] if status['current_version'] else 'N/A'}")
    print(f"Latest Version:   {status['latest_version'][:8] if status['latest_version'] else 'N/A'}")
    print(f"Venv Exists:      {status['venv_exists']}")
    
    # Determine if update is needed
    if status['installed'] and status['current_version'] != status['latest_version']:
        print("\n⚠ Update available!")


def example_conditional_install_or_update():
    """Example: Automatically install or update as needed"""
    print("\nExample 5: Conditional Install/Update")
    print("-" * 50)
    
    installer = AutodartsInstaller()
    
    if not installer.is_installed():
        print("Not installed. Installing...")
        success = installer.install()
    else:
        current = installer.get_current_version()
        latest = installer.get_latest_version()
        
        if current != latest:
            print("Update available. Updating...")
            success = installer.update()
        else:
            print("Already at latest version")
            success = True
    
    if success:
        print("✓ System is up to date")
    else:
        print("✗ Operation failed")


def example_with_error_handling():
    """Example: Robust error handling"""
    print("\nExample 6: Error Handling")
    print("-" * 50)
    
    installer = AutodartsInstaller()
    
    try:
        # Check dependencies first
        if not installer.check_dependencies():
            print("✗ Missing required dependencies")
            print("Run: sudo apt-get install git python3 python3-venv python3-pip")
            return
        
        # Check status
        status = installer.get_status()
        
        if not status['installed']:
            print("Installing autodarts...")
            if not installer.install():
                raise RuntimeError("Installation failed")
        else:
            print("Checking for updates...")
            if status['current_version'] != status['latest_version']:
                if not installer.update():
                    raise RuntimeError("Update failed")
            else:
                print("Already up to date")
        
        print("✓ Operation completed successfully")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


def example_integration_with_setup_script():
    """Example: Integration into a larger setup script"""
    print("\nExample 7: Integration Example")
    print("-" * 50)
    
    def setup_system():
        """Main setup function"""
        steps = [
            ("Check system dependencies", check_system),
            ("Install/Update autodarts", install_autodarts),
            ("Verify installation", verify_installation),
        ]
        
        for step_name, step_func in steps:
            print(f"\n[{step_name}]")
            if not step_func():
                print(f"✗ Failed: {step_name}")
                return False
            print(f"✓ Success: {step_name}")
        
        return True
    
    def check_system():
        """Check system is ready"""
        installer = AutodartsInstaller()
        return installer.check_dependencies()
    
    def install_autodarts():
        """Install or update autodarts"""
        installer = AutodartsInstaller()
        
        if installer.is_installed():
            return installer.update()
        else:
            return installer.install()
    
    def verify_installation():
        """Verify the installation worked"""
        installer = AutodartsInstaller()
        status = installer.get_status()
        return status['installed'] and status['venv_exists']
    
    # Run the setup
    if setup_system():
        print("\n" + "=" * 50)
        print("System setup complete!")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("System setup failed!")
        print("=" * 50)
        sys.exit(1)


def main():
    """Run all examples"""
    print("=" * 50)
    print("AUTODARTS INSTALLER - USAGE EXAMPLES")
    print("=" * 50)
    
    # Note: In real usage, you'd run only the example you need
    # These are all here for demonstration
    
    # Uncomment the example you want to run:
    
    # example_basic_install()
    # example_custom_install()
    # example_update()
    example_check_status()
    # example_conditional_install_or_update()
    # example_with_error_handling()
    # example_integration_with_setup_script()
    
    print("\n" + "=" * 50)
    print("Examples complete")
    print("=" * 50)


if __name__ == '__main__':
    main()
