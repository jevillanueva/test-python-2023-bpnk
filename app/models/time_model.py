from typing import Optional
from pydantic import BaseModel, Field
from datetime import time
from app.utils.mongo_validator import PyObjectId
from app.models.base import Base

class TimeModel(Base):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    time: time
    disabled: bool = False