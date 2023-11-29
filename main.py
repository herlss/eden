from fastapi import FastAPI
from app.api.routers import status

app = FastAPI()

app.include_router(status.router)