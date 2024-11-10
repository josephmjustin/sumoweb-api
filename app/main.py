from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import subprocess
import glob
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
UPLOAD_DIR = "./uploads"
ALLOWED_EXTENSIONS = {'.zip'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

def is_valid_file(filename: str) -> bool:
    """Check if the file has an allowed extension."""
    return any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Validate file extension
        if not is_valid_file(file.filename):
            logger.error(f"Invalid file type: {file.filename}")
            return JSONResponse(
                content={"status": "error", "message": "Invalid file type. Only ZIP files are allowed."},
                status_code=400
            )

        # Create upload directory if it doesn't exist
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        logger.info(f"Saving file to {file_path}")

        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"File {file.filename} saved successfully")

        # Extract the ZIP file
        try:
            shutil.unpack_archive(file_path, UPLOAD_DIR)
            logger.info(f"ZIP file {file.filename} extracted successfully")
            os.remove(file_path)  # Optionally remove the ZIP file after extraction
        except Exception as e:
            logger.error(f"Error extracting ZIP file: {e}")
            return JSONResponse(
                content={"status": "error", "message": f"Error extracting ZIP file: {str(e)}"},
                status_code=500
            )

        return JSONResponse(
            content={"status": "success", "message": "File uploaded and extracted successfully"},
            status_code=200
        )

    except Exception as e:
        logger.error(f"Unexpected error during file upload: {str(e)}")
        return JSONResponse(
            content={"status": "error", "message": f"Unexpected error: {str(e)}"},
            status_code=500
        )


@app.get("/run_simulation/")
async def run_simulation():
    try:
        # Check if required files exist
        config_file = os.path.join(UPLOAD_DIR, "0.sumocfg")
        if not os.path.exists(config_file):
            return JSONResponse(
                content={
                    "status": "error",
                    "message": "Simulation configuration file not found"
                },
                status_code=404
            )

        # Run the simulation
        result = subprocess.run(
            ["sumo", "-c", config_file],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.returncode == 0:
            # Get all output XML files
            output_files = glob.glob(os.path.join(UPLOAD_DIR, "*.out.xml"))
            return JSONResponse(
                content={
                    "status": "success",
                    "message": "Simulation completed successfully!",
                    "output_files": [os.path.basename(f) for f in output_files]
                },
                status_code=200
            )
        else:
            logger.error(f"Simulation error: {result.stderr}")
            return JSONResponse(
                content={
                    "status": "error",
                    "message": f"Simulation failed: {result.stderr}"
                },
                status_code=500
            )

    except subprocess.TimeoutExpired:
        return JSONResponse(
            content={
                "status": "error",
                "message": "Simulation timed out after 5 minutes"
            },
            status_code=504
        )
    except Exception as e:
        logger.error(f"Error running simulation: {str(e)}")
        return JSONResponse(
            content={
                "status": "error",
                "message": f"Error running simulation: {str(e)}"
            },
            status_code=500
        )

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        return JSONResponse(
            content={
                "status": "error",
                "message": "File not found"
            },
            status_code=404
        )
    return FileResponse(file_path, filename=filename)

@app.get("/output_files")
async def list_output_files():
    output_files = glob.glob(os.path.join(UPLOAD_DIR, "*.out.xml"))
    return {"files": [os.path.basename(f) for f in output_files]}

# Optional: Add endpoint to check server status
@app.get("/health")
async def health_check():
    return {"status": "healthy"}