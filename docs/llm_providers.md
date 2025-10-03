# LLM Provider Configuration

The extraction system supports multiple LLM providers. You can switch between providers without changing your code.

## Supported Providers

### Ollama (Default)
Local LLM provider using Ollama. Free to use with your own hardware.

**Configuration:**
```bash
EXTRACTION_LLM_PROVIDER=ollama
EXTRACTION_OLLAMA_MODEL=llama3.1:8b  # Required for Ollama
OLLAMA_BASE_URL=http://localhost:11434
```

### Google Gemini
Cloud-based LLM using Google's Gemini API. Pay-per-use pricing.

**Installation:**
```bash
pip install -r requirements-gemini.txt
```

**Configuration:**
```bash
EXTRACTION_LLM_PROVIDER=gemini
EXTRACTION_GEMINI_MODEL=gemini-2.5-flash  # or gemini-1.5-flash, gemini-1.5-pro
GEMINI_API_KEY=your_api_key_here  # or EXTRACTION_GEMINI_API_KEY
```

## Cost Analysis

### Gemini Pricing (2025)

| Model | Input Cost | Output Cost | Per Extraction* |
|-------|------------|-------------|-----------------|
| Gemini 1.5 Flash | $0.15/M tokens | $0.60/M tokens | ~$0.00057 |
| Gemini 1.5 Pro | $1.25/M tokens | $5.00/M tokens | ~$0.00475 |

*Based on average extraction: ~3,000 input tokens, ~200 output tokens

### Cost Estimates for Full Dataset

Assuming 1,099 domains and 11 extraction types:

- **Gemini Flash**: ~$6.89 total
- **Gemini Pro**: ~$57.40 total
- **Ollama**: $0 (local compute)

### Cost Optimization Tips

1. **Use batch processing** - 50% cost reduction with Gemini
2. **Enable context caching** - 25% cost reduction for repeated queries
3. **Choose Flash for simple extractions** - 8x cheaper than Pro
4. **Use Pro only for complex extractions** requiring higher accuracy

## Switching Providers

### Per-Extraction Override

You can override the provider for specific extractions:

```python
# In your extraction code
from src.llm import get_llm_provider

# Use Gemini for high-accuracy extraction
provider = get_llm_provider(settings, provider='gemini')

# Use Ollama for bulk processing
provider = get_llm_provider(settings, provider='ollama')
```

### Environment-based Configuration

Set different providers for different environments:

```bash
# Development
EXTRACTION_LLM_PROVIDER=ollama
EXTRACTION_OLLAMA_MODEL=llama3.1:8b

# Production (high accuracy)
EXTRACTION_LLM_PROVIDER=gemini
EXTRACTION_GEMINI_MODEL=gemini-1.5-pro

# Production (cost-optimized)
EXTRACTION_LLM_PROVIDER=gemini
EXTRACTION_GEMINI_MODEL=gemini-2.5-flash
```

## Provider Features Comparison

| Feature | Ollama | Gemini |
|---------|--------|---------|
| Cost | Free (local) | Pay-per-use |
| Speed | Depends on hardware | Fast (cloud) |
| Scalability | Limited by hardware | Unlimited |
| JSON Schema Support | ✓ | ✓ |
| Streaming | ✓ | ✓ |
| Token Counting | ✓ | ✓ (precise) |
| Cost Tracking | N/A | ✓ |
| Batch Processing | Manual | Built-in (50% discount) |

## Monitoring Costs

When using Gemini, costs are automatically tracked:

```bash
# Enable cost tracking
EXTRACTION_TRACK_COSTS=true

# Costs are logged per extraction:
[law_firm_confirmation] Estimated cost: $0.000432
```

Costs are also stored in the extraction results:
```json
{
  "is_law_firm": true,
  "_cost_estimate": 0.000432
}
```

## Testing Provider Configuration

Run the test script to verify your configuration:

```bash
python test_provider_switching.py
```

This will test:
- Ollama connectivity
- Gemini API key (if configured)
- Provider switching
- Extraction integration