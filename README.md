# SUMO Web API

FastAPI-based web service for running SUMO (Simulation of Urban MObility) traffic simulations.

## Features

- ✅ Upload ZIP files containing SUMO simulation configurations
- ✅ Run SUMO simulations via REST API
- ✅ Download simulation output files
- ✅ Modern web interface with drag & drop support
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
│   └── index.html             # Modern web interface
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

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   - Web Interface: Open `frontend/index.html` in your browser
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

## Testing the API

### Option 1: Web Interface (Recommended)

1. **Start the API server** (using Docker or locally as shown above)

2. **Open the web interface**
   
   Simply open `frontend/index.html` in your browser:
   ```bash
   # Windows
   start frontend/index.html
   
   # macOS
   open frontend/index.html
   
   # Linux
   xdg-open frontend/index.html
   ```
   
   Or serve it with Python's HTTP server:
   ```bash
   # From project root
   python -m http.server 8080 --directory frontend
   ```
   Then visit: http://localhost:8080

3. **Use the interface**
   - Drag and drop your ZIP file or click to browse
   - Click "Run Simulation" button
   - Watch the progress bar as simulation runs
   - Download output files when complete

### Option 2: Using cURL

#### Upload and Extract ZIP
```bash
curl -X POST "http://localhost:8000/upload/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@simulation.zip"
```

#### Run Simulation
```bash
curl "http://localhost:8000/run_simulation/"
```

#### List Output Files
```bash
curl "http://localhost:8000/output_files"
```

#### Download Output File
```bash
curl "http://localhost:8000/download/edgedata.out.xml" -o output.xml
```

### Option 3: Using Postman or Thunder Client

1. Import the API endpoints
2. Upload: POST to `http://localhost:8000/upload/` with file in form-data
3. Simulate: GET to `http://localhost:8000/run_simulation/`
4. Download: GET to `http://localhost:8000/download/{filename}`

### Option 4: Interactive API Documentation

Visit http://localhost:8000/docs to use Swagger UI:
- Test all endpoints interactively
- See request/response schemas
- Try different parameters

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

#### Root Endpoint
```http
GET /
```

**Response:**
```json
{
  "name": "SUMO Web API",
  "version": "1.0.0",
  "status": "running"
}
```

## Web Interface Features

The modern web interface (`frontend/index.html`) includes:

- **🎨 Beautiful Design**: Modern gradient background with card-based layout
- **📦 Drag & Drop**: Simply drag your ZIP file onto the upload area
- **📊 Progress Tracking**: Real-time progress bar with status updates
- **✨ Animations**: Smooth transitions and visual feedback
- **📱 Responsive**: Works perfectly on desktop, tablet, and mobile
- **⬇️ Easy Downloads**: One-click download for all output files
- **🚀 No Build Required**: Pure HTML/CSS/JavaScript, no dependencies

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

## Troubleshooting

### Cannot Access Web Interface

**Problem:** Frontend can't connect to API (CORS errors)

**Solution:** Ensure the API is running on `localhost:8000` and check browser console for errors.

### Port Already in Use

```bash
# Change port in docker-compose.yml or use:
docker-compose up -p 8001:8000

# Then update API_BASE in frontend/index.html to:
const API_BASE = 'http://localhost:8001';
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

### File Upload Fails

- Check file is a valid ZIP
- Ensure ZIP contains `0.sumocfg`
- Verify file size is under 100MB
- Check API logs for detailed errors

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

### Viewing Logs

```bash
# Docker Compose
docker-compose logs -f sumo-api

# Docker
docker logs -f <container_id>

# Local
# Logs appear in terminal where uvicorn is running
```

## Security Notes

- In production, update `CORS_ORIGINS` to specific domains
- Add authentication for sensitive endpoints
- Implement file size validation
- Use HTTPS in production
- Consider rate limiting for public deployments

## Deployment to Production

1. **Update CORS settings** in `app/core/config.py`
2. **Set environment variables** properly
3. **Use a reverse proxy** (nginx, Traefik)
4. **Enable HTTPS**
5. **Add authentication** if needed
6. **Monitor logs and metrics**

## Example Workflow

1. **Start the API**
   ```bash
   docker-compose up
   ```

2. **Open the web interface**
   - Open `frontend/index.html` in your browser

3. **Upload your simulation**
   - Drag your ZIP file containing SUMO config
   - Click "Run Simulation"

4. **Monitor progress**
   - Watch the animated progress bar
   - See real-time status updates

5. **Download results**
   - Click download on any output file
   - Files are saved to your downloads folder

## License

MIT

## Support

For issues and questions:
- GitHub Issues: [Create an issue]
- SUMO Documentation: https://sumo.dlr.de/docs/

## Changelog

### v1.0.0 (2025-01-31)
- Initial release
- Modern web interface with drag & drop
- File upload and extraction
- SUMO simulation execution
- Output file management
- Docker support
- Comprehensive error handling
