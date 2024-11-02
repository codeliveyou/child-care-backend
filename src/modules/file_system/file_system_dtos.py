from pydantic import BaseModel
from typing import Optional

class UploadFileBody(BaseModel):
    user_id: str
    folder_name: Optional[str] = "default"
