from fastapi import FastAPI

from .routers import tracker

from app.module.postgredb import PostgresDB

app = FastAPI(root_path="/api")

app.include_router(tracker.router)

try:
    with PostgresDB() as postgres:
        postgres.cursor.execute(postgres.query["CREATE_TRACKER_TABLE"])
        postgres.conn.commit()
except Exception as e:
    print(e, flush=True)
