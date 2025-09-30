#!/usr/bin/env python3
"""
Law Firm Data Extraction System - CLI Interface
Following standardized conventions for maintainable CLI entry points
"""

import argparse
import logging
import sys

from supabase import create_client
from src.core.settings import get_settings, ExitCodes
from src.commands import EmbedCommand, ExtractCommand, TestCommand
from src.database.connection import get_database_connection

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Application:
    """Main application with standardized configuration"""
    
    def __init__(self):
        """Initialize application with Pydantic settings"""
        self.settings = get_settings()
        
        # Validate configuration on startup
        try:
            self.settings.validate_config()
        except ValueError as e:
            logger.error(f"Configuration validation failed: {e}")
            raise
        
        self.supabase_client = self._init_supabase()
        self.db_conn = get_database_connection()
    
    def _init_supabase(self):
        """Initialize Supabase client if credentials available"""
        url = self.settings.database.supabase_url
        key = self.settings.database.supabase_key
        
        if url and key:
            try:
                client = create_client(url, key)
                logger.info("Supabase client initialized")
                return client
            except Exception as e:
                logger.warning(f"Failed to initialize Supabase client: {e}")
                return None
        return None
    
    def handle_status(self, args):
        """Show system status and configuration"""
        try:
            print("\nDistillery System Status")
            print("=" * 60)
            print(f"Environment: {self.settings.environment}")
            print(f"Configuration: ✓ Valid")
            
            print("\nDatabase:")
            if self.db_conn.has_connection:
                print(f"  Connection: ✓ Available")
                print(f"  Type: {'Local PostgreSQL' if self.db_conn.is_local else 'Supabase'}")
                if self.db_conn.is_local:
                    # Test local connection
                    try:
                        with self.db_conn.get_postgres_connection() as (conn, cur):
                            cur.execute("SELECT COUNT(*) FROM domains")
                            domain_count = cur.fetchone()[0]
                            print(f"  Domains: {domain_count}")
                    except Exception as e:
                        print(f"  Status: ✗ Error - {str(e)}")
            else:
                print(f"  Connection: ✗ Not configured")
            
            print("\nSupabase:")
            if self.supabase_client:
                print(f"  Client: ✓ Initialized")
                print(f"  URL: {self.settings.database.supabase_url[:30]}...")
            else:
                print(f"  Client: ✗ Not initialized")
            
            print("\nExtraction Settings:")
            print(f"  Model: {self.settings.extraction.model_type}")
            print(f"  Embedder: {self.settings.extraction.embedder_type}")
            print(f"  Chunk Size: {self.settings.extraction.chunk_size}")
            print(f"  Chunk Overlap: {self.settings.extraction.chunk_overlap}")
            print(f"  Temperature: {self.settings.extraction.temperature}")
            print(f"  K Chunks: {self.settings.extraction.k_chunks}")
            
            print("\nOllama:")
            print(f"  Base URL: {self.settings.ollama.base_url}")
            
            # Check if Ollama is running
            try:
                import requests
                response = requests.get(f"{self.settings.ollama.base_url}/api/tags", timeout=2)
                if response.status_code == 200:
                    models = response.json().get('models', [])
                    print(f"  Status: ✓ Running")
                    print(f"  Models: {len(models)} available")
                    if models:
                        for model in models[:3]:  # Show first 3 models
                            print(f"    - {model.get('name', 'unknown')}")
                else:
                    print(f"  Status: ✗ Not responding")
            except:
                print(f"  Status: ✗ Not running")
            
            print("\nPaths:")
            print(f"  Data: {self.settings.paths.data_dir}")
            print(f"  Output: {self.settings.paths.output_dir}")
            print(f"  Logs: {self.settings.paths.logs_dir}")
            
            return ExitCodes.SUCCESS
            
        except Exception as e:
            logger.error(f"Status check failed: {str(e)}")
            print(f"\n✗ Status check failed: {str(e)}")
            return ExitCodes.GENERAL_ERROR
    
    def handle_stats(self, args):
        """Display extraction statistics"""
        try:
            print("\nExtraction Statistics")
            print("=" * 60)
            
            if not self.db_conn.has_connection:
                print("No database connection available")
                return ExitCodes.DATABASE_ERROR
            
            with self.db_conn.get_postgres_connection() as (conn, cur):
                # Get extraction counts
                cur.execute("""
                    SELECT extraction_name, COUNT(*) as count
                    FROM domain_extractions
                    GROUP BY extraction_name
                    ORDER BY count DESC
                """)
                extractions = cur.fetchall()
                
                if extractions:
                    print("\nExtractions by Type:")
                    for extraction_name, count in extractions:
                        print(f"  {extraction_name}: {count:,}")
                
                # Get domain counts
                cur.execute("""
                    SELECT COUNT(DISTINCT domain) as domain_count,
                           COUNT(*) as total_extractions
                    FROM domain_extractions
                """)
                result = cur.fetchone()
                
                print(f"\nTotal Domains Processed: {result[0]:,}")
                print(f"Total Extractions: {result[1]:,}")
                
                # Get recent extractions
                cur.execute("""
                    SELECT domain, extraction_name, extracted_at
                    FROM domain_extractions
                    ORDER BY extracted_at DESC
                    LIMIT 5
                """)
                recent = cur.fetchall()
                
                if recent:
                    print("\nRecent Extractions:")
                    for domain, extraction_name, extracted_at in recent:
                        print(f"  {domain}: {extraction_name} ({extracted_at})")
            
            return ExitCodes.SUCCESS
            
        except Exception as e:
            logger.error(f"Stats query failed: {str(e)}")
            print(f"\n✗ Stats query failed: {str(e)}")
            return ExitCodes.DATABASE_ERROR
    
    def handle_embed(self, args):
        """Handle embed command"""
        try:
            # Create and execute command
            command = EmbedCommand(self.settings)
            results = command.execute(args.targets, is_domain=args.domain, force=args.force)
            command.display_results(results)
            
            return ExitCodes.SUCCESS
            
        except Exception as e:
            logger.error(f"Embed command failed: {str(e)}")
            print(f"\n✗ Embed command failed: {str(e)}")
            return ExitCodes.GENERAL_ERROR
    
    def handle_extract(self, args):
        """Handle extract command"""
        try:
            # Create and execute command
            command = ExtractCommand(self.settings, self.supabase_client)
            results = command.execute(
                args.targets, 
                extraction_type=args.type,
                is_domain=args.domain
            )
            command.display_results(results)
            
            return ExitCodes.SUCCESS
            
        except Exception as e:
            logger.error(f"Extract command failed: {str(e)}")
            print(f"\n✗ Extract command failed: {str(e)}")
            return ExitCodes.GENERAL_ERROR
    
    def handle_test(self, args):
        """Handle test command"""
        try:
            # Create and execute command
            command = TestCommand(self.settings, self.supabase_client)
            results = command.execute(
                args.domain,
                re_embed=args.re_embed
            )
            command.display_results(results)
            
            return ExitCodes.SUCCESS
            
        except Exception as e:
            logger.error(f"Test command failed: {str(e)}")
            print(f"\n✗ Test command failed: {str(e)}")
            return ExitCodes.GENERAL_ERROR


