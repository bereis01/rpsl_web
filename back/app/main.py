import os
from . import context
from shared.storage import ObjStr
from fastapi import FastAPI
from .routers import addr, asn, asset, rs

# Initializes app
app = FastAPI()

# Initializes connection to storage
app.state.storage = ObjStr(os.getenv("OBJSTR_PATH"))

# Includes all routers
app.include_router(asn.router)
app.include_router(asset.router)
app.include_router(addr.router)
app.include_router(rs.router)
