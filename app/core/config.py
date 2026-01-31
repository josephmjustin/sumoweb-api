"""Configuration settings for the SUMO API."""
import os
from pathlib import Path
from typing import Set

class Settings:
    """Application settings."""
    
    # API Settings
    APP_NAME: str = "SUMO Web API"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # CORS Settings
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # File Upload Settings
    UPLOAD_DIR: Path = Path("./uploads")
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS: Set[str] = {'.zip'}
    
    # SUMO Settings
    SUMO_CONFIG_FILE: str = "0.sumocfg"
    SUMO_TIMEOUT: int = 300  # 5 minutes
    SUMO_HOME: str = os.getenv("SUMO_HOME", "/usr/share/sumo")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
