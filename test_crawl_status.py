import psycopg2
from datetime import datetime
import json

# Connect to local database
conn = psycopg2.connect("postgresql://sperk@localhost:5432/claimsboost")
cur = conn.cursor()

# Simulate storing a qualified extraction
domain = "137law.com"
extraction_type = "law_firm_confirmation"
clean_result = {
    "is_law_firm": "true",
    "is_personal_injury_firm": "true"
}

# Check current crawl_status
cur.execute("SELECT crawl_status FROM domains WHERE domain = %s", (domain,))
result = cur.fetchone()
print(f"Current crawl_status for {domain}: {result[0] if result else 'NOT FOUND'}")

# Now update it based on our logic
if extraction_type == 'law_firm_confirmation':
    is_law_firm = clean_result.get('is_law_firm', False)
    is_pi_firm = clean_result.get('is_personal_injury_firm', False)
    
    # Check if both are true (handle string or boolean values)
    if (str(is_law_firm).lower() == 'true' and 
        str(is_pi_firm).lower() == 'true'):
        
        # Update crawl_status to 'verified'
        cur.execute("""
            UPDATE domains 
            SET crawl_status = 'verified',
                updated_at = %s
            WHERE domain = %s
        """, (datetime.now(), domain))
        conn.commit()
        print(f"Updated {domain} crawl_status to 'verified' (qualified PI law firm)")

# Check new status
cur.execute("SELECT crawl_status FROM domains WHERE domain = %s", (domain,))
result = cur.fetchone()
print(f"New crawl_status for {domain}: {result[0] if result else 'NOT FOUND'}")

cur.close()
conn.close()
