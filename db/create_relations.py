import os
import psycopg2

# Connect to your postgres DB
user = os.environ["DB_USER"]
dbname = os.environ["DB_NAME"]
conn = psycopg2.connect(f"dbname={dbname} user={user}")

# Open a cursor to perform database operations
cur = conn.cursor()

# Creates tables
cur.execute(
    """
	create table if not exists aut_nums(
		as_num bigint primary key,
		imports json not null,
		exports json not null,
		body text not null
	);
	"""
)

cur.execute(
    """
	create table if not exists as_sets(
		as_set_name text primary key,
		as_members integer[] not null,
		set_members text[] not null,
		is_any boolean not null
	);
	"""
)

cur.execute(
    """
	create table if not exists route_sets(
		route_set_name text primary key,
		body text not null,
		members json[] not null
	);
	"""
)

cur.execute(
    """
	create table if not exists peering_sets(
		peering_set_name text primary key,
		body text not null,
		peerings json[] not null
	);
	"""
)

cur.execute(
    """
	create table if not exists filter_sets(
		filter_set_name text primary key,
		body text not null,
		filters json[] not null
	);
	"""
)

cur.execute(
    """
	create table if not exists filter_sets(
		filter_set_name text primary key,
		body text not null,
		filters json[] not null
	);
	"""
)

cur.execute(
    """
	create table if not exists as_routes(
		as_num bigint primary key,
		routes text[] not null
	);
	"""
)

# Make the changes to the database persistent
conn.commit()

# Closes connection
cur.close()
conn.close()
