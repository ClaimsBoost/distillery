"""Configuration for supported languages extractor"""

# Extractor identity
EXTRACTOR_NAME = "supported_languages"

# Metadata boost field for better chunk retrieval
BOOST_FIELD = None  # No specific boost needed

# Output size for this extractor
OUTPUT_SIZE = 600  # Multiple booleans + list + support types

# Number of chunks to retrieve for vector search
CHUNK_COUNT = 4  # Increased to find more language support mentions

# Search query for finding relevant chunks
SEARCH_QUERY = "language speak spanish chinese vietnamese french german arabic russian portuguese multilingual bilingual interpreter translator hablamos espanol call center phone support website available we offer assistance"