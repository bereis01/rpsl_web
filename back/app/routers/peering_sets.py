import psycopg2
from fastapi import APIRouter

# Initializes router
router = APIRouter()


@router.get("/peering_sets")
def fetch_page(skip: int = 0, limit: int = 10):
    """
    Fetch entries from the peering_sets table.
    Implements pagination with query parameters.
    """
    # Connects to database
    conn = psycopg2.connect("dbname=rpsl user=bernardo-ubuntu")

    # Opens a cursor to perform database operations
    cur = conn.cursor()

    # Queries the slice
    cur.execute(
        """
        select * from peering_sets offset %s limit %s
        """,
        (skip, limit),
    )

    # Retrieves and formats slice
    records = cur.fetchall()
    records = [
        {"peering_set_name": a, "body": b, "peerings": str(c)} for (a, b, c) in records
    ]

    # Queries the total amount of rows
    cur.execute(
        """
        select count(*) from peering_sets
        """,
    )
    count = cur.fetchone()[0]

    # Closes connection
    cur.close()
    conn.close()

    return {"skip": skip, "limit": limit, "count": count, "data": records}
