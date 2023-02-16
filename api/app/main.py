from fastapi import FastAPI

from .config import settings


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    return app


app = start_application()


@app.get("/")
async def root():
    return {"message": "hello fastapi"}
