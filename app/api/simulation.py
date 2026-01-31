"""SUMO simulation routes."""
import logging
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.utils import run_sumo_simulation, get_output_files

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/run_simulation/")
async def run_simulation():
    """
    Run SUMO traffic simulation with uploaded configuration.
    """
    try:
        # Check if required configuration file exists
        config_file = settings.UPLOAD_DIR / settings.SUMO_CONFIG_FILE
        
        if not config_file.exists():
            raise HTTPException(
                status_code=404,
                detail="Simulation configuration file not found"
            )

        # Run the simulation
        success, message = run_sumo_simulation(config_file)

        if success:
            # Get all output XML files
            output_files = get_output_files()
            return JSONResponse(
                content={
                    "status": "success",
                    "message": message,
                    "output_files": output_files
                },
                status_code=200
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=message
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error running simulation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error running simulation: {str(e)}"
        )
