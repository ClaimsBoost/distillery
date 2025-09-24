"""Configuration for year founded extractor"""

# Extractor identity
EXTRACTOR_NAME = "year_founded"

# Metadata boost field for better chunk retrieval
BOOST_FIELD = None  # No specific boost needed



# Output size for this extractor
OUTPUT_SIZE = 50  # Single year value

# Number of chunks to retrieve for vector search
CHUNK_COUNT = 1  # Usually on about/history pages

# Search query for finding relevant chunks
SEARCH_QUERY = "founded established began started year history since inception opened first 1970s 1980s 1990s 2000s experience serving"