import os
import json
import psycopg2
import pandas as pd


def update_aut_nums(data, conn):
    """
    Receives a dictionary of the parsed aut_num object data.
    Updates this data into the corresponding relation in the database.
    """
    # Converts the data into a dataframe
    aut_nums = pd.DataFrame.from_dict(data, orient="index")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Traverses the data in the dataframe, updating applicable rows
    for i in range(aut_nums.shape[0]):
        entry = aut_nums.iloc[i]
        # try:
        cur.execute(
            """
            update aut_nums 
            set imports=%s, exports=%s, body=%s
            where as_num=%s
            """,
            (
                json.dumps(entry["imports"]),
                json.dumps(entry["exports"]),
                entry["body"],
                entry.name,
            ),
        )

    # Closes the cursor
    cur.close()


def update_as_sets(data, conn):
    """
    Receives a dictionary of the parsed as_set object data.
    Updates this data into the corresponding relation in the database.
    """
    # Converts the data into a dataframe
    as_sets = pd.DataFrame.from_dict(data, orient="index")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Traverses the data in the dataframe, updating applicable rows
    for i in range(as_sets.shape[0]):
        entry = as_sets.iloc[i]
        # try:
        cur.execute(
            """
            update as_sets 
            set as_members=%s, set_members=%s, is_any=%s
            where as_set_name=%s
            """,
            (
                entry["members"],
                entry["set_members"],
                bool(entry["is_any"]),
                entry.name,
            ),
        )

    # Closes the cursor
    cur.close()


def update_route_sets(data, conn):
    """
    Receives a dictionary of the parsed route_set object data.
    Updates this data into the corresponding relation in the database.
    """
    # Converts the data into a dataframe
    route_sets = pd.DataFrame.from_dict(data, orient="index")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Traverses the data in the dataframe, updating applicable rows
    for i in range(route_sets.shape[0]):
        entry = route_sets.iloc[i]
        # try:
        cur.execute(
            """
            update route_sets 
            set body=%s, members=%s::json[]
            where route_set_name=%s
            """,
            (
                entry["body"],
                [json.dumps(x) for x in entry["members"]],
                entry.name,
            ),
        )

    # Closes the cursor
    cur.close()


def update_peering_sets(data, conn):
    """
    Receives a dictionary of the parsed peering_set object data.
    Updates this data into the corresponding relation in the database.
    """
    # Converts the data into a dataframe
    peering_sets = pd.DataFrame.from_dict(data, orient="index")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Traverses the data in the dataframe, updating applicable rows
    for i in range(peering_sets.shape[0]):
        entry = peering_sets.iloc[i]
        # try:
        cur.execute(
            """
            update peering_sets 
            set body=%s, peerings=%s::json[]
            where peering_set_name=%s
            """,
            (
                entry["body"],
                [json.dumps(x) for x in entry["peerings"]],
                entry.name,
            ),
        )

    # Closes the cursor
    cur.close()


def update_filter_sets(data, conn):
    """
    Receives a dictionary of the parsed filter_set object data.
    Updates this data into the corresponding relation in the database.
    """
    # Converts the data into a dataframe
    filter_sets = pd.DataFrame.from_dict(data, orient="index")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Traverses the data in the dataframe, updating applicable rows
    for i in range(filter_sets.shape[0]):
        entry = filter_sets.iloc[i]
        # try:
        cur.execute(
            """
            update filter_sets 
            set body=%s, filters=%s::json[]
            where filter_set_name=%s
            """,
            (
                entry["body"],
                [json.dumps(x) for x in entry["filters"]],
                entry.name,
            ),
        )

    # Closes the cursor
    cur.close()


def update_as_routes(data, conn):
    """
    Receives a dictionary of the parsed as_route object data.
    Updates this data into the corresponding relation in the database.
    """
    # Converts the data into a dataframe
    as_routes = pd.DataFrame.from_dict(
        {key: [data[key]] for key in data},
        orient="index",
        columns=["routes"],
    )
    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Traverses the data in the dataframe, updating applicable rows
    for i in range(as_routes.shape[0]):
        entry = as_routes.iloc[i]
        # try:
        cur.execute(
            """
            update as_routes 
            set routes=%s
            where as_num=%s
            """,
            (
                entry["routes"],
                entry.name,
            ),
        )

    # Closes the cursor
    cur.close()


# Opens raw data
f = open("./parsed_data/0.json")
data = json.load(f)

# Connect to your postgres DB
user = os.environ["DB_USER"]
dbname = os.environ["DB_NAME"]
conn = psycopg2.connect("dbname=rpsl user=bernardo-ubuntu")

# Updates the data from each RPSL class
update_aut_nums(data["aut_nums"], conn)
update_as_sets(data["as_sets"], conn)
update_route_sets(data["route_sets"], conn)
update_peering_sets(data["peering_sets"], conn)
update_filter_sets(data["filter_sets"], conn)
update_as_routes(data["as_routes"], conn)

# Make the changes to the database persistent
# and closes the connection
conn.commit()
conn.close()
