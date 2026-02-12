from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Admin(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    nom: str = Field(max_length=50)
    email: str = Field(unique=True, index=True)
    password_hash: str
    role: str = Field(default="admin", max_length=10)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
