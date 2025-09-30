# Production Setup Guide

This guide provides comprehensive instructions for setting up the Law Firm Extraction System on a production environment with GPU acceleration.

## Table of Contents
- [System Requirements](#system-requirements)
- [Quick Setup](#quick-setup)
- [Detailed Installation](#detailed-installation)
- [GPU Configuration (RTX 3090)](#gpu-configuration-rtx-3090)
- [Database Setup](#database-setup)
- [Configuration](#configuration)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- **OS**: Ubuntu 20.04+ / macOS 12+ / Windows WSL2
- **Python**: 3.9+
- **RAM**: 16GB minimum, 32GB recommended
- **Storage**: 50GB+ SSD space for models and data
- **Database**: PostgreSQL 14+ with pgvector extension

### GPU Requirements (Recommended)
- **NVIDIA GPU**: RTX 3090 or better (24GB VRAM)
- **CUDA**: 11.8+ (for optimal Ollama performance)
- **Driver**: NVIDIA Driver 515+

## Quick Setup

For a quick automated setup, run:

```bash
# Clone the repository
git clone https://github.com/your-org/distillery.git
cd distillery

# Run the setup script
chmod +x setup.sh
./setup.sh

# Configure environment
cp config/.env.example config/.env
# Edit config/.env with your settings

# Activate virtual environment
source venv/bin/activate

# Run the application
python main.py --help
```

## Detailed Installation

### 1. System Dependencies

#### Ubuntu/Debian
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and development tools
sudo apt install -y python3.9 python3.9-venv python3-pip build-essential

# Install PostgreSQL and pgvector
sudo apt install -y postgresql postgresql-contrib
sudo apt install -y postgresql-14-pgvector

# Install CUDA (for GPU support)
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt update
sudo apt install -y cuda-11-8
```

#### macOS
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.9

# Install PostgreSQL with pgvector
brew install postgresql@14
brew install pgvector
```

### 2. Ollama Installation

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve &

# Pull required models
ollama pull llama3.1:8b
ollama pull nomic-embed-text

# Verify installation
ollama list
```

### 3. Python Environment Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/macOS
# OR
venv\Scripts\activate  # On Windows

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### 4. Database Setup

#### Local PostgreSQL
```bash
# Create database and user
sudo -u postgres psql
```

```sql
CREATE DATABASE law_firm_extraction;
CREATE USER extraction_user WITH ENCRYPTED PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE law_firm_extraction TO extraction_user;

-- Enable pgvector extension
\c law_firm_extraction
CREATE EXTENSION IF NOT EXISTS vector;
```

#### Supabase Setup
1. Create a project at [supabase.com](https://supabase.com)
2. Enable pgvector extension in the SQL Editor:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
3. Run the schema setup:
   ```bash
   psql "postgresql://[user]:[password]@[host]/postgres" -f sql/get_domain_extractions.sql
   ```

## GPU Configuration (RTX 3090)

### CUDA Setup Verification
```bash
# Check NVIDIA driver
nvidia-smi

# Check CUDA version
nvcc --version

# Monitor GPU usage during processing
watch -n 1 nvidia-smi
```

### Optimized Settings for RTX 3090 (24GB VRAM)

Add these to your `.env` file:

```env
# GPU Optimizations
EXTRACTION_CHUNK_SIZE=8000
EXTRACTION_NUM_CTX=16384
EXTRACTION_BATCH_SIZE=10

# Ollama GPU settings (uncomment to enable)
# OLLAMA_NUM_GPU=1
# OLLAMA_GPU_LAYERS=35
```

## Configuration

### Environment Variables

Create a `.env` file in the config directory:

```env
# Environment Configuration
ENVIRONMENT=local  # Options: 'local' or 'production'

# Database Configuration
# For Local PostgreSQL
LOCAL_DATABASE_URI=postgresql://username:password@localhost:5432/law_firm_extraction

# For Supabase (production/cloud)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key
SUPABASE_DATABASE_URI=postgresql://username:password@host:5432/database

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
EXTRACTION_MODEL_TYPE=llama3.1:8b
EXTRACTION_EMBEDDER_TYPE=nomic-embed-text

# Processing Configuration
EXTRACTION_TEMPERATURE=0.0
EXTRACTION_CHUNK_SIZE=8000
EXTRACTION_NUM_CTX=16384
EXTRACTION_BATCH_SIZE=10

# Extraction Configuration
EXTRACTION_SIMILARITY_THRESHOLD=0.7
EXTRACTION_K_CHUNKS=3
EXTRACTION_RETRY_ATTEMPTS=3

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/extraction.log
```

## Verification

### 1. Test Ollama Connection
```bash
# Check if models are available
curl http://localhost:11434/api/tags

# Test model inference
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.1:8b",
  "prompt": "Hello, world!"
}'
```

### 2. Test Database Connection
```bash
python -c "
from src.database.vector_store import VectorStore
store = VectorStore()
print('Database connection successful!')
"
```

### 3. Run Test Extraction
```bash
# Test with a single domain
python main.py extract --domain example.com --type contact_info

# Run comprehensive tests
python main.py test --verbose
```

## Troubleshooting

### Common Issues

#### CUDA/GPU Not Detected
```bash
# Check NVIDIA driver installation
lspci | grep -i nvidia

# Reinstall CUDA toolkit
sudo apt install --reinstall cuda-11-8

# Set environment variables
export PATH=/usr/local/cuda-11.8/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:$LD_LIBRARY_PATH
```

#### Ollama Connection Issues
```bash
# Check if Ollama is running
ps aux | grep ollama

# Restart Ollama service
pkill ollama
ollama serve &

# Check Ollama logs
journalctl -u ollama -f
```

#### Out of Memory Errors
- Reduce `EXTRACTION_CHUNK_SIZE` in .env
- Decrease `EXTRACTION_BATCH_SIZE`
- Lower `OLLAMA_GPU_LAYERS` if GPU memory is exhausted

#### Database Connection Errors
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -U extraction_user -d law_firm_extraction -h localhost

# Check pgvector installation
psql -U extraction_user -d law_firm_extraction -c "SELECT * FROM pg_extension WHERE extname = 'vector';"
```

### Performance Tuning

#### For Large-Scale Processing
```env
# Increase batch sizes for better throughput
EXTRACTION_BATCH_SIZE=20

# Adjust chunk size based on available VRAM
EXTRACTION_CHUNK_SIZE=10000

# Enable parallel processing
PERF_MAX_WORKERS=4
```

#### For Limited Resources
```env
# Reduce memory usage
EXTRACTION_BATCH_SIZE=5
EXTRACTION_CHUNK_SIZE=4000

# Use smaller context window
EXTRACTION_NUM_CTX=8192
```

## Production Deployment Checklist

- [ ] GPU drivers and CUDA installed
- [ ] Ollama service running with required models
- [ ] PostgreSQL with pgvector configured
- [ ] Python environment with all dependencies
- [ ] Environment variables configured
- [ ] Database schema initialized
- [ ] Test extraction successful
- [ ] Monitoring and logging configured
- [ ] Backup strategy in place
- [ ] Security hardening completed

## Security Considerations

1. **Environment Variables**: Never commit `.env` files to version control
2. **Database Credentials**: Use strong passwords and rotate regularly
3. **API Keys**: Store securely and limit scope
4. **Network**: Use firewall rules to restrict database access
5. **Updates**: Keep all dependencies and system packages updated

## Support

For issues or questions:
1. Check the [documentation](docs/README.md)
2. Review [troubleshooting](#troubleshooting) section
3. Open an issue on GitHub
4. Contact support at support@example.com