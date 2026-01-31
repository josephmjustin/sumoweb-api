"""File utilities for handling uploads and validations."""
import os
import shutil
from pathlib import Path
from typing import Optional
from fastapi import UploadFile
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

def is_valid_file(filename: str) -> bool:
    """Check if the file has an allowed extension."""
    return any(filename.lower().endswith(ext) for ext in settings.ALLOWED_EXTENSIONS)

async def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    """Save uploaded file to destination."""
    try:
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        logger.info(f"File saved successfully: {destination}")
    except Exception as e:
        logger.error(f"Error saving file {destination}: {e}")
        raise

def extract_archive(file_path: Path, extract_to: Path) -> None:
    """Extract archive file to specified directory."""
    try:
        shutil.unpack_archive(file_path, extract_to)
        logger.info(f"Archive extracted: {file_path} -> {extract_to}")
    except Exception as e:
        logger.error(f"Error extracting archive {file_path}: {e}")
        raise

def cleanup_file(file_path: Path) -> None:
    """Remove a file if it exists."""
    try:
        if file_path.exists():
            os.remove(file_path)
            logger.info(f"File removed: {file_path}")
    except Exception as e:
        logger.error(f"Error removing file {file_path}: {e}")

def ensure_upload_dir() -> None:
    """Ensure upload directory exists."""
    settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def get_output_files(pattern: str = "*.out.xml") -> list[str]:
    """Get list of output files matching pattern."""
    import glob
    files = glob.glob(str(settings.UPLOAD_DIR / pattern))
    return [os.path.basename(f) for f in files]
