"""Configuration for company description extractor"""

# Extractor identity
EXTRACTOR_NAME = "company_description"

# Metadata boost field for better chunk retrieval
BOOST_FIELD = None  # No specific boost needed



# Output size for this extractor
OUTPUT_SIZE = 200  # One sentence description

# Number of chunks to retrieve for vector search
CHUNK_COUNT = 3

# Search query for finding relevant chunks
SEARCH_QUERY = "about us our firm company overview history mission vision values who we are law firm practice description specialization experience founding established"