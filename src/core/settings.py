"""
Centralized configuration management using Pydantic Settings.
Following best practices for type-safe, validated configuration.
"""

from pathlib import Path
from typing import Optional, Literal
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    
    local_database_uri: Optional[str] = Field(None, env='LOCAL_DATABASE_URI')
    supabase_database_uri: Optional[str] = Field(None, env='SUPABASE_DATABASE_URI')
    supabase_url: Optional[str] = Field(None, env='SUPABASE_URL')
    supabase_key: Optional[str] = Field(None, env='SUPABASE_KEY')
    
    class Config:
        env_prefix = ''


class StorageSettings(BaseSettings):
    """Storage configuration settings for Supabase."""

    bucket: str = Field('law-firm-websites', env='STORAGE_BUCKET')
    base_path: str = Field('', env='STORAGE_BASE_PATH')
    
    class Config:
        env_prefix = 'STORAGE_'




class ExtractionSettings(BaseSettings):
    """Extraction pipeline configuration settings."""

    # LLM Provider settings
    llm_provider: str = Field('ollama', env='EXTRACTION_LLM_PROVIDER')  # ollama or gemini

    # Model settings for each provider
    ollama_model: Optional[str] = Field(None, env='EXTRACTION_OLLAMA_MODEL')
    gemini_model: str = Field('gemini-1.5-flash', env='EXTRACTION_GEMINI_MODEL')
    gemini_api_key: Optional[str] = Field(None, env='EXTRACTION_GEMINI_API_KEY')

    # Chunking parameters
    chunk_size: int = Field(..., env='EXTRACTION_CHUNK_SIZE')
    chunk_overlap: int = Field(..., env='EXTRACTION_CHUNK_OVERLAP')

    # Embedder settings
    embedder_type: str = Field(..., env='EXTRACTION_EMBEDDER_TYPE')

    # Generation parameters (used by both providers)
    temperature: float = Field(..., env='EXTRACTION_TEMPERATURE')
    top_p: float = Field(..., env='EXTRACTION_TOP_P')

    # Cost tracking
    track_costs: bool = Field(True, env='EXTRACTION_TRACK_COSTS')
    
    @field_validator('ollama_model')
    @classmethod
    def validate_ollama_model(cls, v, info):
        """Ensure ollama_model is set when using Ollama provider."""
        if info.data.get('llm_provider') == 'ollama' and not v:
            raise ValueError('EXTRACTION_OLLAMA_MODEL must be set when using Ollama provider')
        return v


    @field_validator('chunk_overlap')
    @classmethod
    def validate_chunk_overlap(cls, v, info):
        """Ensure chunk_overlap is less than chunk_size."""
        if 'chunk_size' in info.data and v >= info.data['chunk_size']:
            raise ValueError('chunk_overlap must be less than chunk_size')
        return v
    
    @field_validator('temperature')
    @classmethod
    def validate_temperature(cls, v):
        """Ensure temperature is between 0 and 2."""
        if not 0 <= v <= 2:
            raise ValueError('temperature must be between 0 and 2')
        return v
    
    @field_validator('top_p')
    @classmethod
    def validate_top_p(cls, v):
        """Ensure top_p is between 0 and 1."""
        if not 0 <= v <= 1:
            raise ValueError('top_p must be between 0 and 1')
        return v
    
    class Config:
        env_prefix = 'EXTRACTION_'


class OllamaSettings(BaseSettings):
    """Ollama API configuration settings."""

    base_url: str = Field('http://localhost:11434', env='OLLAMA_BASE_URL')
    timeout: int = Field(30000, env='OLLAMA_TIMEOUT')

    # Ollama-specific extraction parameters
    extraction_seed: int = Field(42, env='OLLAMA_EXTRACTION_SEED')
    num_ctx: int = Field(8192, env='OLLAMA_NUM_CTX')

    class Config:
        env_prefix = 'OLLAMA_'


