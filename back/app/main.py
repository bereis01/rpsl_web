import psycopg2
import pandas as pd
from fastapi import FastAPI

app = FastAPI()


@app.get("/aut_num/{as_num}")
def as_num(as_num: int):
    # Connect to your postgres DB
    conn = psycopg2.connect("dbname=rpsl user=bernardo-ubuntu")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a query
    cur.execute("select * from aut_num where as_num=%s", (as_num,))

    # Retrieve query results
    records = cur.fetchall()
    records = [
        {"as_num": a, "imports": b, "exports": c, "body": d} for (a, b, c, d) in records
    ]

    # Closes connection
    cur.close()
    conn.close()

    return {"data": records}
