# Distillery - Law Firm Data Extraction System

A comprehensive document processing and information extraction system that extracts 11 different types of structured data from law firm websites using RAG (Retrieval-Augmented Generation) technology.

## Documentation

- **[Setup Guide](SETUP.md)** - Production setup and GPU configuration
- **[Full Documentation](docs/README.md)** - Complete system documentation and usage guide
- **[Project Instructions](docs/CLAUDE.md)** - Development instructions and guidelines

## Quick Start

```bash
# Run automated setup
./setup.sh

# Configure environment
cp .env.example .env
# Edit .env with your database credentials and settings

# Activate virtual environment
source venv/bin/activate

# Embed domain content for processing
python main.py embed --domain example.com

# Extract specific data type
python main.py extract --domain example.com --type contact_info

# Extract all data types at once
python main.py extract --domain example.com --type all

# Get combined extraction results
psql -U your_user -d your_database -v domain="'example.com'" -t -A -f sql/get_domain_extractions.sql > output.json
```

For detailed setup instructions, see the [Setup Guide](SETUP.md).
For complete documentation, see the [full documentation](docs/README.md).