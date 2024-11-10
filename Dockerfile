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

# Install FastAPI and Uvicorn
RUN pip install fastapi uvicorn python-multipart

# Set SUMO_HOME environment variable
ENV SUMO_HOME=/usr/share/sumo

# Set working directory
WORKDIR /workspace

# Copy the FastAPI app to the container
COPY app /workspace/app

# Expose the FastAPI API port
EXPOSE 8000

# Run FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
