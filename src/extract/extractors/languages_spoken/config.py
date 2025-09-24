"""Configuration for languages spoken extractor"""

# Extractor identity
EXTRACTOR_NAME = "languages_spoken"

# Metadata boost field for better chunk retrieval
BOOST_FIELD = None  # No specific boost needed



# Output size for this extractor
OUTPUT_SIZE = 500  # Multiple booleans + list

# Number of chunks to retrieve for vector search
CHUNK_COUNT = 3

# Search query for finding relevant chunks
SEARCH_QUERY = "language speak spanish chinese vietnamese french german arabic russian portuguese multilingual bilingual interpreter translator hablamos espanol"