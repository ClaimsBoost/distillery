"""Configuration for law firm confirmation extractor"""

# Extractor identity
EXTRACTOR_NAME = "law_firm_confirmation"

# Metadata boost field for better chunk retrieval
BOOST_FIELD = None  # No specific boost needed



# Output size for this extractor
OUTPUT_SIZE = 50  # Just 2 booleans

# Number of chunks to retrieve for vector search
CHUNK_COUNT = 2  # Homepage/about usually sufficient

# Search query for finding relevant chunks
SEARCH_QUERY = "law firm attorney lawyer legal practice injury accident personal injury about us"