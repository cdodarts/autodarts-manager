# Autodarts Manager

Modular management system for Autodarts Desktop installation and configuration.

## Directory Structure

```
autodarts-manager/
├── config/              # Configuration files
│   ├── __init__.py
│   └── autodarts_config.py
├── scripts/             # Main scripts
│   ├── __init__.py
│   ├── autodarts_installer.py
│   └── setup.py
├── services/            # Service-related files
│   └── (systemd service files, if needed)
├── docs/                # Documentation
│   ├── README.md
│   └── QUICKREF.md
├── examples/            # Example scripts
│   └── examples_autodarts.py
├── Makefile             # Convenience commands
└── __init__.py          # Package init
```

## Quick Start

```bash
# Navigate to the directory
cd /opt/autodarts-manager

# Run complete setup
sudo python3 scripts/setup.py

# Or use the installer directly
sudo python3 scripts/autodarts_installer.py install

# Check status
python3 scripts/autodarts_installer.py status
```

## Using Make

```bash
cd /opt/autodarts-manager

make install     # Install autodarts
make update      # Update autodarts
make status      # Check status
make logs        # View logs
make help        # See all commands
```

## As Python Module

```python
import sys
sys.path.insert(0, '/opt/autodarts-manager')

from scripts.autodarts_installer import AutodartsInstaller
from config.autodarts_config import AutodartsConfig

# Create installer
installer = AutodartsInstaller()

# Install
installer.install()

# Or with custom config
config = AutodartsConfig(enable_autostart=True)
installer = AutodartsInstaller(config)
installer.update()
```

## Documentation

- Full documentation: `docs/README.md`
- Quick reference: `docs/QUICKREF.md`
- Examples: `examples/examples_autodarts.py`

## Installation Location

This package should be installed at `/opt/autodarts-manager/` to match the project structure.
