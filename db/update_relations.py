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
            update aut_num 
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


# Opens raw data
f = open("./parsed_data/0.json")
data = json.load(f)

# Connect to your postgres DB
user = os.environ["DB_USER"]
dbname = os.environ["DB_NAME"]
conn = psycopg2.connect("dbname=rpsl user=bernardo-ubuntu")

# Updates the data from each RPSL class
update_aut_nums(data["aut_nums"], conn)

# Make the changes to the database persistent
# and closes the connection
conn.commit()
conn.close()
