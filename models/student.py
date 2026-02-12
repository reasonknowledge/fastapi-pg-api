from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, date

class Student(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    nom: str = Field(max_length=50)
    prenom: str = Field(max_length=50)
    filiere: str = Field(max_length=100)
    email: str = Field(unique=True, index=True)
    annee: date
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
