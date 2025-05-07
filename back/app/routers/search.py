import json
import psycopg2
from ..utils import parsing
from fastapi import APIRouter

# Initializes router
router = APIRouter(prefix="/search")


@router.get("/asn/{asn}")
def search_asn(asn: int):
    """
    Searches all databases for entries related to the given AS number.
    """
    # Connects to database
    conn = psycopg2.connect("dbname=rpsl user=bernardo-ubuntu")

    # Opens a cursor to perform database operations
    cur = conn.cursor()

    # Queries the aut_nums database
    # Formats results
    cur.execute(
        """
        select * from aut_nums where as_num = %s
        """,
        (asn,),
    )
    record = cur.fetchone()
    if record:
        aut_nums_results = {
            "as_num": record[0],
            "imports": parsing.process_rules(record[1]),
            "exports": parsing.process_rules(record[2]),
            "body": record[3],
        }
    else:
        aut_nums_results = {"as_num": "", "imports": [], "exports": [], "body": ""}

    # Queries the as_sets database
    # Formats results
    cur.execute(
        """
        select * from as_sets where %s = any (as_members)
        """,
        (asn,),
    )
    records = cur.fetchall()
    as_sets_results = [
        {
            "as_set_name": a,
            "as_members": b,
            "set_members": c,
            "is_any": d,
        }
        for (a, b, c, d) in records
    ]

    # Closes connection
    cur.close()
    conn.close()

    return {"aut_nums": aut_nums_results, "as_sets": as_sets_results}
