# Law Firm Office Location Extraction System

A powerful document processing and information extraction system specifically designed to identify office locations from law firm websites. The system uses RAG (Retrieval-Augmented Generation) with vector search to accurately extract office addresses from website content.

## Overview

This system processes law firm website content (stored as markdown files) and extracts structured office location data including street addresses, cities, states, and other location details. It leverages modern NLP techniques including document chunking, vector embeddings, and large language models to provide accurate extraction results.

### Key Features

- **Document Embedding**: Process and embed website content into vector databases for efficient retrieval
- **Vector Search**: Use semantic search to find relevant content chunks containing office information
- **Structured Extraction**: Extract office locations in consistent JSON format
- **Multiple Database Support**: Works with both local PostgreSQL (with pgvector) and Supabase
- **Batch Processing**: Handle individual files or entire domains
- **Testing Framework**: Built-in evaluation against ground truth data

## Architecture

The system follows a modular command-based architecture:

```
src/
├── commands/           # Command handlers for CLI operations
│   ├── embed_command.py    # Document embedding operations
│   ├── extract_command.py  # Office extraction operations
│   └── test_command.py     # Testing and evaluation
├── core/               # Core configuration and utilities
│   ├── config_manager.py   # Configuration management
│   ├── env_config.py      # Environment configuration
│   ├── prompts.py         # LLM prompt templates
│   └── storage_handler.py # File storage operations
├── database/           # Database abstraction layer
│   ├── connection.py      # Database connection management
│   └── vector_store.py    # Vector store implementations
├── embed/              # Document processing and embedding
│   ├── chunker.py         # Document chunking utilities
│   ├── embedder.py        # Vector embedding operations
│   └── pattern_detector.py # Content pattern detection
└── extract/            # Extraction logic
    ├── base_extractor.py  # Base extraction interface
    └── office_extractor.py # Office location extraction
```

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL with pgvector extension (for local development)
- Ollama with required models (see Configuration section)
- Supabase account (for cloud storage and vector database)

### Setup

1. **Clone and install dependencies**:
```bash
git clone <repository-url>
cd distillery
pip install -r requirements.txt
```

2. **Database Setup**:

For local PostgreSQL with pgvector:
```bash
# Install pgvector extension
sudo apt-get install postgresql-14-pgvector  # Ubuntu/Debian
# or
brew install pgvector  # macOS

# Create database and run setup
createdb law_firm_extraction
psql law_firm_extraction < src/database/local_postgres_setup.sql
```

For Supabase:
```bash
# Run the setup SQL in your Supabase SQL editor
cat src/database/supabase_setup.sql
```

3. **Environment Variables**:
Create a `.env` file in the `config/` directory:
```bash
# Database connections
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
LOCAL_DATABASE_URL=postgresql://user:pass@localhost:5432/law_firm_extraction

# Ollama configuration
OLLAMA_BASE_URL=http://localhost:11434

# Environment setting
ENVIRONMENT=local  # or 'prod'
```

4. **Install Ollama models**:
```bash
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

## Configuration

The system uses JSON configuration files in the `config/` directory:

### config.local.json
```json
{
  "extraction": {
    "chunk_size": 5000,
    "chunk_overlap": 500,
    "model_type": "llama3.1:8b",
    "embedder_type": "nomic-embed-text",
    "temperature": 0.0,
    "seed": 42,
    "num_ctx": 8192,
    "k_chunks": 3,
    "similarity_threshold": 0.7,
    "retry_attempts": 3
  },
  "ollama": {
    "base_url": "http://localhost:11434"
  }
}
```

### Configuration Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `chunk_size` | Size of document chunks in characters | 5000 |
| `chunk_overlap` | Overlap between adjacent chunks | 500 |
| `model_type` | Ollama model for extraction | llama3.1:8b |
| `embedder_type` | Embedding model | nomic-embed-text |
| `temperature` | LLM temperature (0.0-2.0) | 0.0 |
| `num_ctx` | Ollama context window size (place in options) | 8192 |
| `seed` | Seed for reproducible results | 42 |
| `k_chunks` | Number of chunks to retrieve | 3 |
| `similarity_threshold` | Minimum similarity score | 0.7 |
| `retry_attempts` | Number of extraction retries | 3 |

## CLI Usage

The system provides three main commands plus a universal evaluation script:

### 1. Embed Command

Process and embed documents into the vector database:

```bash
# Embed individual files
python main.py embed path/to/file1.md path/to/file2.md

