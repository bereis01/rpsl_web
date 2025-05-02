import psycopg2
from fastapi import APIRouter

# Initializes router
router = APIRouter()


@router.get("/as_routes")
def fetch_page(skip: int = 0, limit: int = 10):
    """
    Fetch entries from the as_routes table.
    Implements pagination with query parameters.
    """
    # Connects to database
    conn = psycopg2.connect("dbname=rpsl user=bernardo-ubuntu")

    # Opens a cursor to perform database operations
    cur = conn.cursor()

    # Queries the slice
    cur.execute(
        """
        select * from as_routes offset %s limit %s
        """,
        (skip, limit),
    )

    # Retrieves and formats slice
    records = cur.fetchall()
    records = [{"as_num": a, "routes": str(b)} for (a, b) in records]

    # Queries the total amount of rows
    cur.execute(
        """
        select count(*) from as_routes
        """,
    )
    count = cur.fetchone()[0]

    # Closes connection
    cur.close()
    conn.close()

    return {"skip": skip, "limit": limit, "count": count, "data": records}
