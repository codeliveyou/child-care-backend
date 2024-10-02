from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreateSystemUsageBody(BaseModel):
    date: datetime
    total_users: int
    active_users: int
    total_sessions: int
    average_session_duration: float

class UpdateSystemUsageBody(BaseModel):
    total_users: Optional[int] = None
    active_users: Optional[int] = None
    total_sessions: Optional[int] = None
    average_session_duration: Optional[float] = None