# Embed entire domains
python main.py embed --domain lawfirm1.com lawfirm2.com

# Force re-embedding (overwrite existing)
python main.py embed --domain --force lawfirm.com

# Use custom configuration
python main.py embed --config config/custom.json --domain lawfirm.com
```

### 2. Extract Command

Extract office locations from embedded documents:

```bash
# Extract from domains
python main.py extract --type office_locations --domain lawfirm.com anotherfirm.com

# Extract from specific documents
python main.py extract --type office_locations doc_id_1 doc_id_2

# Save results to file
python main.py extract --type office_locations --domain lawfirm.com --output results.json

# Use custom configuration
python main.py extract --type office_locations --config config/custom.json --domain lawfirm.com
```

### 3. Test Command

Test extraction against ground truth data:

```bash
# Test a domain against ground truth
python main.py test-domain lawfirm.com

# Re-embed before testing
python main.py test-domain --re-embed lawfirm.com

# Use custom configuration
python main.py test-domain --config config/custom.json lawfirm.com
```

### 4. Universal Evaluation Script

Evaluate extraction results against ground truth datasets using the universal evaluation script:

```bash
# Evaluate office locations using test set (default)
python evaluation/scripts/evaluate.py evaluation/results/extractions/office_extraction.json

# Evaluate using validation set
python evaluation/scripts/evaluate.py --dataset validation evaluation/results/extractions/office_extraction.json

# Evaluate different extraction types
python evaluation/scripts/evaluate.py --type phone_numbers phone_extraction.json
python evaluation/scripts/evaluate.py --type email_addresses email_extraction.json
python evaluation/scripts/evaluate.py --type practice_areas practice_extraction.json
python evaluation/scripts/evaluate.py --type attorney_names attorney_extraction.json

# Evaluate specific domains only
python evaluation/scripts/evaluate.py --domains 866attylaw.com 1emslegal.com extraction.json

# Save output to custom file and skip database
python evaluation/scripts/evaluate.py --output custom_results.json --no-db extraction.json

