#!/usr/bin/env python
"""
Execute the AfriBazaar database schema SQL file
"""
import os
import sys
import psycopg
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afribazaar.settings')
sys.path.insert(0, str(Path(__file__).parent / 'ecommerce' / 'afribazaar'))

import django
django.setup()

from django.conf import settings

def execute_schema():
    """Execute the database schema SQL file"""
    
    # Get database config
    db_config = settings.DATABASES['default']
    
    # Read SQL file
    sql_file = Path(__file__).parent / 'afribazaar_database_schema.sql'
    print(f"Reading schema from: {sql_file}")
    
    with open(sql_file, 'r') as f:
        sql_content = f.read()
    
    print(f"Connecting to database: {db_config['HOST']}")
    
    # Connect and execute
    try:
        conn = psycopg.connect(
            dbname=db_config['NAME'],
            user=db_config['USER'],
            password=db_config['PASSWORD'],
            host=db_config['HOST'],
            port=db_config['PORT'],
            sslmode='require'
        )
        
        cursor = conn.cursor()
        
        print("Executing schema...")
        cursor.execute(sql_content)
        conn.commit()
        
        print("✅ Schema executed successfully!")
        print("\nTables created:")
        
        # List tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        tables = cursor.fetchall()
        for table in tables:
            print(f"  - {table[0]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = execute_schema()
    sys.exit(0 if success else 1)
