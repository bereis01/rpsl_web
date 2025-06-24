from storage import ObjStr
from fastapi import FastAPI
from .routers import asn, as_set, prefix

# Initializes app
app = FastAPI()

# Initializes connection to storage
app.state.storage = ObjStr("./data/")

# Includes all routers
app.include_router(asn.router)
app.include_router(as_set.router)
app.include_router(prefix.router)
