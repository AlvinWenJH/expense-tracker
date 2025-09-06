from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from app.module.tracker import Tracker
from app.module.postgredb.main import PostgresDB
from sqlalchemy.orm import Session
from datetime import datetime

router = APIRouter(prefix="/v1/tracker", tags=["tracker"])


class ItemCreate(BaseModel):
    name: str
    description: str
    category: str
    price: int
    restaurant: str
    purchased_at: datetime = datetime.now()


@router.post("/execute_select_query")
async def execute_select_query(
    sql_statement: str = Query(..., min_length=1),
    db: Session = Depends(PostgresDB.get_session),
):
    if not sql_statement.strip():
        raise HTTPException(status_code=400, detail="SQL statement cannot be empty")

    sql_upper = sql_statement.upper().strip()
    if not sql_upper.startswith("SELECT"):
        raise HTTPException(
            status_code=400, detail="Only SELECT statements are allowed"
        )

    tracker = Tracker(db)
    try:
        result = tracker.execute_select_query(sql_statement)
        return {"data": result, "status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid query: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/list_items")
async def list_items(
    limit: int = 10,
    page: int = 1,
    db: Session = Depends(PostgresDB.get_session),
):
    tracker = Tracker(db)
    try:
        result = tracker.list_items(limit=limit, page=page)
        return {"data": result, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/schema")
async def get_schema(
    db: Session = Depends(PostgresDB.get_session),
):
    tracker = Tracker(db)
    try:
        schema = tracker.get_schema()
        return {"data": schema, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error\n\n{e}")


@router.post("/insert_item")
async def insert_item(
    item: ItemCreate,
    db: Session = Depends(PostgresDB.get_session),
):
    tracker = Tracker(db)
    try:
        result = tracker.add_item(
            name=item.name,
            description=item.description,
            category=item.category,
            price=item.price,
            restaurant=item.restaurant,
            purchased_at=item.purchased_at,
        )
        return {"data": result, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
