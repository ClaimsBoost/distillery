"""Configuration for social media extractor"""

# Extractor identity
EXTRACTOR_NAME = "social_media"

# Metadata boost field for better chunk retrieval
BOOST_FIELD = None  # No specific boost needed



# Output size for this extractor
OUTPUT_SIZE = 500  # Multiple URL fields

# Number of chunks to retrieve for vector search
CHUNK_COUNT = 3

# Search query for finding relevant chunks
SEARCH_QUERY = "social media facebook twitter linkedin instagram youtube contact us footer follow us connect links profiles justia avvo martindale lawyers.com nolo"