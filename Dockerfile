FROM ubuntu:22.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Add retry logic and use multiple mirrors
RUN echo 'Acquire::Retries "3";' > /etc/apt/apt.conf.d/80-retries && \
    echo "deb mirror://mirrors.ubuntu.com/mirrors.txt jammy main restricted universe multiverse" > /etc/apt/sources.list && \
    echo "deb mirror://mirrors.ubuntu.com/mirrors.txt jammy-updates main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb mirror://mirrors.ubuntu.com/mirrors.txt jammy-security main restricted universe multiverse" >> /etc/apt/sources.list

# Update package list and install required packages
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
        software-properties-common \
        ca-certificates \
        gnupg \
        wget \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install SUMO
RUN apt-get update && \
    add-apt-repository ppa:sumo/stable && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        sumo \
        sumo-tools \
        sumo-doc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set SUMO_HOME environment variable
ENV SUMO_HOME=/usr/share/sumo
ENV PATH="${PATH}:${SUMO_HOME}/bin"

# Set working directory
WORKDIR /workspace

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the FastAPI app to the container
COPY app /workspace/app

# Create uploads directory
RUN mkdir -p /workspace/uploads && chmod 777 /workspace/uploads

# Expose the FastAPI API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
