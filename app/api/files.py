"""File upload and management routes."""
import logging
from pathlib import Path
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse

from app.core.config import settings
from app.utils import (
    is_valid_file,
    save_upload_file,
    extract_archive,
    cleanup_file,
    ensure_upload_dir,
    get_output_files
)

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload and extract a ZIP file containing SUMO simulation files.
    """
    try:
        # Validate file extension
        if not is_valid_file(file.filename):
            logger.error(f"Invalid file type: {file.filename}")
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Only ZIP files are allowed."
            )

        # Ensure upload directory exists
        ensure_upload_dir()
        
        file_path = settings.UPLOAD_DIR / file.filename
        logger.info(f"Saving file to {file_path}")

        # Save the uploaded file
        await save_upload_file(file, file_path)

        # Extract the ZIP file
        try:
            extract_archive(file_path, settings.UPLOAD_DIR)
            cleanup_file(file_path)  # Remove ZIP after extraction
        except Exception as e:
            logger.error(f"Error extracting ZIP file: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Error extracting ZIP file: {str(e)}"
            )

        return JSONResponse(
            content={
                "status": "success",
                "message": "File uploaded and extracted successfully"
            },
            status_code=200
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during file upload: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

@router.get("/download/{filename}")
async def download_file(filename: str):
    """
    Download a specific output file.
    """
    file_path = settings.UPLOAD_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )
    
    return FileResponse(file_path, filename=filename)

@router.get("/output_files")
async def list_output_files():
    """
    List all output XML files.
    """
    files = get_output_files()
    return {"files": files}
