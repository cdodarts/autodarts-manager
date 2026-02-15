# Autodarts Installer Module

A modular, maintainable Python module for installing and updating the autodarts-caller application on Raspberry Pi systems.

## Features

- ✅ **Modular Design**: Clean separation of concerns with dedicated classes
- ✅ **DRY Principles**: No code duplication, reusable components
- ✅ **Error Handling**: Comprehensive error handling and logging
- ✅ **Easy to Extend**: Add new features without modifying core logic
- ✅ **Well Tested**: Includes comprehensive unit tests
- ✅ **CLI Support**: Can be used as a command-line tool or Python module
- ✅ **Version Checking**: Automatically detects if updates are needed
- ✅ **Service Management**: Handles systemd service stop/start

## Installation

Simply copy `autodarts_installer.py` to your project:

```bash
# Make it executable
chmod +x autodarts_installer.py

# Or use it as a module
python3 -c "from autodarts_installer import AutodartsInstaller"
```

## Quick Start

### Command Line Usage

```bash
# Check status
./autodarts_installer.py status

# Install autodarts
./autodarts_installer.py install

# Update autodarts
./autodarts_installer.py update

# Custom installation directory
./autodarts_installer.py install --install-dir /home/pi/autodarts

# Enable debug logging
./autodarts_installer.py install --debug
```

### Python Module Usage

```python
from autodarts_installer import AutodartsInstaller

# Create installer instance
installer = AutodartsInstaller()

# Install
if installer.install():
    print("Installation successful!")

# Or update
if installer.update():
    print("Update successful!")

# Check status
status = installer.get_status()
print(f"Installed: {status['installed']}")
print(f"Current version: {status['current_version']}")
```

## Configuration

Customize the installation by creating a custom configuration:

```python
from autodarts_installer import AutodartsInstaller, AutodartsConfig
from pathlib import Path

# Create custom config
config = AutodartsConfig(
    install_dir=Path("/opt/autodarts"),
    venv_dir=Path("/opt/autodarts/venv"),
    service_name="autodarts-caller",
    repo_url="https://github.com/lbormann/autodarts-caller.git",
    user="pi",
    python_version="python3"
)

# Use custom config
installer = AutodartsInstaller(config)
```

## Architecture

### Class Structure

```
AutodartsConfig
├── Configuration dataclass
└── Holds all installation parameters

AutodartsInstaller
├── __init__()              # Initialize with config
├── check_dependencies()    # Verify system dependencies
├── is_installed()          # Check if already installed
├── get_current_version()   # Get installed version
├── get_latest_version()    # Get latest available version
├── install()               # Fresh installation
├── update()                # Update existing installation
├── get_status()            # Get installation status
└── Internal methods:
    ├── _setup_logging()
    ├── _command_exists()
    ├── _run_command()
    ├── stop_service()
    ├── start_service()
    ├── clone_repository()
    ├── update_repository()
    ├── setup_virtual_environment()
    ├── install_dependencies()
    └── _execute_steps()
```

### Installation Flow

```
install()
├── check_dependencies()
├── is_installed() → fail if exists
├── clone_repository()
├── setup_virtual_environment()
├── install_dependencies()
└── return success/failure

update()
├── is_installed() → fail if not exists
├── get_current_version()
├── get_latest_version()
├── stop_service()
├── update_repository()
├── setup_virtual_environment()
├── install_dependencies()
├── start_service()
└── return success/failure
```

## Usage Examples

See `examples_autodarts.py` for comprehensive examples:

1. **Basic Installation** - Simple install with defaults
2. **Custom Installation** - Custom paths and configuration
3. **Update** - Update existing installation
4. **Check Status** - Get installation information
5. **Conditional Install/Update** - Smart install or update
6. **Error Handling** - Robust error handling patterns
7. **Integration** - Use within larger setup scripts

## Testing

Run the test suite:

