import psycopg2

# Connect to your postgres DB
conn = psycopg2.connect("dbname=rpsl user=bernardo-ubuntu")

# Open a cursor to perform database operations
cur = conn.cursor()

# Creates tables
cur.execute(
    """
	create table if not exists aut_num(
		as_num int primary key,
		imports json not null,
		exports json not null,
		body text not null
	);
	"""
)

# Make the changes to the database persistent
conn.commit()

# Closes connection
cur.close()
conn.close()
