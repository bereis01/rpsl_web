import os
import json
import psycopg2
import pandas as pd


def load_aut_nums(data, conn):
    """
    Receives a dictionary of the parsed aut_num object data.
    Inserts this data into the corresponding relation in the database.
    """
    # Converts the data into a dataframe
    aut_nums = pd.DataFrame.from_dict(data, orient="index")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Traverses the data in the dataframe and inserts it into the database
    # If the key is already present, updates it
    for i in range(aut_nums.shape[0]):
        entry = aut_nums.iloc[i]
        cur.execute(
            """
            insert into aut_nums (as_num, imports, exports, body) 
            values (%s, %s, %s, %s)
            """,
            (
                entry.name,
                json.dumps(entry["imports"]),
                json.dumps(entry["exports"]),
                entry["body"],
            ),
        )

    # Closes the cursor
    cur.close()


def load_as_sets(data, conn):
    """
    Receives a dictionary of the parsed as_set object data.
    Inserts this data into the corresponding relation in the database.
    """
    # Converts the data into a dataframe
    as_sets = pd.DataFrame.from_dict(data, orient="index")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Traverses the data in the dataframe and inserts it into the database
    # If the key is already present, updates it
    for i in range(as_sets.shape[0]):
        entry = as_sets.iloc[i]
        cur.execute(
            """
            insert into as_sets (as_set_name, as_members, set_members, is_any) 
            values (%s, %s, %s, %s)
            """,
            (
                entry.name,
                entry["members"],
                entry["set_members"],
                bool(entry["is_any"]),
            ),
        )

    # Closes the cursor
    cur.close()


def load_route_sets(data, conn):
    """
    Receives a dictionary of the parsed route_set object data.
    Inserts this data into the corresponding relation in the database.
    """
    # Converts the data into a dataframe
    route_sets = pd.DataFrame.from_dict(data, orient="index")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Traverses the data in the dataframe and inserts it into the database
    # If the key is already present, updates it
    for i in range(route_sets.shape[0]):
        entry = route_sets.iloc[i]
        cur.execute(
            """
            insert into route_sets (route_set_name, body, members) 
            values (%s, %s, %s::json[])
            """,
            (
                entry.name,
                entry["body"],
                [json.dumps(x) for x in entry["members"]],
            ),
        )

    # Closes the cursor
    cur.close()


def load_peering_sets(data, conn):
    """
    Receives a dictionary of the parsed peering_set object data.
    Inserts this data into the corresponding relation in the database.
    """
    # Converts the data into a dataframe
    peering_sets = pd.DataFrame.from_dict(data, orient="index")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Traverses the data in the dataframe and inserts it into the database
    # If the key is already present, updates it
    for i in range(peering_sets.shape[0]):
        entry = peering_sets.iloc[i]
        cur.execute(
            """
            insert into peering_sets (peering_set_name, body, peerings) 
            values (%s, %s, %s::json[])
            """,
            (
                entry.name,
                entry["body"],
                [json.dumps(x) for x in entry["peerings"]],
            ),
        )

    # Closes the cursor
    cur.close()


def load_filter_sets(data, conn):
    """
    Receives a dictionary of the parsed filter_set object data.
    Inserts this data into the corresponding relation in the database.
    """
    # Converts the data into a dataframe
    filter_sets = pd.DataFrame.from_dict(data, orient="index")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Traverses the data in the dataframe and inserts it into the database
    # If the key is already present, updates it
    for i in range(filter_sets.shape[0]):
        entry = filter_sets.iloc[i]
        cur.execute(
            """
            insert into filter_sets (filter_set_name, body, filters) 
            values (%s, %s, %s::json[])
            """,
            (
                entry.name,
                entry["body"],
                [json.dumps(x) for x in entry["filters"]],
            ),
        )

    # Closes the cursor
    cur.close()


def load_as_routes(data, conn):
    """
    Receives a dictionary of the parsed as_route object data.
    Inserts this data into the corresponding relation in the database.
    """
    # Converts the data into a dataframe
    as_routes = pd.DataFrame.from_dict(
        {key: [data[key]] for key in data},
        orient="index",
        columns=["routes"],
    )

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Traverses the data in the dataframe and inserts it into the database
    # If the key is already present, updates it
    for i in range(as_routes.shape[0]):
        entry = as_routes.iloc[i]
        cur.execute(
            """
            insert into as_routes (as_num, routes) 
            values (%s, %s)
            """,
            (
                entry.name,
                entry["routes"],
            ),
        )

    # Closes the cursor
    cur.close()


# Opens raw data
f = open("./parsed_data/full.json")
data = json.load(f)

# Connect to your postgres DB
user = os.environ["DB_USER"]
dbname = os.environ["DB_NAME"]
conn = psycopg2.connect("dbname=rpsl user=bernardo-ubuntu")

# Loads the data from each RPSL class
load_aut_nums(data["aut_nums"], conn)
load_as_sets(data["as_sets"], conn)
load_route_sets(data["route_sets"], conn)
load_peering_sets(data["peering_sets"], conn)
load_filter_sets(data["filter_sets"], conn)
load_as_routes(data["as_routes"], conn)

# Make the changes to the database persistent
# and closes the connection
conn.commit()
conn.close()
