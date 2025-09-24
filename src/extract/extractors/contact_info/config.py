"""Configuration for contact info extractor"""

# Extractor identity
EXTRACTOR_NAME = "contact_info"

# Metadata boost field for better chunk retrieval
BOOST_FIELD = "contact"  # Boost chunks containing emails or phone numbers

# Output size for this extractor
OUTPUT_SIZE = 200  # Contact details

# Number of chunks to retrieve for vector search
CHUNK_COUNT = 3

# Search query for finding relevant chunks
SEARCH_QUERY = "phone call contact email fax 24/7 24 hours emergency hotline toll free 1-800 after hours available anytime always available weekend"