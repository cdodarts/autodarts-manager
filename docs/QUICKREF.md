# Autodarts Installer - Quick Reference

## 🚀 Quick Start

### Command Line
```bash
# Install
./autodarts_installer.py install

# Update
./autodarts_installer.py update

# Check status
./autodarts_installer.py status
```

### Python
```python
from autodarts_installer import AutodartsInstaller

installer = AutodartsInstaller()
installer.install()  # or installer.update()
```

## 📋 Common Use Cases

### 1. First-Time Installation
```python
from autodarts_installer import AutodartsInstaller

installer = AutodartsInstaller()

# Check if dependencies are installed
if not installer.check_dependencies():
    print("Please install: git python3 python3-venv python3-pip")
    exit(1)

# Install
if installer.install():
    print("Installation successful!")
```

### 2. Update Check and Install
```python
from autodarts_installer import AutodartsInstaller

installer = AutodartsInstaller()

# Get versions
current = installer.get_current_version()
latest = installer.get_latest_version()

if current != latest:
    print(f"Update available: {current[:8]} -> {latest[:8]}")
    installer.update()
else:
    print("Already up to date")
```

### 3. Smart Install/Update
```python
from autodarts_installer import AutodartsInstaller

installer = AutodartsInstaller()

if not installer.is_installed():
    installer.install()
else:
    installer.update()
```

### 4. Custom Installation Path
```python
from autodarts_installer import AutodartsInstaller, AutodartsConfig
from pathlib import Path

config = AutodartsConfig(
    install_dir=Path("/home/pi/autodarts"),
    venv_dir=Path("/home/pi/autodarts/venv")
)

installer = AutodartsInstaller(config)
installer.install()
```

### 5. Get Installation Status
```python
from autodarts_installer import AutodartsInstaller

installer = AutodartsInstaller()
status = installer.get_status()

print(f"Installed: {status['installed']}")
print(f"Path: {status['install_dir']}")
print(f"Version: {status['current_version'][:8]}")
```

### 6. Complete Setup Script
```python
#!/usr/bin/env python3
from autodarts_installer import AutodartsInstaller
import sys

def main():
    installer = AutodartsInstaller()
    
    # Check dependencies
    if not installer.check_dependencies():
        print("Missing dependencies!")
        return False
    
    # Install or update
    if not installer.is_installed():
        return installer.install()
    else:
        current = installer.get_current_version()
        latest = installer.get_latest_version()
        if current != latest:
            return installer.update()
        return True

if __name__ == '__main__':
    sys.exit(0 if main() else 1)
```

### 7. Error Handling
```python
from autodarts_installer import AutodartsInstaller
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)

installer = AutodartsInstaller()

try:
    if not installer.install():
        print("Installation failed - check logs above")
except Exception as e:
    print(f"Error: {e}")
```

## 🔧 Configuration Options

```python
from autodarts_installer import AutodartsConfig
from pathlib import Path

config = AutodartsConfig(
    install_dir=Path("/opt/autodarts"),          # Installation directory
    venv_dir=Path("/opt/autodarts/venv"),        # Virtual environment path
    service_name="autodarts-caller",             # Systemd service name
    repo_url="https://github.com/...",           # Git repository URL
    user="pi",                                    # System user
    python_version="python3"                      # Python command
)
```

## 📊 Status Dictionary

```python
status = installer.get_status()
# Returns:
{
    'installed': bool,           # Is autodarts installed?
    'current_version': str,      # Current git commit hash
    'latest_version': str,       # Latest git commit hash
    'install_dir': str,          # Installation directory path
    'venv_exists': bool         # Does virtual environment exist?
}
```

## 🛠️ Available Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `install()` | Fresh installation | `bool` |
| `update()` | Update existing installation | `bool` |
| `is_installed()` | Check if installed | `bool` |
| `get_current_version()` | Get installed version | `str` or `None` |
| `get_latest_version()` | Get latest version | `str` or `None` |
| `get_status()` | Get installation info | `dict` |
| `check_dependencies()` | Verify system dependencies | `bool` |

## ⚡ Using with Makefile

```bash
# Installation
make install
make update
make status

# Development
make test
make lint
make check

# Cleanup
make clean
```

## 🔍 Troubleshooting

### Check Dependencies
```bash
./autodarts_installer.py status
```

### Manual Git Check
```bash
cd /opt/autodarts
git status
git log -1
```

### Reset Installation
```bash
cd /opt/autodarts
git fetch origin
git reset --hard origin/main
```

### View Logs
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Then run installer with debug enabled
installer = AutodartsInstaller()
```

## 🎯 Integration Patterns

### Pattern 1: Standalone Script
```python
#!/usr/bin/env python3
from autodarts_installer import AutodartsInstaller

AutodartsInstaller().update()
```

### Pattern 2: Part of Setup System
```python
class SystemSetup:
    def __init__(self):
        self.autodarts = AutodartsInstaller()
    
    def setup(self):
        self.configure_network()
        self.autodarts.install()  # <-- Integrated here
        self.configure_services()
```

### Pattern 3: Conditional Update
```python
def ensure_latest():
    installer = AutodartsInstaller()
    if installer.is_installed():
        current = installer.get_current_version()
        latest = installer.get_latest_version()
        if current != latest:
            installer.update()
            return "updated"
        return "current"
    else:
        installer.install()
        return "installed"
```

## 📝 Notes

- All methods return `bool` for success/failure
- Logging is built-in via Python's `logging` module
- Service management is automatic during updates
- Virtual environment is created automatically
- Git operations use `origin/main` branch

## 🔗 Links

- Repository: https://github.com/lbormann/autodarts-caller
- Full Documentation: See README.md
- Examples: See examples_autodarts.py
