# Complete System Instructions and Documentation

> **Purpose**: This document contains the complete instructions for using, configuring, and extending the Law Firm Data Extraction System. For a quick start, see the main [README](../README.md). For production setup, see the [Setup Guide](../SETUP.md).

## Law Firm Data Extraction System

A comprehensive document processing and information extraction system designed to extract 11 different types of structured data from law firm websites. The system uses RAG (Retrieval-Augmented Generation) with vector search to accurately extract various types of information including office locations, contact details, practice areas, attorney information, and business metrics from website content.

## Overview

This system processes law firm website content (stored as markdown files) and extracts 11 different types of structured data through specialized extractors. Each extractor focuses on a specific data type and uses tailored prompts and schemas to ensure accurate extraction. The system leverages modern NLP techniques including document chunking, vector embeddings, and large language models to provide accurate and consistent extraction results across all data types.

### Key Features

- **Document Embedding**: Process and embed website content into vector databases for efficient retrieval
- **Vector Search**: Use semantic search to find relevant content chunks for each extraction type
- **Modular Extractors**: 11 specialized extractors, each with dedicated prompts, schemas, and logic
- **Structured Extraction**: Extract all data types in consistent JSON format with validation
- **Multiple Database Support**: Works with both local PostgreSQL (with pgvector) and Supabase
- **Batch Processing**: Handle individual files or entire domains
- **Comprehensive Extraction**: Run all extractors at once or target specific data types
- **Testing Framework**: Built-in evaluation against ground truth data

## Extraction Types

The system includes 11 specialized extractors, each designed to extract specific types of information from law firm websites:

### 1. Office Locations (`office_locations`)
Extracts physical office addresses, including street addresses, cities, states, and postal codes.

### 2. Law Firm Confirmation (`law_firm_confirmation`)
Confirms whether the website represents a legitimate law firm and extracts basic firm identity information.

### 3. Contact Information (`contact_info`)
Extracts contact details including phone numbers, email addresses, and other contact methods.

### 4. Practice Areas (`practice_areas`)
Identifies the legal practice areas and specializations offered by the firm.

### 5. Attorney Information (`attorneys`)
Extracts information about attorneys including names, titles, credentials, and specializations.

### 6. Year Founded (`year_founded`)
Extracts the founding year or establishment date of the law firm.

### 7. Total Settlements (`total_settlements`)
Identifies settlement amounts, case results, and monetary outcomes when available.

### 8. Supported Languages (`supported_languages`)
Extracts comprehensive information about languages supported by the firm through any channel - website translations, staff capabilities, phone/call center support, interpreter services, or document translation.

### 9. Social Media (`social_media`)
Identifies social media profiles and online presence information.

### 10. Company Description (`company_description`)
Extracts descriptive information about the firm's mission, values, and overview.

### 11. States Served (`states_served`)
Determines the geographic regions, states, or jurisdictions where the firm provides services.

Each extractor follows a consistent structure with:
- **Modular Design**: Self-contained in its own directory
- **Custom Prompts**: Tailored extraction prompts in `prompt.md`
- **Schema Validation**: JSON schema for output validation in `schema.json`
- **Specialized Logic**: Extractor-specific implementation in `extractor.py`

## Architecture

The system follows a modular command-based architecture:

```
src/
├── commands/           # Command handlers for CLI operations
│   ├── embed_command.py    # Document embedding operations
│   ├── extract_command.py  # Data extraction operations (all 11 types)
│   └── test_command.py     # Testing and evaluation
├── core/               # Core configuration and utilities
│   ├── settings.py         # Pydantic-based configuration management
│   ├── prompts.py         # LLM prompt templates
│   └── storage_handler.py # File storage operations
├── database/           # Database abstraction layer
│   ├── connection.py      # Database connection management
│   └── vector_store.py    # Vector store implementations
├── embed/              # Document processing and embedding
│   ├── chunker.py         # Document chunking utilities
│   ├── embedder.py        # Vector embedding operations
│   └── pattern_detector.py # Content pattern detection
└── extract/            # Modular extraction system
    ├── enhanced_base_extractor.py  # Enhanced base extraction interface
    ├── extractor_config.py        # Extractor configuration utilities
    └── extractors/                # Individual extractor modules
        ├── office_locations/      # Office location extraction
        │   ├── extractor.py      # Extractor implementation
        │   ├── prompt.md         # Extraction prompt
        │   ├── schema.json       # JSON schema for validation
        │   └── __init__.py       # Module exports
        ├── law_firm_confirmation/ # Law firm confirmation
        ├── contact_info/          # Contact information
        ├── practice_areas/        # Practice areas
        ├── attorneys/             # Attorney information
        ├── year_founded/          # Year founded
        ├── total_settlements/     # Settlement information
        ├── supported_languages/   # Languages supported across all channels
        ├── social_media/          # Social media presence
        ├── company_description/   # Company description
        └── states_served/         # States served
```

