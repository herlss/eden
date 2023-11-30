from fastapi import FastAPI
from app.api.routers import status, dashboard
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(status.router)
app.include_router(dashboard.router)


origins = [
    "https://eden-front.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)