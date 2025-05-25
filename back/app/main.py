from .routers import asn, as_set, prefix
from fastapi import FastAPI

# Initializes app
app = FastAPI()

# Includes all routers
app.include_router(asn.router)
app.include_router(as_set.router)
app.include_router(prefix.router)
