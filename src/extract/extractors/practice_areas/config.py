"""Configuration for practice areas extractor"""

# Extractor identity
EXTRACTOR_NAME = "practice_areas"

# Metadata boost field for better chunk retrieval
BOOST_FIELD = None  # No specific boost needed



# Output size for this extractor
OUTPUT_SIZE = 500  # List of practice areas

# Number of chunks to retrieve for vector search
CHUNK_COUNT = 4

# Search query for finding relevant chunks
SEARCH_QUERY = "practice areas services we handle cases legal services personal injury medical malpractice wrongful death product liability premises liability motor vehicle workplace"