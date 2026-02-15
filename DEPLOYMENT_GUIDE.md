# Autodarts Manager - Deployment Guide

## 📁 Directory Structure

```
/opt/autodarts-manager/
├── config/                      # Configuration
│   ├── __init__.py
│   └── autodarts_config.py     # Main configuration class
├── scripts/                     # Executable scripts
│   ├── __init__.py
│   ├── autodarts_installer.py  # Main installer (CLI + API)
│   └── setup.py                 # Complete setup workflow
├── services/                    # Service files (empty for now)
├── docs/                        # Documentation
│   ├── README.md                # Full documentation
│   └── QUICKREF.md              # Quick reference
├── examples/                    # Usage examples
│   └── examples_autodarts.py
├── Makefile                     # Convenience commands
├── __init__.py                  # Package init
└── README.md                    # Main readme
```

## 🚀 Deployment Steps

### Step 1: Upload Files to Pi

**Option A: Using the upload script**
```bash
# On your local machine
chmod +x upload_to_pi.sh
./upload_to_pi.sh
```

**Option B: Manual SCP**
```bash
# Create directory on Pi
ssh cdo-vertex@cdo-vertex.local "sudo mkdir -p /opt/autodarts-manager/{config,scripts,services,docs,examples} && sudo chown -R cdo-vertex:cdo-vertex /opt/autodarts-manager"

# Upload config files
scp config/* cdo-vertex@cdo-vertex.local:/opt/autodarts-manager/config/

# Upload scripts
scp scripts/* cdo-vertex@cdo-vertex.local:/opt/autodarts-manager/scripts/

# Upload docs
scp docs/* cdo-vertex@cdo-vertex.local:/opt/autodarts-manager/docs/

# Upload examples
scp examples/* cdo-vertex@cdo-vertex.local:/opt/autodarts-manager/examples/

# Upload root files
scp Makefile __init__.py README.md cdo-vertex@cdo-vertex.local:/opt/autodarts-manager/

# Set permissions
ssh cdo-vertex@cdo-vertex.local "chmod +x /opt/autodarts-manager/scripts/*.py"
```

### Step 2: Run Setup on Pi

```bash
# SSH into Pi
ssh cdo-vertex@cdo-vertex.local

# Navigate to directory
cd /opt/autodarts-manager

# Run complete setup
sudo python3 scripts/setup.py

# Or install manually
sudo python3 scripts/autodarts_installer.py install
```

## 📋 Usage After Installation

### Using Scripts Directly

```bash
cd /opt/autodarts-manager

# Install/Update
sudo python3 scripts/autodarts_installer.py install
sudo python3 scripts/autodarts_installer.py update

# Service Management
sudo python3 scripts/autodarts_installer.py start
sudo python3 scripts/autodarts_installer.py stop
sudo python3 scripts/autodarts_installer.py restart

# Status & Logs
python3 scripts/autodarts_installer.py status
python3 scripts/autodarts_installer.py logs --follow

# UVC Hack
sudo python3 scripts/autodarts_installer.py uvc-install
```

### Using Makefile

```bash
cd /opt/autodarts-manager

make install      # Install autodarts
make update       # Update autodarts
make status       # Check status
make start        # Start service
make stop         # Stop service
make restart      # Restart service
make logs         # View logs
make logs-follow  # Follow logs
```

### As Python Module (in your code)

```python
import sys
sys.path.insert(0, '/opt/autodarts-manager')

from scripts.autodarts_installer import AutodartsInstaller
from config.autodarts_config import AutodartsConfig

# Basic usage
installer = AutodartsInstaller()
installer.install()

# With custom config
config = AutodartsConfig(
    enable_autostart=True,
    user="cdo-vertex"
)
installer = AutodartsInstaller(config)
installer.update()
```

## 🔗 Integration with WiFi Manager

Add to your `/opt/pi-wifi-manager/wifi_manager.py`:

```python
import sys
sys.path.insert(0, '/opt/autodarts-manager')

from scripts.autodarts_installer import AutodartsInstaller

def setup_autodarts():
    """Setup autodarts as part of system configuration"""
    installer = AutodartsInstaller()
    
    if not installer.is_installed():
        installer.install()
    else:
        installer.update()
    
    installer.enable_service()
    installer.start_service()
    
    return installer.get_status()
```

## 🎯 Complete System Setup Script

Create `/opt/setup_system.sh`:

```bash
#!/bin/bash
echo "Setting up complete dartboard system..."

# Setup WiFi Manager
cd /opt/pi-wifi-manager
python3 wifi_manager.py setup

# Setup Autodarts
cd /opt/autodarts-manager
sudo python3 scripts/setup.py

echo "✓ Complete system setup finished!"
```

## 📁 File List

### Config Files
- `config/__init__.py` - Config package init
- `config/autodarts_config.py` - Configuration dataclass

### Scripts
- `scripts/__init__.py` - Scripts package init
- `scripts/autodarts_installer.py` - Main installer (470+ lines)
- `scripts/setup.py` - Complete setup workflow

### Documentation
- `docs/README.md` - Full documentation
- `docs/QUICKREF.md` - Quick reference guide

### Examples
- `examples/examples_autodarts.py` - 11 usage examples

### Root Files
- `Makefile` - Convenience commands
- `__init__.py` - Package init
- `README.md` - Main readme

## ✅ Verification

After deployment, verify everything is in place:

```bash
# SSH to Pi
ssh cdo-vertex@cdo-vertex.local

# Check structure
ls -R /opt/autodarts-manager

# Test import
python3 -c "import sys; sys.path.insert(0, '/opt/autodarts-manager'); from scripts.autodarts_installer import AutodartsInstaller; print('✓ Import successful')"

# Check status
cd /opt/autodarts-manager
python3 scripts/autodarts_installer.py status
```

## 🔧 Troubleshooting

### Import Errors
```python
# Always add to path first
import sys
sys.path.insert(0, '/opt/autodarts-manager')
```

### Permission Issues
```bash
sudo chown -R cdo-vertex:cdo-vertex /opt/autodarts-manager
chmod +x /opt/autodarts-manager/scripts/*.py
```

### Missing Dependencies
```bash
sudo apt install curl -y
```
