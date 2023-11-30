from fastapi import FastAPI
from app.api.routers import status, dashboard

app = FastAPI()

app.include_router(status.router)
app.include_router(dashboard.router)