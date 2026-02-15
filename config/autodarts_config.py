"""Autodarts Configuration Module"""
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

DEFAULT_CONFIG = AutodartsConfig()
