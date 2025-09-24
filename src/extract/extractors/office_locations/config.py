"""Configuration for office locations extractor"""

# Extractor identity
EXTRACTOR_NAME = "office_locations"

# Metadata boost field for better chunk retrieval
BOOST_FIELD = "addresses"  # Boost chunks containing addresses

# Output size for this extractor
OUTPUT_SIZE = 500  # List of addresses

# Number of chunks to retrieve for vector search
CHUNK_COUNT = 4

# Search query for finding relevant chunks
SEARCH_QUERY = "office location address street city state zip where find us directions map contact headquarters branch main office satellite"