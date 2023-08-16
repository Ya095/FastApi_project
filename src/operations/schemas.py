from datetime import datetime
from pydantic import BaseModel, Field


class OperationCreate(BaseModel):
    id: int
    quantity: str
    figi: str
    instrument_type: str
    date: datetime = Field(default=datetime.today().replace(microsecond=0))
    type: str
