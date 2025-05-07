import psycopg2
from fastapi import APIRouter

# Initializes router
router = APIRouter()


@router.get("/as_routes")
def fetch_as_routes_page(skip: int = 0, limit: int = 10):
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


@router.get("/as_sets")
def fetch__as_sets_page(skip: int = 0, limit: int = 10):
    """
    Fetch entries from the as_sets table.
    Implements pagination with query parameters.
    """
    # Connects to database
    conn = psycopg2.connect("dbname=rpsl user=bernardo-ubuntu")

    # Opens a cursor to perform database operations
    cur = conn.cursor()

    # Queries the slice
    cur.execute(
        """
        select * from as_sets offset %s limit %s
        """,
        (skip, limit),
    )

    # Retrieves and formats slice
    records = cur.fetchall()
    records = [
        {
            "as_set_name": a,
            "as_members": str(b),
            "set_members": str(c),
            "is_any": str(d),
        }
        for (a, b, c, d) in records
    ]

    # Queries the total amount of rows
    cur.execute(
        """
        select count(*) from as_sets
        """,
    )
    count = cur.fetchone()[0]

    # Closes connection
    cur.close()
    conn.close()

    return {"skip": skip, "limit": limit, "count": count, "data": records}


@router.get("/aut_nums")
def fetch_aut_nums_page(skip: int = 0, limit: int = 10):
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


@router.get("/filter_sets")
def fetch_filter_sets_page(skip: int = 0, limit: int = 10):
    """
    Fetch entries from the filter_sets table.
    Implements pagination with query parameters.
    """
    # Connects to database
    conn = psycopg2.connect("dbname=rpsl user=bernardo-ubuntu")

    # Opens a cursor to perform database operations
    cur = conn.cursor()

    # Queries the slice
    cur.execute(
        """
        select * from filter_sets offset %s limit %s
        """,
        (skip, limit),
    )

    # Retrieves and formats slice
    records = cur.fetchall()
    records = [
        {"filter_set_name": a, "body": b, "filters": str(c)} for (a, b, c) in records
    ]

    # Queries the total amount of rows
    cur.execute(
        """
        select count(*) from filter_sets
        """,
    )
    count = cur.fetchone()[0]

    # Closes connection
    cur.close()
    conn.close()

    return {"skip": skip, "limit": limit, "count": count, "data": records}


@router.get("/peering_sets")
def fetch_peering_sets_page(skip: int = 0, limit: int = 10):
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


@router.get("/route_sets")
def fetch_route_sets_page(skip: int = 0, limit: int = 10):
    """
    Fetch entries from the route_sets table.
    Implements pagination with query parameters.
    """
    # Connects to database
    conn = psycopg2.connect("dbname=rpsl user=bernardo-ubuntu")

    # Opens a cursor to perform database operations
    cur = conn.cursor()

    # Queries the slice
    cur.execute(
        """
        select * from route_sets offset %s limit %s
        """,
        (skip, limit),
    )

    # Retrieves and formats slice
    records = cur.fetchall()
    records = [
        {"route_set_name": a, "body": b, "members": str(c)} for (a, b, c) in records
    ]

    # Queries the total amount of rows
    cur.execute(
        """
        select count(*) from route_sets
        """,
    )
    count = cur.fetchone()[0]

    # Closes connection
    cur.close()
    conn.close()

    return {"skip": skip, "limit": limit, "count": count, "data": records}
