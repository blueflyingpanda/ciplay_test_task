from fastapi import FastAPI
from utils.db import db_pool
from utils.rest import router
from fastapi.responses import RedirectResponse

app = FastAPI()
app.include_router(router)


@app.get("/")
async def root():
    return RedirectResponse(url=app.docs_url)


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    if db_pool:
        db_pool.closeall()