# Run quietly (less verbose output)
python evaluation/scripts/evaluate.py --quiet extraction.json
```

#### Evaluation Options

| Option | Description | Default |
|--------|-------------|----------|
| `--type` | Type of extraction to evaluate | office_locations |
| `--dataset` | Dataset to use (test/validation) | test |
| `--domains` | Specific domains to evaluate | All domains |
| `--output` | Custom output file | Auto-generated |
| `--no-db` | Skip saving to database | False |
| `--quiet` | Reduce output verbosity | False |

**Automatic File Naming**: The evaluation script automatically saves results to `evaluation/results/evaluations/{extraction_type}_evaluation_{timestamp}.json` unless a custom output file is specified.

## Output Format

The system extracts office locations in the following JSON structure:

```json
{
  "extraction_type": "office_locations",
  "timestamp": "2024-01-15T10:30:00",
  "results": [
    {
      "target": "lawfirm.com",
      "type": "domain",
      "data": {
        "offices": [
          "123 Main Street New York, NY 10001",
          "456 Oak Ave Suite 200 Los Angeles, CA 90210"
        ],
        "_metadata": {
          "extraction_time_seconds": 2.45,
          "timestamp": "2024-01-15T10:30:00"
        }
      }
    }
  ],
  "summary": {
    "total_targets": 1,
    "successful": 1
  },
  "config": {
    "model": "llama3.1:8b",
    "temperature": 0.1,
    "k_chunks": 5
  }
}
```

## Database Schema

The system uses the following main table:

### document_vectors
```sql
CREATE TABLE document_vectors (
    id SERIAL PRIMARY KEY,
    document_id TEXT NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB,
    embedding VECTOR(768),
    domain TEXT,
    domain_id TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(document_id, content)
);
```

## File Structure

The system follows this organization:

```
distillery/
├── src/                    # Core application code
├── config/                 # Configuration files
├── evaluation/             # Evaluation system
│   ├── scripts/           # Evaluation scripts
│   │   └── evaluate.py    # Universal evaluation script
│   ├── test_data/         # Ground truth datasets
│   │   ├── office_locations_test_set.json
│   │   └── office_locations_validation_set.json
│   └── results/           # Evaluation results
│       ├── extractions/   # Raw extraction results
│       └── evaluations/   # Evaluation metrics
├── prompts/               # LLM prompt templates
└── main.py               # Main CLI interface
```

## Development

### Adding New Extraction Types

1. Create a new extractor class inheriting from `BaseExtractor`
2. Add the extraction logic in `src/extract/`
3. Update the CLI command handler in `src/commands/extract_command.py`
4. Add corresponding prompts in `prompts/extraction/`
5. Create ground truth datasets in `evaluation/test_data/`
6. Update the universal evaluator to support the new type

### Testing and Evaluation

The system includes a comprehensive testing framework:

1. **Ground Truth Data**: Store test cases in `evaluation/test_data/{extraction_type}_{dataset_type}_set.json`
2. **Test Execution**: Use the `test-domain` command for individual domain testing
3. **Universal Evaluation**: Use `evaluation/scripts/evaluate.py` for comprehensive evaluation
4. **Metrics**: The system calculates precision, recall, and F1-score automatically

### Current Performance Metrics

**Office Location Extraction:**
- Test Set: ~94.67% F1 Score
- Validation Set: 96.67% F1 Score (10 domains)
- Average Precision: 95%
- Average Recall: 100%

The system demonstrates strong performance across different law firm websites with consistent accuracy in extracting office addresses.

### Ground Truth Format

Datasets use consistent format across extraction types:

```json
{
  "metadata": {
    "created_at": "2024-12-30T12:00:00",
    "created_by": "manual_extraction_from_markdown",
    "purpose": "office_location_extraction_evaluation",
    "total_samples": 10
  },
  "samples": [
    {
      "domain": "example-law.com",
      "firm_name": "Example Law Firm",
      "ground_truth": {
        "offices": [
          "123 Main Street, New York, NY 10001",
          "456 Oak Avenue, Suite 200, Los Angeles, CA 90210"
        ]
      }
    }
  ]
}
```

**Important Domain Format**: 
- Use dots in domain names (example.com) in ground truth data
- File paths and folders use underscores (example_com)
- The system automatically handles format conversion

## Performance Optimization

### Vector Search Optimization
- The system uses metadata boosting to prioritize chunks containing addresses
- Address-containing chunks are sorted first, then by semantic similarity
- Local PostgreSQL supports advanced boosting queries
- Domain format consistency: dots in queries, underscores only for file paths

### Configuration Tuning
- **chunk_size**: Larger chunks capture more context but may dilute relevant information
- **num_ctx**: Context window size - increase for longer documents (default: 8192)
- **k_chunks**: More chunks provide better coverage but increase processing time
- **temperature**: Set to 0 for deterministic results, higher for creativity
- **seed**: Use consistent seed value for reproducible results
- **similarity_threshold**: Adjust based on your content quality and requirements

### Key Improvements
- **Context Window**: System now properly handles contexts beyond 4096 tokens
- **Domain Consistency**: Automatic conversion between dots and underscores
- **Reproducibility**: Seed parameter ensures consistent results
- **Universal Evaluation**: Single script handles multiple extraction types

## Troubleshooting

### Common Issues

1. **"No database configuration found"**
   - Ensure either `LOCAL_DATABASE_URL` or Supabase credentials are set
   - Check your `.env` file is in the `config/` directory

2. **"Ollama connection failed"**
   - Verify Ollama is running: `ollama serve`
   - Check the base URL in configuration matches your Ollama instance
   - Ensure required models are downloaded

3. **"No files found for domain"**
   - Verify markdown files exist in Supabase storage under the correct path
   - Check domain format: use dots (example.com) not underscores
   - Check storage bucket and base path configuration
   - Use the embed command to process files first

4. **Low extraction accuracy**
   - Increase `k_chunks` to retrieve more relevant content
   - Adjust `chunk_size` to better capture complete address information
   - Review and refine extraction prompts
   - Check ground truth data quality

### Debug Mode

Enable detailed logging by setting the logging level:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Monitoring

Monitor extraction performance with:
- Extraction time (included in results metadata)
- Vector search relevance scores
- Chunk retrieval patterns
- LLM token usage and response times

## Contributing

1. Follow the modular architecture pattern
2. Add comprehensive tests for new features
3. Update configuration documentation
4. Include example usage in docstrings
5. Follow existing code style and naming conventions

