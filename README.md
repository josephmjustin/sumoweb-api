# SUMO Web API

FastAPI-based web service for running SUMO (Simulation of Urban MObility) traffic simulations.

## Features

- ✅ Upload ZIP files containing SUMO simulation configurations
- ✅ Run SUMO simulations via REST API
- ✅ Download simulation output files
- ✅ Docker containerized deployment
- ✅ CORS enabled for frontend integration
- ✅ Comprehensive logging

## Project Structure

```
sumoweb-api/
├── app/
│   ├── api/                    # API route handlers
│   │   ├── files.py           # File upload/download endpoints
│   │   └── simulation.py      # Simulation execution endpoints
│   ├── core/                   # Core configurations
│   │   └── config.py          # Application settings
│   ├── utils/                  # Utility functions
│   │   ├── file_handler.py    # File operations
│   │   └── sumo_runner.py     # SUMO execution logic
│   └── main.py                # FastAPI application entry
├── frontend/                   # Frontend files
│   └── index.html             # Web interface
├── uploads/                    # Upload directory (auto-created)
├── Dockerfile                  # Docker build configuration
├── docker-compose.yml          # Docker compose setup
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## Prerequisites

- Docker and Docker Compose
- OR Python 3.8+ with SUMO installed locally

## Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   cd C:\Users\justi\Work\Personal\sumoweb\sumoweb-api
   ```

2. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Access the API**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Using Docker without Compose

```bash
docker build -t sumo-api .
docker run -p 8000:8000 -v ./uploads:/workspace/uploads sumo-api
```

### Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install SUMO**
   - Ubuntu: `sudo add-apt-repository ppa:sumo/stable && sudo apt-get install sumo sumo-tools`
   - Windows/Mac: Download from https://sumo.dlr.de/docs/Downloads.php

3. **Run the server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Endpoints

### File Management

#### Upload ZIP File
```http
POST /upload/
Content-Type: multipart/form-data

Body: file (ZIP containing SUMO configuration files)
```

**Response:**
```json
{
  "status": "success",
  "message": "File uploaded and extracted successfully"
}
```

#### List Output Files
```http
GET /output_files
```

**Response:**
```json
{
  "files": ["edgedata.out.xml", "fc.out.xml"]
}
```

#### Download File
```http
GET /download/{filename}
```

### Simulation

#### Run Simulation
```http
GET /run_simulation/
```

**Response:**
```json
{
  "status": "success",
  "message": "Simulation completed successfully!",
  "output_files": ["edgedata.out.xml"]
}
```

### System

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and customize:

```env
DEBUG=False
LOG_LEVEL=INFO
CORS_ORIGINS=*
SUMO_HOME=/usr/share/sumo
```

### Application Settings

Edit `app/core/config.py` to modify:
- Upload directory
- File size limits
- Allowed file extensions
- SUMO timeout duration

## SUMO Configuration Requirements

Your ZIP file should contain:
- `0.sumocfg` - Main SUMO configuration file
- Network file (`.net.xml`)
- Route file (`.rou.xml`)
- Additional files as needed (vtypes, edge data, etc.)

Example structure:
```
simulation.zip
├── 0.sumocfg
├── network0.xml
├── Routes.Rou.xml
├── vtypes.add.xml
└── edgedata.add.xml
```

## Frontend Integration

Open `frontend/index.html` in a browser or serve it via a web server:

```bash
# Simple HTTP server
python -m http.server 8080 --directory frontend
```

Then access: http://localhost:8080

## Troubleshooting

### Port Already in Use
```bash
# Change port in docker-compose.yml or use:
docker-compose up -p 8001:8000
```

### Upload Directory Permissions
```bash
chmod 777 uploads/
```

### SUMO Not Found
Ensure SUMO_HOME environment variable is set correctly:
```bash
echo $SUMO_HOME
which sumo
```

### Docker Build Issues
```bash
# Clean build
docker-compose down
docker system prune -a
docker-compose up --build
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black app/
```

### Linting
```bash
flake8 app/
```

## Logs

View application logs:
```bash
docker-compose logs -f sumo-api
```

## Security Notes

- In production, update `CORS_ORIGINS` to specific domains
- Add authentication for sensitive endpoints
- Implement file size validation
- Use HTTPS in production

## License

MIT

## Support

For issues and questions:
- GitHub Issues: [Create an issue]
- SUMO Documentation: https://sumo.dlr.de/docs/


