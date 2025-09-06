from app.module.postgredb.main import engine
from .repo import TrackerRepo

from sqlalchemy import inspect, text
from sqlalchemy.orm import Session
from datetime import datetime

import logging


class Tracker:
    def __init__(self, session: Session):
        self.session = session

    def get_schema(self):
        try:
            inspector = inspect(engine)
            inspector = inspect(engine)

            columns = inspector.get_columns("tracker")

            schema_info = []
            for column in columns:
                schema_info.append(
                    {
                        "name": column["name"],
                        "type": str(column["type"]),
                        "comment": column.get("comment"),
                    }
                )
            return {"table_name": "tracker", "schema": schema_info}
        except Exception as e:
            logging.error(f"Error getting schema: {str(e)}")
            raise e

    def execute_select_query(self, sql_statement: str):
        try:
            result = self.session.execute(text(sql_statement))
            columns = result.keys()
            rows = result.fetchall()
            return {
                "columns": list(columns),
                "rows": [dict(zip(columns, row)) for row in rows],
                "count": len(rows),
            }
        except Exception as e:
            raise ValueError(f"Query execution failed: {str(e)}")

    def list_items(
        self,
        limit: int = 10,
        page: int = 1,
    ):
        offset = (page - 1) * limit
        items = (
            self.session.query(TrackerRepo)
            .filter(TrackerRepo.is_deleted == False)
            .offset(offset)
            .limit(limit)
            .all()
        )
        return [
            {
                "id": str(item.id),
                "name": item.name,
                "description": item.description,
                "category": item.category,
                "price": item.price,
                "restaurant": item.restaurant,
                "purchased_at": str(item.purchased_at),
                "registered_at": str(item.registered_at),
            }
            for item in items
        ]

    def add_item(
        self,
        name: str,
        description: str,
        category: str,
        price: int,
        restaurant: str,
        purchased_at: datetime = None,
    ):
        try:
            if purchased_at is None:
                purchased_at = datetime.utcnow()

            registered_at = datetime.utcnow()

            new_entry = TrackerRepo(
                order_type=name,
                description=description,
                category=category,
                price=price,
                restaurant=restaurant,
                purchased_at=purchased_at,
                registered_at=registered_at,
            )
            self.session.add(new_entry)
            self.session.commit()
            return {
                "id": str(new_entry.id),
                "order_type": name,
                "description": description,
                "category": category,
                "price": price,
                "restaurant": restaurant,
                "purchased_at": str(purchased_at),
                "registered_at": str(registered_at),
            }
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error creating item: {str(e)}")
            raise
