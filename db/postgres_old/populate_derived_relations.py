import os
import json
import psycopg2
import pandas as pd


def load_routes(conn):
    """
    Populates the routes table with data from the main tables.
    """
    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Queries data from as_routes table
    cur.execute(
        """
        select routes from as_routes
        """
    )
    route_lists = cur.fetchall()

    # Creates a list with all unique routes
    unique_routes = []
    for (route_list,) in route_lists:
        unique_routes += route_list
    unique_routes = list(set(unique_routes))

    print(len(unique_routes))
    for route in unique_routes:
        print(route)
        # Retrieves the numbers of the ases that originate each route
        cur.execute(
            """
            select as_num from as_routes where %s = any (routes)
            """,
            (route,),
        )
        originated_by = [entry for (entry,) in cur.fetchall()]

        # Inserts the record in the database
        cur.execute(
            """
            insert into routes (route, originated_by) 
            values (%s, %s)
            """,
            (route, originated_by),
        )

    # Closes the cursor
    cur.close()


# Connect to your postgres DB
user = os.environ["DB_USER"]
dbname = os.environ["DB_NAME"]
conn = psycopg2.connect("dbname=rpsl user=bernardo-ubuntu")

# Loads the data into the derived relations
load_routes(conn)

# Make the changes to the database persistent
# and closes the connection
conn.commit()
conn.close()
