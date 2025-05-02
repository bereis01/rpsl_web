import psycopg2
from fastapi import APIRouter

# Initializes router
router = APIRouter()


@router.get("/aut_nums")
def fetch_page(skip: int = 0, limit: int = 10):
    """
    Fetch entries from the aut_nums table.
    Implements pagination with query parameters.
    """
    # Connects to database
    conn = psycopg2.connect("dbname=rpsl user=bernardo-ubuntu")

    # Opens a cursor to perform database operations
    cur = conn.cursor()

    # Queries the slice
    cur.execute(
        """
        select * from aut_nums offset %s limit %s
        """,
        (skip, limit),
    )

    # Retrieves and formats slice
    records = cur.fetchall()
    records = [
        {"as_num": a, "imports": str(b), "exports": str(c), "body": d}
        for (a, b, c, d) in records
    ]

    # Queries the total amount of rows
    cur.execute(
        """
        select count(*) from aut_nums
        """,
    )
    count = cur.fetchone()[0]

    # Closes connection
    cur.close()
    conn.close()

    return {"skip": skip, "limit": limit, "count": count, "data": records}
