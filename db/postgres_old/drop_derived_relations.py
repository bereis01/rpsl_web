import os
import psycopg2

# Connect to your postgres DB
user = os.environ["DB_USER"]
dbname = os.environ["DB_NAME"]
conn = psycopg2.connect(f"dbname={dbname} user={user}")

# Open a cursor to perform database operations
cur = conn.cursor()

# Drops tables
cur.execute(
    """
	drop table if exists routes cascade
	"""
)

# Make the changes to the database persistent
conn.commit()

# Closes connection
cur.close()
conn.close()
