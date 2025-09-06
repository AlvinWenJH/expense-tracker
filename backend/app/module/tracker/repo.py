import uuid

from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Column,
    Text,
    TIMESTAMP,
    Integer,
    Boolean,
)


Base = declarative_base()


class TrackerRepo(Base):
    __tablename__ = "tracker"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    order_type = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    restaurant = Column(Text, nullable=False)
    purchased_at = Column(TIMESTAMP(timezone=True), nullable=False)
    registered_at = Column(TIMESTAMP(timezone=True), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    class Config:
        orm_mode = True
