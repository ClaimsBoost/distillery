#!/bin/bash

set -e

echo "========================================="
echo "Law Firm Extraction System Setup Script"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check Python version
print_status "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    if [ $(echo "$PYTHON_VERSION >= 3.9" | bc) -eq 1 ]; then
        print_status "Python $PYTHON_VERSION detected"
    else
        print_error "Python 3.9+ required, found $PYTHON_VERSION"
        exit 1
    fi
else
    print_error "Python 3 not found"
    exit 1
fi

# Check for GPU/CUDA
print_status "Checking for NVIDIA GPU..."
if command -v nvidia-smi &> /dev/null; then
    GPU_INFO=$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader)
    print_status "GPU detected: $GPU_INFO"

    # Check CUDA version
    if command -v nvcc &> /dev/null; then
        CUDA_VERSION=$(nvcc --version | grep "release" | awk '{print $5}' | cut -d',' -f1)
        print_status "CUDA $CUDA_VERSION detected"
    else
        print_warning "CUDA not found. GPU acceleration may not work optimally."
        print_warning "Install CUDA 11.8+ from: https://developer.nvidia.com/cuda-downloads"
    fi
else
    print_warning "No NVIDIA GPU detected. System will use CPU for processing."
fi

# Create virtual environment
print_status "Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip -q

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Check for Ollama
print_status "Checking for Ollama installation..."
if command -v ollama &> /dev/null; then
    print_status "Ollama is installed"

    # Check if Ollama is running
    if pgrep -x "ollama" > /dev/null; then
        print_status "Ollama service is running"
    else
        print_warning "Ollama is installed but not running"
        print_status "Starting Ollama service..."
        ollama serve &> /dev/null &
        sleep 3
    fi

    # Pull required models
    print_status "Pulling required Ollama models..."
    print_status "Pulling llama3.1:8b (this may take a while)..."
    ollama pull llama3.1:8b
    print_status "Pulling nomic-embed-text..."
    ollama pull nomic-embed-text
else
    print_error "Ollama not found. Please install from: https://ollama.ai"
    echo "Installation command: curl -fsSL https://ollama.ai/install.sh | sh"
    exit 1
fi

# Check PostgreSQL
print_status "Checking PostgreSQL installation..."
if command -v psql &> /dev/null; then
    print_status "PostgreSQL client found"
else
    print_warning "PostgreSQL client not found"
    echo "Please install PostgreSQL: https://www.postgresql.org/download/"
fi

# Setup environment file
print_status "Setting up environment configuration..."
if [ ! -f "config/.env" ]; then
    if [ -f "config/.env.example" ]; then
        cp config/.env.example config/.env
        print_status "Created config/.env from config/.env.example"
        print_warning "Please edit config/.env with your database credentials and API keys"
    else
        print_error "config/.env.example not found. Please check your installation."
    fi
else
    print_status "config/.env file already exists"
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p results
mkdir -p logs
mkdir -p data
print_status "Directories created"

# Database setup prompt
echo ""
print_warning "Database Setup Required:"
echo "1. Ensure PostgreSQL is running with pgvector extension"
echo "2. Create your database and run the SQL setup:"
echo "   psql -U your_user -d your_database -f sql/get_domain_extractions.sql"
echo "3. Configure your Supabase or local PostgreSQL connection in config/.env"
echo ""

# GPU optimization settings for RTX 3090
if [[ "$GPU_INFO" == *"3090"* ]] || [[ "$GPU_INFO" == *"RTX 3090"* ]]; then
    print_status "RTX 3090 detected. Recommended GPU optimization settings..."
    echo ""
    echo "Add these to your config/.env file for RTX 3090 (24GB VRAM):"
    echo "----------------------------------------"
    echo "# GPU Optimizations"
    echo "EXTRACTION_CHUNK_SIZE=8000"
    echo "EXTRACTION_NUM_CTX=16384"
    echo "EXTRACTION_BATCH_SIZE=10"
    echo "# Note: OLLAMA_NUM_GPU and OLLAMA_GPU_LAYERS can also be set"
    echo "# for GPU acceleration with Ollama"
    echo "----------------------------------------"
fi

echo ""
print_status "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Configure your config/.env file with database credentials"
echo "3. Setup your database with the provided SQL scripts"
echo "4. Run: python main.py --help to see available commands"
echo ""
echo "For detailed setup instructions, see SETUP.md"