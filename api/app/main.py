from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import api_router
from app.models import create_tables
from app.seeding import data_seeder


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    app.include_router(api_router)
    # configure_static(app)
    create_tables()  # new
    data_seeder()
    return app


app = start_application()


origins = ["http://localhost", "http://localhost:8080", "http://localhost:8082"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "hello laxminarayan"}