def create_parser():
    """Create argument parser with standardized commands"""
    parser = argparse.ArgumentParser(
        description='Law Firm Data Extraction System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py status                        # Check system status
  python main.py stats                         # View extraction statistics
  python main.py embed domain.com --domain     # Embed a domain
  python main.py extract domain.com --type office_locations --domain
  
Environment:
  Set ENVIRONMENT variable to switch configurations:
    ENVIRONMENT=production python main.py status
        """
    )
    
    subparsers = parser.add_subparsers(dest='mode', help='Available commands')
    
    # Status command
    subparsers.add_parser('status', help='Show system status and configuration')
    
    # Stats command
    subparsers.add_parser('stats', help='Display extraction statistics')
    
    # Embed command
    embed_parser = subparsers.add_parser('embed', help='Embed documents into vector database')
    embed_parser.add_argument('targets', nargs='+', help='File paths or domain names')
    embed_parser.add_argument('--domain', action='store_true', help='Targets are domains')
    embed_parser.add_argument('--force', action='store_true', help='Force re-embedding')
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract data from embedded documents')
    extract_parser.add_argument('targets', nargs='+', help='Domains or file paths')
    extract_parser.add_argument('--type', required=True,
                               choices=['office_locations', 'law_firm_confirmation', 'year_founded', 'total_settlements', 'supported_languages', 'practice_areas', 'attorneys', 'social_media', 'company_description', 'states_served', 'contact_info', 'all'],
                               help='Type of extraction (use "all" to run all extractors)')
    extract_parser.add_argument('--domain', action='store_true', help='Targets are domains')
    
    # Test command
    test_parser = subparsers.add_parser('test-domain', help='Test extraction for a domain')
    test_parser.add_argument('domain', help='Domain name')
    test_parser.add_argument('--re-embed', action='store_true', help='Re-embed documents')
    
    return parser


def main():
    """Main entry point with standardized error handling"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.mode:
        parser.print_help()
        sys.exit(ExitCodes.SUCCESS)
    
    # Initialize application
    try:
        app = Application()
    except ValueError as e:
        print(f"Configuration error: {str(e)}")
        print("\nPlease check your config/.env file")
        sys.exit(ExitCodes.CONFIG_ERROR)
    except Exception as e:
        print(f"Failed to initialize application: {str(e)}")
        sys.exit(ExitCodes.GENERAL_ERROR)
    
    # Route to appropriate handler
    exit_code = ExitCodes.SUCCESS
    
    try:
        if args.mode == 'status':
            exit_code = app.handle_status(args)
        elif args.mode == 'stats':
            exit_code = app.handle_stats(args)
        elif args.mode == 'embed':
            exit_code = app.handle_embed(args)
        elif args.mode == 'extract':
            exit_code = app.handle_extract(args)
        elif args.mode == 'test-domain':
            exit_code = app.handle_test(args)
        else:
            parser.print_help()
            exit_code = ExitCodes.GENERAL_ERROR
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        exit_code = ExitCodes.INTERRUPTED
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        print(f"\nUnexpected error: {str(e)}")
        exit_code = ExitCodes.GENERAL_ERROR
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()