#!/usr/bin/env python3
"""
UFC Database Setup Script
=========================

This script sets up the UFC database from scratch, including schema creation
and data migration from existing CSV files.

Usage:
    python setup_database.py [--db-path DATABASE_PATH] [--data-file CSV_FILE]
"""

import argparse
import os
import sys
import logging
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from database_schema import UFCDatabase
from data_migration import UFCDataMigrator
from config import get_db_path, get_backup_path
from database_utils import backup_database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_database(db_path: str, data_file: str = None, backup_existing: bool = True):
    """Set up the UFC database with schema and data."""
    
    # Backup existing database if it exists
    if backup_existing and os.path.exists(db_path):
        backup_path = get_backup_path(db_path)
        backup_database(db_path, backup_path)
        logger.info(f"Backed up existing database to {backup_path}")
    
    # Initialize database schema
    logger.info("Creating database schema...")
    db = UFCDatabase(db_path)
    try:
        db.create_tables()
        db.create_indexes()
        logger.info("Database schema created successfully")
    except Exception as e:
        logger.error(f"Failed to create database schema: {e}")
        raise
    finally:
        db.close()
    
    # Migrate data if CSV file provided
    if data_file and os.path.exists(data_file):
        logger.info(f"Migrating data from {data_file}...")
        migrator = UFCDataMigrator(db_path, ".")
        try:
            migrator.migrate_complete_data(data_file)
            logger.info("Data migration completed successfully")
        except Exception as e:
            logger.error(f"Data migration failed: {e}")
            raise
        finally:
            migrator.close()
    elif data_file:
        logger.warning(f"Data file not found: {data_file}")
    
    logger.info(f"Database setup complete: {db_path}")


def main():
    """Main setup function."""
    parser = argparse.ArgumentParser(description="Set up UFC database")
    parser.add_argument(
        "--db-path", 
        default="ufc_data.db",
        help="Path to the database file (default: ufc_data.db)"
    )
    parser.add_argument(
        "--data-file",
        default="complete_ufc_data.csv",
        help="Path to the CSV data file (default: complete_ufc_data.csv)"
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Don't backup existing database"
    )
    parser.add_argument(
        "--schema-only",
        action="store_true",
        help="Only create schema, don't migrate data"
    )
    
    args = parser.parse_args()
    
    try:
        data_file = None if args.schema_only else args.data_file
        setup_database(
            db_path=args.db_path,
            data_file=data_file,
            backup_existing=not args.no_backup
        )
        
        print("\n" + "="*50)
        print("DATABASE SETUP COMPLETE")
        print("="*50)
        print(f"Database: {args.db_path}")
        if not args.schema_only and data_file:
            print(f"Data source: {data_file}")
        print("\nNext steps:")
        print("1. Use the data access layer for CRUD operations")
        print("2. Run analytics and generate reports")
        print("3. Integrate with prediction models")
        print("4. Create DraftKings lineups")
        print("\nSee example_usage.py for demonstrations")
        
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
