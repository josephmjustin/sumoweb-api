# Quick Start Guide

## 1. Start the API

### Option A: Docker Compose (Easiest)
```bash
docker-compose up --build
```

### Option B: Docker
```bash
docker build -t sumo-api .
docker run -p 8000:8000 sumo-api
```

### Option C: Local Python
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 2. Test the API

### Using the Web Interface (Recommended)

**Open the modern web interface:**

1. Simply open `frontend/index.html` in your browser
   
   OR serve it with:
   ```bash
   python -m http.server 8080 --directory frontend
   ```
   Then visit: http://localhost:8080

2. **Drag and drop** your ZIP file or click to browse

3. Click **"Run Simulation"** button

4. Watch the **progress bar** as your simulation runs

5. **Download** output files when complete

### Using cURL

**Upload simulation files:**
```bash
curl -X POST "http://localhost:8000/upload/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@simulation.zip"
```

**Run simulation:**
```bash
curl "http://localhost:8000/run_simulation/"
```

**List output files:**
```bash
curl "http://localhost:8000/output_files"
```

**Download output:**
```bash
curl "http://localhost:8000/download/edgedata.out.xml" -o output.xml
```

### Using Swagger UI

Visit: http://localhost:8000/docs

- Interactive API documentation
- Test all endpoints directly
- See request/response examples

## 3. Verify It's Running

**Check health:**
```bash
curl http://localhost:8000/health
```

**Check API info:**
```bash
curl http://localhost:8000
```

**View logs:**
```bash
docker-compose logs -f sumo-api
```

## Common Issues

### Can't access localhost:8000?

✅ **Solutions:**
- Check container is running: `docker ps`
- View logs: `docker-compose logs`
- Try: http://127.0.0.1:8000

### Port already in use?

✅ **Solutions:**
- Change port in `docker-compose.yml` to `8001:8000`
- Update `frontend/index.html`: `const API_BASE = 'http://localhost:8001';`

### Simulation fails?

✅ **Check:**
- ZIP contains `0.sumocfg` file
- SUMO configuration files are valid
- View detailed errors in API logs

### CORS errors in browser?

✅ **Solutions:**
- Ensure API is running on `localhost:8000`
- Check CORS settings in `app/core/config.py`
- Serve frontend via HTTP server (not file://)

## Next Steps

- Read full documentation in `README.md`
- Customize settings in `app/core/config.py`
- Add your own SUMO simulation files
- Deploy to production using Docker

## Example Files

Your ZIP should contain:
```
simulation.zip
├── 0.sumocfg          # Main config
├── network0.xml       # Road network
├── Routes.Rou.xml     # Vehicle routes
├── vtypes.add.xml     # Vehicle types (optional)
└── edgedata.add.xml   # Edge data (optional)
```

## Getting Help

- Check logs: `docker-compose logs -f`
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health
- SUMO docs: https://sumo.dlr.de/docs/