```bash
# Run all tests
python3 -m pytest test_autodarts_installer.py -v

# Or using unittest
python3 test_autodarts_installer.py

# Run specific test
python3 -m pytest test_autodarts_installer.py::TestAutodartsInstaller::test_install_success
```

Test coverage includes:
- Configuration handling
- Dependency checking
- Version detection
- Installation flow
- Update flow
- Service management
- Error conditions

## Extending the Module

### Adding a New Step

To add a new installation step:

```python
class AutodartsInstaller:
    def my_new_step(self) -> bool:
        """Description of what this step does"""
        try:
            self.logger.info("Running my new step")
            # Your implementation here
            return True
        except Exception as e:
            self.logger.error(f"New step failed: {e}")
            return False
    
    def install(self) -> bool:
        """Modified install to include new step"""
        steps = [
            ("Clone repository", self.clone_repository),
            ("My new step", self.my_new_step),  # Add here
            ("Setup virtual environment", self.setup_virtual_environment),
            ("Install dependencies", self.install_dependencies),
        ]
        return self._execute_steps(steps)
```

### Adding Custom Validation

```python
class CustomAutodartsInstaller(AutodartsInstaller):
    """Extended installer with custom validation"""
    
    def validate_system(self) -> bool:
        """Custom system validation"""
        # Check disk space
        # Check network connectivity
        # etc.
        return True
    
    def install(self) -> bool:
        """Override install with validation"""
        if not self.validate_system():
            self.logger.error("System validation failed")
            return False
        return super().install()
```

## Error Handling

The module provides comprehensive error handling:

```python
try:
    installer = AutodartsInstaller()
    
    if not installer.check_dependencies():
        print("Install dependencies first:")
        print("sudo apt-get install git python3 python3-venv python3-pip")
        sys.exit(1)
    
    if not installer.install():
        print("Installation failed - check logs")
        sys.exit(1)
        
except Exception as e:
    print(f"Unexpected error: {e}")
    sys.exit(1)
```

## Logging

The module uses Python's logging module:

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Or configure custom logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('autodarts_install.log'),
        logging.StreamHandler()
    ]
)
```

## Dependencies

### System Requirements
- Git
- Python 3.7+
- python3-venv
- python3-pip

### Python Requirements
None! The module uses only Python standard library.

## Integration Examples

### With Your Setup Script

```python
#!/usr/bin/env python3
from autodarts_installer import AutodartsInstaller

def main():
    installer = AutodartsInstaller()
    
    # Install or update
    if not installer.is_installed():
        print("Installing autodarts...")
        installer.install()
    else:
        print("Updating autodarts...")
        installer.update()

if __name__ == '__main__':
    main()
```

### With Systemd Service

The installer automatically manages the systemd service during updates:
- Stops service before update
- Performs update
- Starts service after update

## Troubleshooting

### Installation Fails

1. Check dependencies:
   ```bash
   ./autodarts_installer.py status
   ```

2. Verify git access:
   ```bash
   git ls-remote https://github.com/lbormann/autodarts-caller.git
   ```

3. Check permissions:
   ```bash
   ls -la /opt/autodarts
   ```

### Update Fails

1. Check current state:
   ```bash
   cd /opt/autodarts
   git status
   ```

2. Manual reset if needed:
   ```bash
   git fetch origin
   git reset --hard origin/main
   ```

## Best Practices

1. **Always check status first**: Use `get_status()` before operations
2. **Handle errors gracefully**: Check return values and log errors
3. **Use custom configs**: Don't modify the default config
4. **Test in development**: Use a custom install directory for testing
5. **Keep it DRY**: Extend the class rather than duplicating code

## License

This module is provided as-is for use with the autodarts-caller project.

## Contributing

When extending this module:

1. Maintain the existing architecture
2. Add tests for new functionality
3. Update documentation
4. Follow the existing code style
5. Keep methods focused and single-purpose

## Changelog

### Version 1.0.0
- Initial release
- Install and update functionality
- Version checking
- Service management
- Comprehensive testing
- CLI support
