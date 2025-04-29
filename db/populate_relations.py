import json
import psycopg2

# Opens data
f = open("../parsed_all/0.json")
data = json.load(f)
aut_nums = pd.DataFrame.from_dict(data["aut_nums"], orient="index")

# Connect to your postgres DB
conn = psycopg2.connect("dbname=rpsl user=bernardo-ubuntu")

# Open a cursor to perform database operations
cur = conn.cursor()

# Traverses the data in the dataframe and inserts it into the database
for i in range(aut_nums.shape[0]):
    entry = aut_nums.iloc[i]
    cur.execute(
        "insert into aut_num (as_num, imports, exports, body) values (%s, %s, %s, %s)",
        (
            entry.name,
            json.dumps(entry["imports"]),
            json.dumps(entry["exports"]),
            entry["body"],
        ),
    )

# Make the changes to the database persistent
conn.commit()

# Closes connection
cur.close()
conn.close()
