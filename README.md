# Distillery - Law Firm Data Extraction System

A powerful document processing and information extraction system for law firm websites.

## Documentation

- **[Full Documentation](docs/README.md)** - Complete system documentation, installation, and usage guide
- **[Project Instructions](docs/CLAUDE.md)** - Development instructions and guidelines
- **[Configuration Guide](docs/configuration-refactoring-guide.md)** - Configuration system architecture and best practices

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp config/.env.example config/.env
# Edit config/.env with your credentials

# Check system status
python main.py status

# View extraction statistics
python main.py stats

# Extract law firm data
python main.py extract domain.com --type law_firm_confirmation --domain
```

For detailed instructions, see the [full documentation](docs/README.md).