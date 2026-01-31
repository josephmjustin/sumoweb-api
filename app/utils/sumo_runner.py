"""SUMO simulation utilities."""
import subprocess
import logging
from pathlib import Path
from typing import Tuple

from app.core.config import settings

logger = logging.getLogger(__name__)

class SimulationError(Exception):
    """Custom exception for simulation errors."""
    pass

def run_sumo_simulation(config_file: Path) -> Tuple[bool, str]:
    """
    Run SUMO simulation with the given configuration file.
    
    Args:
        config_file: Path to SUMO configuration file
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        if not config_file.exists():
            raise SimulationError(f"Configuration file not found: {config_file}")
        
        logger.info(f"Starting SUMO simulation with config: {config_file}")
        
        result = subprocess.run(
            ["sumo", "-c", str(config_file)],
            capture_output=True,
            text=True,
            timeout=settings.SUMO_TIMEOUT
        )
        
        if result.returncode == 0:
            logger.info("Simulation completed successfully")
            return True, "Simulation completed successfully!"
        else:
            error_msg = result.stderr or "Unknown error"
            logger.error(f"Simulation failed: {error_msg}")
            return False, f"Simulation failed: {error_msg}"
            
    except subprocess.TimeoutExpired:
        error_msg = f"Simulation timed out after {settings.SUMO_TIMEOUT} seconds"
        logger.error(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"Error running simulation: {str(e)}"
        logger.error(error_msg)
        return False, error_msg