## Installation

### Prerequisites

- Python 3.9+
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
Create a `.env` file in the project root:
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

# Embed specific domains
python main.py embed lawfirm1.com lawfirm2.com --domain

# Embed all pending domains (not yet embedded)
python main.py embed --all

# Force re-embed all domains
python main.py embed --all --force

# Force re-embedding specific domain
python main.py embed lawfirm.com --domain --force
```

**Embedding Tracking**: The system automatically tracks which pages have been embedded using the `domain_paths` table with `is_embedded` and `last_embedded_at` fields.

### 2. Extract Command

Extract specific data types or all data from embedded documents:

```bash
# Extract specific data types from domains
python main.py extract --type office_locations --domain lawfirm.com
python main.py extract --type practice_areas --domain lawfirm.com
python main.py extract --type contact_info --domain lawfirm.com

# Extract all data types at once
python main.py extract --type all --domain lawfirm.com

# Extract from multiple domains
python main.py extract --type office_locations --domain lawfirm1.com lawfirm2.com

# Extract from specific documents
python main.py extract --type office_locations doc_id_1 doc_id_2

# Save results to file
python main.py extract --type all --domain lawfirm.com --output results.json

# Use custom configuration
python main.py extract --type office_locations --config config/custom.json --domain lawfirm.com
```

#### Available Extraction Types

| Type | Description |
|------|-------------|
| `office_locations` | Physical office addresses |
| `law_firm_confirmation` | Law firm identity verification |
| `contact_info` | Phone numbers, emails, contact methods |
| `practice_areas` | Legal specializations and services |
| `attorneys` | Attorney names, titles, credentials |
| `year_founded` | Firm establishment date |
| `total_settlements` | Settlement amounts and case results |
| `supported_languages` | Languages supported across all channels |
| `social_media` | Social media profiles |
| `company_description` | Firm mission and overview |
| `states_served` | Geographic service areas |
| `all` | Run all extractors |

### Getting Combined Results

After running extractions, you can retrieve all results for a domain in a single JSON object:

```bash
# Get combined extraction results for a domain
psql -U postgres -d claimsboost -v domain="'lawfirm.com'" -t -A -f sql/get_domain_extractions.sql > output.json

# Pretty print the results
psql -U postgres -d claimsboost -v domain="'lawfirm.com'" -f sql/get_domain_extractions.sql
```

This SQL query combines the most recent extraction results for each data type into a single JSON object, making it easy to work with all extracted data together.

### 3. Test Command

Test extraction against ground truth data:

```bash
# Test a specific domain against ground truth
python main.py test-domain lawfirm.com

# Re-embed before testing
python main.py test-domain --re-embed lawfirm.com

# Run comprehensive test suite with verbose output
python main.py test --verbose

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

The system extracts data in consistent JSON structures. Here are examples for different extraction types:

