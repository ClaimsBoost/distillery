"""Configuration for states served extractor"""

# Extractor identity
EXTRACTOR_NAME = "states_served"

# Metadata boost field for better chunk retrieval
BOOST_FIELD = None  # No specific boost needed



# Output size for this extractor
OUTPUT_SIZE = 200  # States list + booleans

# Number of chunks to retrieve for vector search
CHUNK_COUNT = 3

# Search query for finding relevant chunks
SEARCH_QUERY = "states served licensed practice nationwide nationwide coverage service areas jurisdiction bar admission admitted multi-state regional tri-state"