class GeminiSettings(BaseSettings):
    """Google Gemini API configuration settings."""

    api_key: Optional[str] = Field(None, env='GEMINI_API_KEY')
    model: str = Field('gemini-1.5-flash', env='GEMINI_MODEL')
    batch_size: int = Field(10, env='GEMINI_BATCH_SIZE')  # For batch processing

    class Config:
        env_prefix = 'GEMINI_'


class LoggingSettings(BaseSettings):
    """Logging configuration settings."""
    
    level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR'] = Field('INFO', env='LOG_LEVEL')
    file: Optional[str] = Field(None, env='LOG_FILE')
    format: str = Field(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        env='LOG_FORMAT'
    )
    
    class Config:
        env_prefix = 'LOG_'



class PathSettings(BaseSettings):
    """File path configuration."""
    
    data_dir: Path = Field(Path('data'), env='DATA_DIR')
    output_dir: Path = Field(Path('data/output'), env='OUTPUT_DIR')
    logs_dir: Path = Field(Path('logs'), env='LOGS_DIR')
    
    def ensure_directories(self):
        """Create directories if they don't exist."""
        for dir_path in [self.data_dir, self.output_dir, self.logs_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    class Config:
        env_prefix = ''


class Settings(BaseSettings):
    """Main settings class that combines all configuration sections."""
    
    # Environment
    environment: Literal['local', 'production'] = Field('local', env='ENVIRONMENT')
    
    # Sub-configurations
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    storage: StorageSettings = Field(default_factory=StorageSettings)
    extraction: ExtractionSettings = Field(default_factory=ExtractionSettings)
    ollama: OllamaSettings = Field(default_factory=OllamaSettings)
    gemini: GeminiSettings = Field(default_factory=GeminiSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    paths: PathSettings = Field(default_factory=PathSettings)
    
    class Config:
        env_file = 'config/.env'
        case_sensitive = False
        extra = 'ignore'  # Ignore extra environment variables
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == 'production'
    
    @property
    def is_local(self) -> bool:
        """Check if running in local environment."""
        return self.environment == 'local'
    
    @property
    def active_database_uri(self) -> str:
        """Get the active database URI based on environment."""
        if self.is_production and self.database.supabase_database_uri:
            return self.database.supabase_database_uri
        elif self.is_local and self.database.local_database_uri:
            return self.database.local_database_uri
        else:
            raise ValueError(f"No database URI configured for {self.environment} environment")
    
    
    def validate_config(self) -> bool:
        """Validate that required configuration is present."""
        errors = []
        
        # Check database configuration
        if self.is_production and not self.database.supabase_database_uri:
            errors.append("SUPABASE_DATABASE_URI is not set for production")
        elif self.is_local and not self.database.local_database_uri:
            errors.append("LOCAL_DATABASE_URI is not set for local environment")
        
        # Check Supabase credentials if in production (storage always uses Supabase)
        if self.is_production:
            if not self.database.supabase_url:
                errors.append("SUPABASE_URL is not set")
            if not self.database.supabase_key:
                errors.append("SUPABASE_KEY is not set")
        
        # Validate extraction settings
        if self.extraction.chunk_overlap >= self.extraction.chunk_size:
            errors.append("chunk_overlap must be less than chunk_size")
        
        if errors:
            for error in errors:
                print(f"Configuration error: {error}")
            raise ValueError("Configuration validation failed")
        
        return True
    

# Load .env file before creating settings instance
env_file = Path(__file__).parent.parent.parent / "config" / ".env"
if env_file.exists():
    load_dotenv(env_file)

# Create global settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings


# Exit codes for consistent error handling
class ExitCodes:
    """Standard exit codes for consistent error handling."""
    SUCCESS = 0
    GENERAL_ERROR = 1
    CONFIG_ERROR = 2
    FILE_NOT_FOUND = 3
    DATABASE_ERROR = 4
    API_ERROR = 5
    INTERRUPTED = 130  # Standard SIGINT code