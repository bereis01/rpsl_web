from .routers import raw
from .routers import search
from fastapi import FastAPI

# Initializes app
app = FastAPI()

# Includes all routers
app.include_router(raw.router)
app.include_router(search.router)
