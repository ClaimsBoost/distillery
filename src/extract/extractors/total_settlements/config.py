"""Configuration for total settlements extractor"""

# Extractor identity
EXTRACTOR_NAME = "total_settlements"

# Metadata boost field for better chunk retrieval
BOOST_FIELD = "money"  # Boost chunks containing money/settlement amounts

# Output size for this extractor
OUTPUT_SIZE = 500  # List of settlement cases

# Number of chunks to retrieve for vector search
CHUNK_COUNT = 5  # May be scattered across site

# Search query for finding relevant chunks
SEARCH_QUERY = "settlement verdict million billion recovered won obtained secured compensation case result success story client testimonial award judgment"