### Office Locations
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
  }
}
```

### Contact Information
```json
{
  "extraction_type": "contact_info",
  "timestamp": "2024-01-15T10:30:00",
  "results": [
    {
      "target": "lawfirm.com",
      "type": "domain",
      "data": {
        "phone_numbers": ["(555) 123-4567", "(555) 987-6543"],
        "email_addresses": ["info@lawfirm.com", "contact@lawfirm.com"],
        "fax_numbers": ["(555) 123-4568"],
        "_metadata": {
          "extraction_time_seconds": 1.8,
          "timestamp": "2024-01-15T10:30:00"
        }
      }
    }
  ]
}
```

### Practice Areas
```json
{
  "extraction_type": "practice_areas",
  "timestamp": "2024-01-15T10:30:00",
  "results": [
    {
      "target": "lawfirm.com",
      "type": "domain",
      "data": {
        "practice_areas": [
          "Personal Injury",
          "Medical Malpractice",
          "Workers' Compensation",
          "Car Accidents"
        ],
        "_metadata": {
          "extraction_time_seconds": 2.1,
          "timestamp": "2024-01-15T10:30:00"
        }
      }
    }
  ]
}
```

### Combined Results (using SQL query)
```json
{
  "domain": "lawfirm.com",
  "extractions": {
    "office_locations": {
      "offices": ["123 Main Street New York, NY 10001"]
    },
    "contact_info": {
      "phone_numbers": ["(555) 123-4567"],
      "email_addresses": ["info@lawfirm.com"]
    },
    "practice_areas": {
      "practice_areas": ["Personal Injury", "Medical Malpractice"]
    },
    "attorneys": {
      "attorneys": [
        {
          "name": "John Smith",
          "title": "Senior Partner",
          "specializations": ["Personal Injury"]
        }
      ]
    },
    "law_firm_confirmation": {
      "is_law_firm": true,
      "firm_name": "Smith & Associates"
    }
  }
}
```

All extractions include metadata about processing time and timestamps, and follow consistent JSON schemas defined in each extractor's `schema.json` file.

## Database Schema

The system uses the following main table:

### document_vectors
```sql
CREATE TABLE document_vectors (
    id UUID PRIMARY KEY,
    document_id TEXT NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB,
    embedding VECTOR(768),  -- nomic-embed-text embeddings
    domain TEXT,
    domain_id VARCHAR(12),
    embedding_model TEXT DEFAULT 'nomic-embed-text',
    embedding_dimension INTEGER DEFAULT 768,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### domain_paths (with embedding tracking)
```sql
-- Existing columns plus:
is_embedded BOOLEAN DEFAULT false,
last_embedded_at TIMESTAMP WITH TIME ZONE
```

## File Structure

The system follows this organization:

```
distillery/
├── src/                    # Core application code
│   └── extract/extractors/ # 11 modular extractors
├── config/                 # Configuration files
├── sql/                    # Database setup and queries
│   ├── postgres_setup.sql  # Complete PostgreSQL setup
│   ├── supabase_setup.sql  # Complete Supabase setup
│   └── queries/            # Utility queries
│       └── get_domain_extractions.sql  # Combined results query
├── evaluation/             # Evaluation system
│   ├── scripts/           # Evaluation scripts
│   │   └── evaluate.py    # Universal evaluation script
│   ├── test_data/         # Ground truth datasets
│   │   ├── office_locations_test_set.json
│   │   └── {extraction_type}_test_set.json (for each type)
│   └── results/           # Evaluation results
│       ├── extractions/   # Raw extraction results
│       └── evaluations/   # Evaluation metrics
└── main.py               # Main CLI interface
```

## Development

### Adding New Extraction Types

1. Create a new directory in `src/extract/extractors/{new_extractor_name}/`
2. Implement the extractor class inheriting from `BaseExtractor` in `extractor.py`
3. Create the extraction prompt in `prompt.md`
4. Define the JSON schema for validation in `schema.json`
5. Add module exports in `__init__.py`
6. Update the CLI command handler in `src/commands/extract_command.py` to include the new extractor
7. Create ground truth datasets in `evaluation/test_data/`
8. Update the universal evaluator to support the new type

#### Extractor Directory Structure
```
src/extract/extractors/{new_extractor_name}/
├── extractor.py     # Main extractor implementation
├── prompt.md        # LLM prompt for extraction
├── schema.json      # JSON schema for output validation
└── __init__.py      # Module exports
```

### Testing and Evaluation

The system includes a comprehensive testing framework:

1. **Ground Truth Data**: Store test cases in `evaluation/test_data/{extraction_type}_{dataset_type}_set.json`
2. **Test Execution**: Use the `test-domain` command for individual domain testing
3. **Universal Evaluation**: Use `evaluation/scripts/evaluate.py` for comprehensive evaluation
4. **Metrics**: The system calculates precision, recall, and F1-score automatically

### Current Performance Metrics

**Office Location Extraction (Primary Reference):**
- Test Set: ~94.67% F1 Score
- Validation Set: 96.67% F1 Score (10 domains)
- Average Precision: 95%
- Average Recall: 100%

The system demonstrates strong performance across different law firm websites with consistent accuracy. While comprehensive performance metrics are being developed for all 11 extraction types, the office location extractor serves as the performance benchmark, showing reliable extraction capabilities that extend to other data types through the shared modular architecture.

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

