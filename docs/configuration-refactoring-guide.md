# Configuration Refactoring Guide: From JSON/Hardcoded to Pydantic Settings

## Overview
This guide documents the process of refactoring a complex configuration system that had JSON files, environment variables, and hardcoded values scattered throughout the codebase into a centralized, type-safe Pydantic Settings implementation.

## Table of Contents
- [Initial State Problems](#initial-state-problems)
- [Implementation Steps](#implementation-steps)
- [Problems Encountered & Solutions](#problems-encountered--solutions)
- [Migration Checklist](#migration-checklist)
- [Best Practices for Database Projects](#best-practices-for-database-projects)
- [Testing Configuration](#testing-configuration)
- [Key Takeaways](#key-takeaways)

## Initial State Problems

1. **Three different config sources**: JSON files (`config.json`, `config.local.json`, `config.prod.json`), `.env` file, and hardcoded values
2. **Naming mismatches**: `config.prod.json` vs `ENVIRONMENT=production`
3. **Unused configurations**: JSON files loaded but mostly ignored
4. **No validation**: Missing configs only discovered at runtime
5. **Scattered hardcoded values**: Grid sizes, API settings, density thresholds throughout code

## Implementation Steps

### 1. Install Dependencies

```bash
pip install pydantic pydantic-settings python-dotenv
```

### 2. Create Settings Structure

Create `src/core/settings.py`:

```python
from pathlib import Path
from typing import Dict, List, Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Sub-settings for organization
class APISettings(BaseSettings):
    """API configuration settings."""
    google_places_api_key: str = Field(None, env='GOOGLE_PLACES_API_KEY')
    rate_limit: int = Field(30000, env='API_RATE_LIMIT')
    timeout: int = Field(30000, env='API_TIMEOUT')
    retry_attempts: int = Field(3, env='API_RETRY_ATTEMPTS')

class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    local_database_uri: Optional[str] = Field(None, env='LOCAL_DATABASE_URI')
    supabase_database_uri: Optional[str] = Field(None, env='SUPABASE_DATABASE_URI')
    supabase_url: Optional[str] = Field(None, env='SUPABASE_URL')
    supabase_key: Optional[str] = Field(None, env='SUPABASE_KEY')

class PathSettings(BaseSettings):
    """File path configuration."""
    data_dir: Path = Field(Path('data'), env='DATA_DIR')
    output_dir: Path = Field(Path('data/output'), env='OUTPUT_DIR')
    cities_csv: str = Field('data/output/cities_cleaned.csv', env='CITIES_CSV_PATH')

class Settings(BaseSettings):
    """Main settings class that combines all configuration sections."""
    
    # Environment
    environment: str = Field('local', env='ENVIRONMENT')
    
    # Sub-configurations
    api: APISettings = Field(default_factory=APISettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    paths: PathSettings = Field(default_factory=PathSettings)
    
    class Config:
        env_file = 'config/.env'
        case_sensitive = False
        extra = 'ignore'  # Important: prevents validation errors from extra env vars
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == 'production'
    
    @property
    def is_local(self) -> bool:
        """Check if running in local environment."""
        return self.environment.lower() == 'local'
    
    @property
    def active_database_uri(self) -> str:
        """Get the active database URI based on environment."""
        if self.is_production:
            return self.database.supabase_database_uri
        return self.database.local_database_uri

# CRITICAL: Load .env before creating settings instance
env_file = Path(__file__).parent.parent.parent / "config" / ".env"
if env_file.exists():
    load_dotenv(env_file)

# Create global settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings
```

## Problems Encountered & Solutions

### Problem 1: Pydantic v2 Breaking Changes

**Error**: 
```
PydanticImportError: BaseSettings has been moved to pydantic-settings
```

**Solution**: 
```python
# Wrong (Pydantic v1)
from pydantic import BaseSettings

# Correct (Pydantic v2)
from pydantic_settings import BaseSettings
```

### Problem 2: Environment Variables Not Loading in Sub-Settings

**Issue**: Sub-settings classes (like `DatabaseSettings`) weren't loading from `.env` file

**Solution**: Manually load dotenv BEFORE creating settings instance
```python
# Must load .env first
from pathlib import Path
from dotenv import load_dotenv

env_file = Path(__file__).parent.parent.parent / "config" / ".env"
if env_file.exists():
    load_dotenv(env_file)

# Then create settings
settings = Settings()
```

### Problem 3: Extra Environment Variables Causing Validation Errors

**Error**: 
```
validation error for Settings
google_application_credentials
  Extra inputs are not permitted [type=extra_forbidden]
```

**Solution**: Add `extra = 'ignore'` to Config class
```python
class Config:
    env_file = 'config/.env'
    case_sensitive = False
    extra = 'ignore'  # Ignore extra environment variables
```

### Problem 4: Database Connection Refactoring

**Issue**: Database connection was using different methods for local vs production (psycopg2 vs Supabase client)

**Solution**: Simplified to use PostgreSQL for both environments
```python
class DatabaseConnection:
    def __init__(self):
        self.settings = get_settings()
        self.active_db_url = self.settings.active_database_uri
        
    def execute_query(self, query: str, params: tuple = None):
        # Use same PostgreSQL connection for both local and production
        with psycopg2.connect(self.active_db_url) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                if fetch:
                    return cur.fetchall()
                conn.commit()
                return cur.rowcount
```

## Migration Checklist

### 1. Audit Current Configuration

```bash
# Find all hardcoded values
grep -r "2500\|10000\|30000" --include="*.py"

# List all config files
find . -name "config*"

# Check environment variable usage
grep -r "os.getenv\|os.environ" --include="*.py"
```

### 2. Design Settings Structure

- Group related settings (API, Database, Paths, etc.)
- Use sub-settings classes for organization
- Add properties for computed values (like `active_database_uri`)

### 3. Update Imports Throughout Codebase

```python
# Old approach
from src.core.config import get_config
config = get_config()
api_key = config.get_google_api_key()

# New approach
from src.core.settings import get_settings
settings = get_settings()
api_key = settings.api.google_places_api_key
```

### 4. Handle Environment Switching

```bash
# Development (default)
python main.py status

# Production
ENVIRONMENT=production python main.py status
```

### 5. Remove Old Configuration Files

```bash
rm config/*.json
rm src/core/config.py
```

## Best Practices for Database Projects

### 1. Separate Database Configs by Environment

```python
@property
def active_database_uri(self) -> str:
    """Get the appropriate database URI based on environment."""
    if self.environment == 'production':
        return self.database.supabase_database_uri
    return self.database.local_database_uri
```

### 2. Add Connection Pooling Settings

```python
class DatabaseSettings(BaseSettings):
    local_database_uri: Optional[str] = Field(None, env='LOCAL_DATABASE_URI')
    supabase_database_uri: Optional[str] = Field(None, env='SUPABASE_DATABASE_URI')
    
    # Connection pool settings
    max_connections: int = Field(20, env='DB_MAX_CONNECTIONS')
    connection_timeout: int = Field(30, env='DB_TIMEOUT')
    pool_size: int = Field(5, env='DB_POOL_SIZE')
```

### 3. Validate Configuration on Startup

```python
def validate_config(self) -> bool:
    """Validate that required configuration is present."""
    errors = []
    
    # Check API key
    if not self.api.google_places_api_key:
        errors.append("GOOGLE_PLACES_API_KEY is not set")
    
    # Check database configuration
    if self.is_production and not self.database.supabase_database_uri:
        errors.append("SUPABASE_DATABASE_URI is not set for production")
    elif self.is_local and not self.database.local_database_uri:
        errors.append("LOCAL_DATABASE_URI is not set for local environment")
    
    if errors:
        for error in errors:
            print(f"Configuration error: {error}")
        raise ValueError("Configuration validation failed")
    
    return True
```

### 4. Keep Sensitive Data in .env (Never Commit)

```bash
# .env (add to .gitignore)
ENVIRONMENT=local
LOCAL_DATABASE_URI=postgresql://localhost/myapp
SUPABASE_DATABASE_URI=postgresql://user:pass@host:5432/db
SUPABASE_KEY=sb_secret_...
GOOGLE_PLACES_API_KEY=AIza...
```

## Testing Configuration

### Quick Tests

```python
# Test local environment
python -c "from src.core.settings import get_settings; s = get_settings(); print('Environment:', s.environment); print('Database:', s.active_database_uri)"

# Test production environment
ENVIRONMENT=production python -c "from src.core.settings import get_settings; s = get_settings(); print('Environment:', s.environment); print('Database:', s.active_database_uri)"
```

### Test Script

```python
#!/usr/bin/env python
"""Test configuration loading."""

from src.core.settings import get_settings

def test_config():
    settings = get_settings()
    
    print(f"Environment: {settings.environment}")
    print(f"Is Production: {settings.is_production}")
    print(f"Is Local: {settings.is_local}")
    print(f"Database URI: {settings.active_database_uri}")
    print(f"API Key Set: {bool(settings.api.google_places_api_key)}")
    
    # Validate
    try:
        settings.validate_config()
        print("✅ Configuration is valid")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")

if __name__ == "__main__":
    test_config()
```

## Key Takeaways

1. **Always load dotenv before creating settings instance** - Sub-settings don't automatically load .env files
2. **Use `extra = 'ignore'` to handle unrelated env vars** - Prevents validation errors from other environment variables
3. **Pydantic v2 requires `pydantic-settings` package** - BaseSettings moved to separate package
4. **Simplify database connections** - Use same method for all environments when possible
5. **Group related settings in sub-classes** - Better organization and type hints
6. **Add validation and helpful properties** - Catch configuration errors early
7. **Use Field defaults wisely** - Provide sensible defaults where appropriate
8. **Document environment variables** - Keep a template .env.example file

## Example Usage

```python
from src.core.settings import get_settings

# Get settings instance
settings = get_settings()

# Access configuration
api_key = settings.api.google_places_api_key
rate_limit = settings.api.rate_limit
db_uri = settings.active_database_uri

# Check environment
if settings.is_production:
    # Production-specific logic
    print("Running in production mode")
else:
    # Development logic
    print("Running in local mode")

# Access nested settings
timeout = settings.api.timeout
cities_path = settings.paths.cities_csv
```

## Benefits of This Approach

- ✅ **Type Safety**: IDE autocomplete and type checking
- ✅ **Single Source of Truth**: No more scattered configuration
- ✅ **Environment Flexibility**: Easy switching between environments
- ✅ **Validation**: Catches missing configuration at startup
- ✅ **Clean API**: Intuitive dot notation access
- ✅ **Testability**: Easy to mock for testing
- ✅ **Documentation**: Settings classes serve as documentation
- ✅ **Override Capability**: Any setting can be overridden via environment variables

## Common Pitfalls to Avoid

1. **Forgetting to load .env**: Always load dotenv before creating settings
2. **Not handling extra env vars**: Use `extra = 'ignore'` in Config
3. **Hardcoding after refactor**: Resist temptation to hardcode "just this once"
4. **Committing secrets**: Always add .env to .gitignore
5. **Complex nested structures**: Keep settings relatively flat for simplicity
6. **Not validating early**: Add validation to catch issues at startup

This approach provides a robust, maintainable configuration system that scales well with project growth and team size.

---

# Main.py Standardized Conventions

## Overview
Standardized conventions for creating consistent, maintainable CLI entry points using `main.py` across projects.

## Core Principles

1. **Single Entry Point**: `main.py` should be the only CLI entry point
2. **Subcommand Pattern**: Use subcommands for different operations
3. **Self-Documenting**: Comprehensive help text with examples
4. **Environment Aware**: Support environment switching via environment variables
5. **Fail Fast**: Validate configuration before executing
6. **Progress Feedback**: Clear feedback during long operations

## Standard Commands

Every `main.py` should implement these core commands:

### 1. Status Command
Shows system health and configuration.

```python
def status_command(args):
    """Show system status and configuration."""
    settings = get_settings()
    
    print("Project Status")
    print("=" * 60)
    print(f"Environment: {settings.environment}")
    print(f"Version: {__version__}")
    
    # Check critical components
    print("\nComponents:")
    print(f"  Database: {'✓ connected' if check_db() else '✗ disconnected'}")
    print(f"  API Keys: {'✓ configured' if settings.api.key else '✗ missing'}")
    
    # Check data files
    print("\nData Files:")
    for file in required_files:
        print(f"  {file}: {'✓ exists' if Path(file).exists() else '✗ missing'}")
    
    return 0
```

### 2. Run/Process Command
Main processing command.

```python
def run_command(args):
    """Run the main processing pipeline."""
    settings = get_settings()
    
    # Validate before running
    if not settings.validate_config():
        print("Configuration validation failed")
        return 1
    
    print(f"Starting processing in {settings.environment} mode...")
    print("-" * 60)
    
    try:
        result = process_data(args.input, args.output)
        print(f"✓ Processing complete: {result}")
        return 0
    except Exception as e:
        print(f"✗ Processing failed: {e}")
        return 1
```

### 3. Stats Command
View processing statistics and metrics.

```python
def stats_command(args):
    """Display processing statistics."""
    settings = get_settings()
    
    print("Processing Statistics")
    print("=" * 60)
    
    # Load statistics from database or files
    stats = load_statistics()
    
    if args.format == 'json':
        import json
        print(json.dumps(stats, indent=2))
    else:
        # Table format
        print(f"Total Processed: {stats['total_processed']:,}")
        print(f"Success Rate: {stats['success_rate']:.1f}%")
        print(f"Average Time: {stats['avg_time']:.2f}s")
        print(f"Last Run: {stats['last_run']}")
        
        if stats.get('by_category'):
            print("\nBy Category:")
            for category, count in stats['by_category'].items():
                print(f"  {category}: {count:,}")
    
    return 0
```

## Implementation Template

```python
#!/usr/bin/env python
"""
Project Name - CLI Interface

Usage:
    python main.py <command> [options]

Commands:
    status      Show system status
    run         Execute main processing
    stats       View processing statistics
    
Examples:
    python main.py status
    python main.py run --input data.csv
    ENVIRONMENT=production python main.py run
"""

import sys
import argparse
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.core.settings import get_settings
from src.commands import status, run, stats


def create_parser():
    """Create the argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        description='Project Name - CLI Interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py status                    # Check system status
  python main.py run --input data.csv      # Process data
  python main.py stats                     # View processing statistics
  
Environment:
  Set ENVIRONMENT variable to switch configurations:
    ENVIRONMENT=production python main.py run
        """
    )
    
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands'
    )
    
    # Status command
    subparsers.add_parser('status', help='Show system status')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Execute processing')
    run_parser.add_argument('--input', required=True, help='Input file')
    run_parser.add_argument('--output', default='output/', help='Output directory')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='View processing statistics')
    stats_parser.add_argument('--format', choices=['table', 'json'], default='table', help='Output format')
    
    return parser


def main():
    """Main entry point for CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Show help if no command provided
    if not args.command:
        parser.print_help()
        return 0
    
    # Route to command handlers
    commands = {
        'status': status_command,
        'run': run_command,
        'stats': stats_command,
    }
    
    handler = commands.get(args.command)
    if handler:
        try:
            exit_code = handler(args)
            sys.exit(exit_code)
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            sys.exit(1)
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
```

## Best Practices

### 1. Error Handling & Exit Codes

Define standardized exit codes in your settings module for consistent error handling:

```python
# In config/settings.py
class ExitCodes:
    """Standard exit codes for consistent error handling"""
    SUCCESS = 0
    GENERAL_ERROR = 1
    CONFIG_ERROR = 2
    FILE_NOT_FOUND = 3
    DATABASE_ERROR = 4
    API_ERROR = 5
    INTERRUPTED = 130  # Standard SIGINT code
```

Use these codes consistently in your command handlers:

```python
from config.settings import ExitCodes

def command_handler(args):
    try:
        # Validate configuration
        if not settings.validate_config():
            return ExitCodes.CONFIG_ERROR
        
        # Process command
        process_data()
        return ExitCodes.SUCCESS
        
    except FileNotFoundError as e:
        print(f"Error: File not found: {e}")
        return ExitCodes.FILE_NOT_FOUND
    except DatabaseError as e:
        print(f"Database error: {e}")
        return ExitCodes.DATABASE_ERROR
    except Exception as e:
        print(f"Unexpected error: {e}")
        return ExitCodes.GENERAL_ERROR
```

Handle interrupts gracefully in the main function:

```python
def main():
    try:
        return _main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        return ExitCodes.INTERRUPTED
    except Exception as e:
        print(f"Unexpected error: {e}")
        return ExitCodes.GENERAL_ERROR
```

**Exit Code Meanings:**
- `0` (SUCCESS): Operation completed successfully
- `1` (GENERAL_ERROR): Unspecified error occurred
- `2` (CONFIG_ERROR): Configuration validation failed
- `3` (FILE_NOT_FOUND): Required file or data not found
- `4` (DATABASE_ERROR): Database connection or query failed
- `5` (API_ERROR): External API call failed
- `130` (INTERRUPTED): User interrupted execution (Ctrl+C)

### 2. Progress Indicators
```python
# For long operations
from tqdm import tqdm

def process_items(items):
    for item in tqdm(items, desc="Processing"):
        process_item(item)

# Or simple progress
total = len(items)
for i, item in enumerate(items, 1):
    print(f"Processing {i}/{total}: {item.name}")
    process_item(item)
```

### 3. Validation Before Execution
```python
def validate_before_run():
    """Validate system state before running."""
    errors = []
    
    # Check configuration
    settings = get_settings()
    if not settings.validate_config():
        errors.append("Invalid configuration")
    
    # Check required files
    for file in REQUIRED_FILES:
        if not Path(file).exists():
            errors.append(f"Missing file: {file}")
    
    # Check database connection
    if not test_database_connection():
        errors.append("Database connection failed")
    
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"  ✗ {error}")
        return False
    
    return True
```

### 4. Environment Handling
```python
def run_command(args):
    settings = get_settings()
    
    if settings.is_production:
        print("⚠️  Running in PRODUCTION mode")
        if not confirm("Continue?"):
            return 0
```

## Common Patterns

### Batch Processing with Limits
```python
parser.add_argument('--limit', type=int, help='Process only N items')
parser.add_argument('--offset', type=int, default=0, help='Start from item N')

def run_command(args):
    items = load_items()
    if args.offset:
        items = items[args.offset:]
    if args.limit:
        items = items[:args.limit]
    process_items(items)
```

### Confirmation Prompts
```python
def confirm(message="Continue?"):
    """Ask for confirmation."""
    response = input(f"{message} [y/N]: ").lower().strip()
    return response in ['y', 'yes']

def dangerous_command(args):
    if not args.force:
        if not confirm("This will delete data. Continue?"):
            print("Aborted")
            return 0
```

## Testing CLI Commands

```python
# tests/test_cli.py
import subprocess
import sys

def test_status_command():
    """Test status command."""
    result = subprocess.run(
        [sys.executable, "main.py", "status"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Environment:" in result.stdout

def test_invalid_command():
    """Test invalid command handling."""
    result = subprocess.run(
        [sys.executable, "main.py", "invalid"],
        capture_output=True,
        text=True
    )
    assert result.returncode != 0
```

## Summary

A well-designed `main.py`:
1. Provides a single, consistent entry point
2. Uses subcommands for different operations
3. Includes comprehensive help text
4. Validates inputs before execution
5. Provides clear progress feedback
6. Handles errors gracefully with appropriate exit codes
7. Supports environment configuration
8. Is testable and maintainable

Following these conventions ensures consistency across projects and makes CLIs intuitive for users and maintainable for developers.