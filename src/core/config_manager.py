"""
Configuration management for RAG extraction system
"""

from typing import List, Optional
from dataclasses import dataclass, field
from enum import Enum
import os


class ModelType(Enum):
    """Available LLM models"""
    LLAMA3_1_8B = "llama3.1:8b"
    

class EmbedderType(Enum):
    """Available embedding models"""
    NOMIC_EMBED = "nomic-embed-text"


@dataclass
class ExtractionConfig:
    """Configuration for RAG extraction pipeline"""
    
    # Chunking parameters
    chunk_size: int
    chunk_overlap: int
    
    # Model parameters
    model_type: str
    embedder_type: str
    temperature: float
    top_p: float
    max_tokens: int
    seed: int  # For reproducibility
    
    # Retrieval parameters
    k_chunks: int  # Number of chunks to retrieve
    similarity_threshold: float
    
    # Processing parameters
    batch_size: int
    retry_attempts: int
    
    # Feature flags (planned enhancements - not yet implemented)
    use_reranking: bool  # TODO: Implement chunk reranking with cross-encoder
    use_query_expansion: bool  # TODO: Implement query expansion for better retrieval
    extract_confidence_scores: bool
    
    # Supabase settings (from environment)
    supabase_url: str = field(default_factory=lambda: os.environ.get('SUPABASE_URL', ''))
    supabase_key: str = field(default_factory=lambda: os.environ.get('SUPABASE_KEY', ''))
    
    # Ollama settings
    ollama_base_url: str = field(default_factory=lambda: os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434'))
    num_ctx: Optional[int] = None  # Context window size (optional, uses Ollama default if not set)
    
    def validate(self) -> List[str]:
        """
        Validate configuration parameters
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Validate chunk parameters
        if self.chunk_size < 100:
            errors.append("chunk_size must be at least 100")
        if self.chunk_overlap >= self.chunk_size:
            errors.append("chunk_overlap must be less than chunk_size")
        if self.chunk_overlap < 0:
            errors.append("chunk_overlap must be non-negative")
        
        # Validate model parameters
        if self.temperature < 0 or self.temperature > 2:
            errors.append("temperature must be between 0 and 2")
        if self.top_p < 0 or self.top_p > 1:
            errors.append("top_p must be between 0 and 1")
        if self.max_tokens < 100:
            errors.append("max_tokens must be at least 100")
        
        # Validate retrieval parameters
        if self.k_chunks < 1:
            errors.append("k_chunks must be at least 1")
        if self.similarity_threshold < 0 or self.similarity_threshold > 1:
            errors.append("similarity_threshold must be between 0 and 1")
        
        # Validate environment settings
        if not self.supabase_url:
            errors.append("SUPABASE_URL environment variable not set")
        if not self.supabase_key:
            errors.append("SUPABASE_KEY environment variable not set")
        
        return errors


    

    

    
   
    
   
    