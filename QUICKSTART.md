# Quick Start Guide

## Start the API

### Option 1: Docker Compose (Easiest)
```bash
docker-compose up --build
```

### Option 2: Docker
```bash
docker build -t sumo-api .
docker run -p 8000:8000 sumo-api
```

### Option 3: Local Python
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Verify It's Running

1. Open browser: http://localhost:8000
2. Check health: http://localhost:8000/health
3. View API docs: http://localhost:8000/docs

## Test the API

### 1. Upload Simulation Files
```bash
curl -X POST "http://localhost:8000/upload/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_simulation.zip"
```

### 2. Run Simulation
```bash
curl "http://localhost:8000/run_simulation/"
```

### 3. List Output Files
```bash
curl "http://localhost:8000/output_files"
```

### 4. Download Output
```bash
curl "http://localhost:8000/download/edgedata.out.xml" -o output.xml
```

## Using the Frontend

1. Open `frontend/index.html` in browser
2. Upload your ZIP file
3. Click "Run Simulation"
4. Download results

## Common Issues

**Can't access localhost:8000?**
- Check container is running: `docker ps`
- Check logs: `docker-compose logs`
- Try: http://127.0.0.1:8000

**Simulation fails?**
- Ensure ZIP contains `0.sumocfg`
- Check SUMO files are valid
- View logs for errors

**Port already in use?**
- Change port in docker-compose.yml
- Or use: `docker-compose up -p 8001:8000`
