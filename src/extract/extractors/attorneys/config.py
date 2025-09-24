"""Configuration for attorneys extractor"""

# Extractor identity
EXTRACTOR_NAME = "attorneys"

# Metadata boost field for better chunk retrieval
BOOST_FIELD = None  # No specific boost needed



# Output size for this extractor
OUTPUT_SIZE = 1500  # Multiple attorney profiles

# Number of chunks to retrieve for vector search
CHUNK_COUNT = 4  # Multiple attorney pages

# Search query for finding relevant chunks
SEARCH_QUERY = "attorney lawyer partner associate counsel team staff bio biography"