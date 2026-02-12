from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class AdminCreate(BaseModel):
    nom: str
    email: EmailStr
    password: str

class AdminRead(BaseModel):
    id: str
    nom: str
    email: EmailStr
    role: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
