from fastapi import FastAPI
from .routers import aut_nums
from .routers import as_sets
from .routers import route_sets
from .routers import peering_sets
from .routers import filter_sets
from .routers import as_routes

# Initializes app
app = FastAPI()

# Includes all routers
app.include_router(aut_nums.router)
app.include_router(as_sets.router)
app.include_router(route_sets.router)
app.include_router(peering_sets.router)
app.include_router(filter_sets.router)
app.include_router(as_routes.router)
