from pydantic import BaseModel
from typing import Optional

class UploadFileBody(BaseModel):
    user_id: str
    folder_name: Optional[str] = "default"
    file_type: Optional[str]  # New field to include file type
