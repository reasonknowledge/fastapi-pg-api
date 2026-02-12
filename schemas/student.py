from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date, datetime

class StudentCreate(BaseModel):
    nom: str
    prenom: str
    filiere: str
    email: EmailStr
    annee: date

class StudentRead(BaseModel):
    id: str
    nom: str
    prenom: str
    filiere: str
    email: EmailStr
    annee: date
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
